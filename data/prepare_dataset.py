"""
Dataset preparation script for VidyaAI fine-tuning.

Collects and formats educational QA data from multiple sources into
a unified instruction-tuning format for Gemma 4 fine-tuning with Unsloth.

Sources:
- ai4bharat/IndicQA (Indian language QA)
- Custom NCERT-style educational QA pairs

Output format (JSONL):
{
    "instruction": "system prompt with language/subject context",
    "input": "student question",
    "output": "teacher response"
}
"""

import json
import os
import argparse
from pathlib import Path

try:
    from datasets import load_dataset
except ImportError:
    print("Install datasets: pip install datasets")
    exit(1)


SYSTEM_PROMPTS = {
    "hindi": (
        "तुम VidyaAI हो, एक बुद्धिमान शिक्षा सहायक। "
        "NCERT पाठ्यक्रम के अनुसार सरल हिंदी में जवाब दो।"
    ),
    "english": (
        "You are VidyaAI, an intelligent education assistant. "
        "Answer according to NCERT curriculum in clear English."
    ),
}

# Educational QA templates for generating synthetic data
EDUCATIONAL_TEMPLATES_HINDI = [
    {
        "subject": "science",
        "input": "प्रकाश संश्लेषण क्या है?",
        "output": (
            "प्रकाश संश्लेषण वह प्रक्रिया है जिसमें हरे पौधे सूर्य के प्रकाश की ऊर्जा का उपयोग करके "
            "कार्बन डाइऑक्साइड और पानी से ग्लूकोज (भोजन) बनाते हैं। इस प्रक्रिया में ऑक्सीजन भी निकलती है।\n\n"
            "समीकरण: 6CO₂ + 6H₂O + सूर्य का प्रकाश → C₆H₁₂O₆ + 6O₂\n\n"
            "यह प्रक्रिया पत्तियों में मौजूद क्लोरोफिल की मदद से होती है।"
        ),
    },
    {
        "subject": "math",
        "input": "पाइथागोरस प्रमेय क्या है? उदाहरण के साथ समझाइए।",
        "output": (
            "पाइथागोरस प्रमेय कहता है कि एक समकोण त्रिभुज में, कर्ण का वर्ग "
            "अन्य दो भुजाओं के वर्गों के योग के बराबर होता है।\n\n"
            "सूत्र: c² = a² + b²\n\n"
            "उदाहरण: अगर एक त्रिभुज की दो भुजाएं 3 cm और 4 cm हैं, तो:\n"
            "c² = 3² + 4² = 9 + 16 = 25\n"
            "c = √25 = 5 cm\n\n"
            "इसलिए कर्ण 5 cm होगा।"
        ),
    },
    {
        "subject": "history",
        "input": "भारत की आज़ादी कब और कैसे मिली?",
        "output": (
            "भारत को 15 अगस्त 1947 को ब्रिटिश शासन से आज़ादी मिली।\n\n"
            "मुख्य बिंदु:\n"
            "1. महात्मा गांधी ने अहिंसा और सत्याग्रह के माध्यम से स्वतंत्रता आंदोलन का नेतृत्व किया।\n"
            "2. 1942 में 'भारत छोड़ो आंदोलन' ने ब्रिटिश शासन को हिला दिया।\n"
            "3. सुभाष चंद्र बोस ने आज़ाद हिंद फ़ौज बनाई।\n"
            "4. द्वितीय विश्व युद्ध के बाद ब्रिटेन कमज़ोर हो गया।\n"
            "5. अंततः माउंटबेटन योजना के तहत भारत और पाकिस्तान का विभाजन हुआ।\n\n"
            "पंडित जवाहरलाल नेहरू भारत के पहले प्रधानमंत्री बने।"
        ),
    },
    {
        "subject": "science",
        "input": "न्यूटन के गति के तीन नियम क्या हैं?",
        "output": (
            "न्यूटन के गति के तीन नियम:\n\n"
            "**पहला नियम (जड़त्व का नियम):**\n"
            "कोई वस्तु विराम अवस्था में रहती है या एकसमान गति से चलती रहती है, "
            "जब तक कोई बाहरी बल उस पर न लगाया जाए।\n"
            "उदाहरण: बस के अचानक रुकने पर हम आगे गिरते हैं।\n\n"
            "**दूसरा नियम (F = ma):**\n"
            "बल = द्रव्यमान × त्वरण। जितना ज़्यादा बल, उतना ज़्यादा त्वरण।\n"
            "उदाहरण: क्रिकेट बॉल को ज़ोर से मारने पर वह तेज़ जाती है।\n\n"
            "**तीसरा नियम (क्रिया-प्रतिक्रिया):**\n"
            "हर क्रिया की बराबर और विपरीत प्रतिक्रिया होती है।\n"
            "उदाहरण: रॉकेट गैसों को नीचे फेंकता है, और ऊपर उठता है।"
        ),
    },
]


def format_as_instruction(system: str, user_input: str, output: str) -> dict:
    return {
        "instruction": system,
        "input": user_input,
        "output": output,
    }


def load_indic_qa(max_samples: int = 5000) -> list[dict]:
    """Load and format IndicQA dataset."""
    examples = []
    try:
        dataset = load_dataset("ai4bharat/IndicQA", "indicqa.hi", split="test")
        for item in dataset.select(range(min(max_samples, len(dataset)))):
            context = item.get("context", "")
            question = item.get("question", "")
            answers = item.get("answers", {})
            answer_text = answers.get("text", [""])[0] if answers else ""

            if question and answer_text:
                full_output = answer_text
                if context:
                    full_output = f"{answer_text}\n\nसंदर्भ: {context[:200]}"

                examples.append(
                    format_as_instruction(
                        SYSTEM_PROMPTS["hindi"],
                        question,
                        full_output,
                    )
                )
    except Exception as e:
        print(f"Warning: Could not load IndicQA: {e}")

    return examples


def generate_seed_examples() -> list[dict]:
    """Generate seed examples from templates."""
    examples = []
    for item in EDUCATIONAL_TEMPLATES_HINDI:
        examples.append(
            format_as_instruction(
                SYSTEM_PROMPTS["hindi"],
                item["input"],
                item["output"],
            )
        )
    return examples


def save_dataset(examples: list[dict], output_path: str):
    """Save dataset as JSONL."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for ex in examples:
            f.write(json.dumps(ex, ensure_ascii=False) + "\n")
    print(f"Saved {len(examples)} examples to {output_path}")


def main():
    parser = argparse.ArgumentParser(description="Prepare VidyaAI training dataset")
    parser.add_argument(
        "--output", default="data/processed/train.jsonl", help="Output JSONL path"
    )
    parser.add_argument(
        "--max-samples", type=int, default=5000, help="Max samples from each source"
    )
    args = parser.parse_args()

    all_examples = []

    # 1. Seed examples (high quality, hand-crafted)
    seed = generate_seed_examples()
    print(f"Seed examples: {len(seed)}")
    all_examples.extend(seed)

    # 2. IndicQA
    indic = load_indic_qa(args.max_samples)
    print(f"IndicQA examples: {len(indic)}")
    all_examples.extend(indic)

    # Summary
    print(f"\nTotal examples: {len(all_examples)}")
    save_dataset(all_examples, args.output)

    # Also save a small validation split
    val_size = min(100, len(all_examples) // 10)
    if val_size > 0:
        val_path = args.output.replace("train.jsonl", "val.jsonl")
        save_dataset(all_examples[:val_size], val_path)


if __name__ == "__main__":
    main()

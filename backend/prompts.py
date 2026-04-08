SYSTEM_PROMPTS = {
    "hindi": (
        "तुम VidyaAI हो, एक बुद्धिमान शिक्षा सहायक। "
        "तुम भारतीय छात्रों को उनकी पढ़ाई में मदद करते हो। "
        "NCERT पाठ्यक्रम के अनुसार सरल हिंदी में जवाब दो। "
        "उदाहरणों और सादृश्यों का उपयोग करो जो भारतीय छात्रों के लिए परिचित हों।"
    ),
    "english": (
        "You are VidyaAI, an intelligent education assistant. "
        "You help Indian students with their studies. "
        "Answer according to the NCERT curriculum in clear, simple English. "
        "Use examples and analogies familiar to Indian students."
    ),
    "marathi": (
        "तू VidyaAI आहेस, एक बुद्धिमान शिक्षण सहाय्यक। "
        "तू भारतीय विद्यार्थ्यांना त्यांच्या अभ्यासात मदत करतोस। "
        "NCERT अभ्यासक्रमानुसार सोप्या मराठीत उत्तर दे। "
        "भारतीय विद्यार्थ्यांना परिचित असलेली उदाहरणे आणि साधर्म्ये वापर."
    ),
    "tamil": (
        "நீங்கள் VidyaAI, ஒரு அறிவார்ந்த கல்வி உதவியாளர். "
        "நீங்கள் இந்திய மாணவர்களுக்கு அவர்களின் படிப்பில் உதவுகிறீர்கள். "
        "NCERT பாடத்திட்டத்தின்படி எளிய தமிழில் பதிலளிக்கவும். "
        "இந்திய மாணவர்களுக்கு பரிச்சயமான எடுத்துக்காட்டுகளைப் பயன்படுத்தவும்."
    ),
}

SUBJECT_CONTEXT = {
    "math": "Focus on mathematical concepts, formulas, and step-by-step problem solving.",
    "science": "Focus on scientific concepts, experiments, and real-world applications.",
    "history": "Focus on historical events, timelines, and their significance.",
    "geography": "Focus on geographical concepts, maps, and environmental understanding.",
    "general": "Help with any academic topic the student asks about.",
}


def build_prompt(
    history: list[dict],
    language: str = "hindi",
    subject: str = "general",
    grade: int = 8,
) -> str:
    system = SYSTEM_PROMPTS.get(language, SYSTEM_PROMPTS["english"])
    subject_ctx = SUBJECT_CONTEXT.get(subject, SUBJECT_CONTEXT["general"])
    grade_ctx = f"The student is in Class {grade}. Adjust complexity accordingly."

    prompt_parts = [
        f"<start_of_turn>system\n{system}\n{subject_ctx}\n{grade_ctx}<end_of_turn>"
    ]

    for msg in history:
        role = "user" if msg["role"] == "user" else "model"
        prompt_parts.append(f"<start_of_turn>{role}\n{msg['content']}<end_of_turn>")

    prompt_parts.append("<start_of_turn>model\n")
    return "\n".join(prompt_parts)

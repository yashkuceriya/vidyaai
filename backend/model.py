import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from peft import PeftModel
from dotenv import load_dotenv

load_dotenv()

# Configuration
BASE_MODEL = os.getenv("BASE_MODEL", "google/gemma-4-e4b")
LORA_ADAPTER = os.getenv("LORA_ADAPTER", "")  # HuggingFace path to LoRA weights
MAX_NEW_TOKENS = int(os.getenv("MAX_NEW_TOKENS", "512"))
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


class ModelService:
    def __init__(self):
        self.model = None
        self.tokenizer = None

    def load(self):
        print(f"Loading model: {BASE_MODEL} on {DEVICE}")

        quantization_config = None
        if DEVICE == "cuda":
            quantization_config = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_quant_type="nf4",
                bnb_4bit_compute_dtype=torch.bfloat16,
            )

        self.tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
        self.model = AutoModelForCausalLM.from_pretrained(
            BASE_MODEL,
            quantization_config=quantization_config,
            device_map="auto" if DEVICE == "cuda" else None,
            torch_dtype=torch.bfloat16,
        )

        # Load LoRA adapter if specified
        if LORA_ADAPTER:
            print(f"Loading LoRA adapter: {LORA_ADAPTER}")
            self.model = PeftModel.from_pretrained(self.model, LORA_ADAPTER)

        self.model.eval()
        print("Model loaded successfully")

    def generate(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)

        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                do_sample=True,
                temperature=0.7,
                top_p=0.9,
                repetition_penalty=1.1,
            )

        # Decode only the new tokens
        new_tokens = outputs[0][inputs["input_ids"].shape[1]:]
        response = self.tokenizer.decode(new_tokens, skip_special_tokens=True)
        return response.strip()

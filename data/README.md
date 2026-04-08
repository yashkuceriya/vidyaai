# VidyaAI Training Dataset

## Sources

1. **Seed Examples** — Hand-crafted Hindi educational QA pairs covering Math, Science, History
2. **ai4bharat/IndicQA** — Hindi question-answering dataset from AI4Bharat
3. **Custom** — Additional examples generated from NCERT curriculum content

## Format

JSONL with fields:
- `instruction`: System prompt with language/subject context
- `input`: Student question
- `output`: Teacher response

## Usage

```bash
pip install datasets
python prepare_dataset.py --output processed/train.jsonl --max-samples 5000
```

## Statistics

Target: 10K-20K training examples across Hindi + English

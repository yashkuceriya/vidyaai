# VidyaAI - Multilingual Education Assistant

> Empowering Indian students with AI-powered education in their native language.

VidyaAI is a multilingual education assistant powered by **Gemma 4**, fine-tuned using **Unsloth** for Indian regional languages. It helps students learn subjects like Math, Science, and History in Hindi, Marathi, Tamil, and English through an intuitive chat and voice interface.

## The Problem

250M+ Indian students lack access to quality education in their native language. Teachers are scarce in rural areas, and existing digital tools are primarily English-only. Language becomes a barrier to learning.

## The Solution

VidyaAI brings a personal AI tutor to every student's phone — one that speaks their language, understands their curriculum (NCERT), and adapts to their level.

### Features

- **Multilingual Chat** — Ask questions in Hindi, Marathi, Tamil, or English
- **Voice Interaction** — Speak your question, hear the answer (powered by Whisper + Edge TTS)
- **Curriculum-Aligned** — Trained on NCERT content for Classes 6-12
- **Quiz Mode** — Practice with AI-generated questions and get instant feedback
- **Mobile-First** — Designed for smartphone access in low-bandwidth environments

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Model | Gemma 4 E4B, fine-tuned with Unsloth (QLoRA) |
| Backend | Python, FastAPI |
| Frontend | Next.js, TypeScript, Tailwind CSS |
| Voice | Whisper (STT) + Edge TTS |
| Hosting | AWS (model) + Vercel (frontend) |

## Project Structure

```
vidyaai/
├── notebooks/          # Unsloth fine-tuning notebook (Colab-ready)
├── data/               # Dataset preparation scripts
├── backend/            # FastAPI server
├── frontend/           # Next.js web app
├── deploy/             # Deployment configs
└── docker-compose.yml  # Local development
```

## Getting Started

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Built For

- [Gemma 4 Good Hackathon](https://kaggle.com/competitions/gemma-4-good-hackathon) on Kaggle
- Tracks: Unsloth | Digital Equity & Inclusivity | Future of Education

## License

MIT

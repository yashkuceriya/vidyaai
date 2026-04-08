from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from contextlib import asynccontextmanager
import uuid

from model import ModelService
from prompts import build_prompt
from voice import transcribe_audio, synthesize_speech
from quiz import generate_quiz, grade_answer

model_service: ModelService = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global model_service
    model_service = ModelService()
    model_service.load()
    yield
    del model_service


app = FastAPI(title="VidyaAI", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory conversation store
conversations: dict[str, list[dict]] = {}


class ChatRequest(BaseModel):
    message: str
    language: str = "hindi"
    subject: str = "general"
    grade: int = 8
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    reply: str
    conversation_id: str


class QuizRequest(BaseModel):
    topic: str
    language: str = "hindi"
    subject: str = "science"
    grade: int = 8
    num_questions: int = 3


class QuizAnswerRequest(BaseModel):
    question: str
    correct_answer: str
    student_answer: str
    language: str = "hindi"


@app.get("/health")
async def health():
    return {"status": "ok", "model_loaded": model_service is not None}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    conv_id = req.conversation_id or str(uuid.uuid4())

    if conv_id not in conversations:
        conversations[conv_id] = []

    conversations[conv_id].append({"role": "user", "content": req.message})

    prompt = build_prompt(
        history=conversations[conv_id],
        language=req.language,
        subject=req.subject,
        grade=req.grade,
    )

    reply = model_service.generate(prompt)
    conversations[conv_id].append({"role": "assistant", "content": reply})

    return ChatResponse(reply=reply, conversation_id=conv_id)


@app.post("/api/voice")
async def voice_chat(
    audio: UploadFile = File(...),
    language: str = "hindi",
    subject: str = "general",
    grade: int = 8,
    conversation_id: str | None = None,
):
    audio_bytes = await audio.read()
    transcript = transcribe_audio(audio_bytes, language)

    if not transcript:
        raise HTTPException(status_code=400, detail="Could not transcribe audio")

    conv_id = conversation_id or str(uuid.uuid4())
    if conv_id not in conversations:
        conversations[conv_id] = []

    conversations[conv_id].append({"role": "user", "content": transcript})

    prompt = build_prompt(
        history=conversations[conv_id],
        language=language,
        subject=subject,
        grade=grade,
    )

    reply = model_service.generate(prompt)
    conversations[conv_id].append({"role": "assistant", "content": reply})

    audio_response = await synthesize_speech(reply, language)

    return {
        "transcript": transcript,
        "reply": reply,
        "audio_url": audio_response,
        "conversation_id": conv_id,
    }


@app.post("/api/quiz")
async def create_quiz(req: QuizRequest):
    prompt = generate_quiz(
        topic=req.topic,
        language=req.language,
        subject=req.subject,
        grade=req.grade,
        num_questions=req.num_questions,
    )
    result = model_service.generate(prompt)
    return {"quiz": result}


@app.post("/api/quiz/grade")
async def grade_quiz(req: QuizAnswerRequest):
    prompt = grade_answer(
        question=req.question,
        correct_answer=req.correct_answer,
        student_answer=req.student_answer,
        language=req.language,
    )
    result = model_service.generate(prompt)
    return {"feedback": result}

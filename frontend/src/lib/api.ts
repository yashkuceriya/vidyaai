const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ChatRequest {
  message: string;
  language: string;
  subject: string;
  grade: number;
  conversation_id?: string;
}

export interface ChatResponse {
  reply: string;
  conversation_id: string;
}

export interface QuizRequest {
  topic: string;
  language: string;
  subject: string;
  grade: number;
  num_questions: number;
}

export interface QuizGradeRequest {
  question: string;
  correct_answer: string;
  student_answer: string;
  language: string;
}

export async function sendMessage(req: ChatRequest): Promise<ChatResponse> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) throw new Error(`Chat failed: ${res.statusText}`);
  return res.json();
}

export async function sendVoice(
  audio: Blob,
  language: string,
  subject: string,
  grade: number,
  conversationId?: string
) {
  const formData = new FormData();
  formData.append("audio", audio, "recording.wav");
  formData.append("language", language);
  formData.append("subject", subject);
  formData.append("grade", String(grade));
  if (conversationId) formData.append("conversation_id", conversationId);

  const res = await fetch(`${API_BASE}/api/voice`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error(`Voice failed: ${res.statusText}`);
  return res.json();
}

export async function generateQuiz(req: QuizRequest) {
  const res = await fetch(`${API_BASE}/api/quiz`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) throw new Error(`Quiz failed: ${res.statusText}`);
  return res.json();
}

export async function gradeQuizAnswer(req: QuizGradeRequest) {
  const res = await fetch(`${API_BASE}/api/quiz/grade`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(req),
  });
  if (!res.ok) throw new Error(`Grading failed: ${res.statusText}`);
  return res.json();
}

QUIZ_LANGUAGE_INSTRUCTION = {
    "hindi": "प्रश्न और उत्तर हिंदी में लिखो।",
    "english": "Write questions and answers in English.",
    "marathi": "प्रश्न आणि उत्तरे मराठीत लिहा.",
    "tamil": "கேள்விகளையும் பதில்களையும் தமிழில் எழுதுங்கள்.",
}


def generate_quiz(
    topic: str,
    language: str = "hindi",
    subject: str = "science",
    grade: int = 8,
    num_questions: int = 3,
) -> str:
    lang_instruction = QUIZ_LANGUAGE_INSTRUCTION.get(
        language, QUIZ_LANGUAGE_INSTRUCTION["english"]
    )

    return f"""<start_of_turn>system
You are VidyaAI, an education assistant creating quizzes for Indian students.
Create exactly {num_questions} multiple-choice questions about "{topic}" for Class {grade} {subject}.
{lang_instruction}

Format each question as:
Q1: [question]
A) [option]
B) [option]
C) [option]
D) [option]
Answer: [correct letter]

Make questions progressively harder. Use NCERT curriculum as reference.<end_of_turn>
<start_of_turn>model
"""


def grade_answer(
    question: str,
    correct_answer: str,
    student_answer: str,
    language: str = "hindi",
) -> str:
    lang_instruction = QUIZ_LANGUAGE_INSTRUCTION.get(
        language, QUIZ_LANGUAGE_INSTRUCTION["english"]
    )

    return f"""<start_of_turn>system
You are VidyaAI, an encouraging education assistant.
Grade the student's answer and provide helpful feedback.
{lang_instruction}
Be encouraging but honest. If wrong, explain why and give the correct answer with a brief explanation.<end_of_turn>
<start_of_turn>user
Question: {question}
Correct Answer: {correct_answer}
Student's Answer: {student_answer}

Please grade this and provide feedback.<end_of_turn>
<start_of_turn>model
"""

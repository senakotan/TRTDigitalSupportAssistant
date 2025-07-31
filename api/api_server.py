
from fastapi import FastAPI
from pydantic import BaseModel
from src.rag_logic import get_relevant_context, generate_llm_answer

class QuestionRequest(BaseModel):
    question: str

class AnswerResponse(BaseModel):
    answer: str

app = FastAPI(title="TRT Bilgi Asistani API")

@app.post("/ask", response_model=AnswerResponse)
def ask_question(request: QuestionRequest):
    soru = request.question
    context = get_relevant_context(soru)
    final_answer = generate_llm_answer(soru, context)
    return AnswerResponse(answer=final_answer)

@app.get("/")
def root():
    return {"message": "TRT Bilgi Asistani API Aktif"}

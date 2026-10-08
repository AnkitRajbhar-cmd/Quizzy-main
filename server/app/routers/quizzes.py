from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from typing import List
from app.db.database import quizzes_collection, scores_collection
from app.models.schemas import QuizCreate, QuizDB, QuizPublic, QuizSubmission, QuizResult, UserInDB
from app.services.langgraph_workflow import generate_quiz_from_text
from app.core.security import get_current_user
from app.services.pdf_parser import extract_text_from_pdf
from pypdf import PdfReader
import io
from bson import ObjectId
from datetime import datetime

router = APIRouter()

@router.post("/generate", response_model=QuizPublic)
async def generate_quiz(
    file: UploadFile = File(...),
    current_user: UserInDB = Depends(get_current_user)
):
    if file.content_type != "application/pdf":
        raise HTTPException(400, "File must be PDF")
    
    # 1. Parse PDF
    content = await file.read()
    text = extract_text_from_pdf(content)
        
    # 2. AI Generation
    try:
        questions = await generate_quiz_from_text(text)
    except RuntimeError as exc:
        # Likely missing API key or LLM configuration
        raise HTTPException(status_code=503, detail=str(exc))
    
    if not questions:
        raise HTTPException(500, "Failed to generate quiz")

    # 3. Save to DB
    quiz_data = QuizDB(
        title=f"Quiz: {file.filename}",
        source_filename=file.filename,
        questions=questions,
        user_id=str(current_user.id)
    )
    new_quiz = await quizzes_collection.insert_one(quiz_data.dict(by_alias=True))
    
    # 4. Return Sanitized Quiz
    return QuizPublic(
        id=str(new_quiz.inserted_id),
        title=quiz_data.title,
        source_filename=quiz_data.source_filename,
        created_at=quiz_data.created_at,
        questions=[{k: v for k, v in q.items() if k not in ["correct_answer", "explanation"]} for q in questions]
    )

@router.get("/{id}", response_model=QuizPublic)
async def get_quiz(id: str, current_user: UserInDB = Depends(get_current_user)):
    quiz = await quizzes_collection.find_one({"_id": ObjectId(id)})
    if not quiz:
        raise HTTPException(404, "Quiz not found")
        
    # Strip answers for the taker view
    stripped_questions = [
        {k: v for k, v in q.items() if k not in ["correct_answer", "explanation"]} 
        for q in quiz["questions"]
    ]
    
    return {
        "id": str(quiz["_id"]),
        "title": quiz["title"],
        "source_filename": quiz["source_filename"],
        "created_at": quiz["created_at"],
        "questions": stripped_questions
    }

@router.post("/submit/{id}", response_model=QuizResult)
async def submit_quiz(
    id: str, 
    submission: QuizSubmission, 
    current_user: UserInDB = Depends(get_current_user)
):
    quiz = await quizzes_collection.find_one({"_id": ObjectId(id)})
    if not quiz:
        raise HTTPException(404, "Quiz not found")
        
    correct_count = 0
    analysis = []
    
    for q in quiz["questions"]:
        user_ans = submission.answers.get(q["id"])
        is_correct = user_ans == q["correct_answer"]
        if is_correct:
            correct_count += 1
            
        analysis.append({
            "question_id": q["id"],
            "question_text": q["text"],
            "user_answer": user_ans,
            "correct_answer": q["correct_answer"],
            "is_correct": is_correct,
            "explanation": q["explanation"]
        })
        
    percentage = (correct_count / len(quiz["questions"])) * 100
    
    # Save score
    await scores_collection.insert_one({
        "user_id": current_user.id,
        "quiz_id": ObjectId(id),
        "score": correct_count,
        "percentage": percentage,
        "created_at": datetime.utcnow()
    })
    
    return {
        "score": correct_count,
        "percentage": percentage,
        "analysis": analysis
    }

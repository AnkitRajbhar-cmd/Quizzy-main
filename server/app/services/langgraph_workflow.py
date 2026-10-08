import json
from typing import List, TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import StateGraph, END
from langchain_core.messages import SystemMessage, HumanMessage
from app.core.config import settings
from functools import lru_cache

# Lazy LLM factory to avoid import-time validation errors when API key is missing
@lru_cache()
def get_llm():
    if not settings.GOOGLE_API_KEY:
        raise RuntimeError("GOOGLE_API_KEY not set. Set the env var to use the LLM features.")
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=settings.GOOGLE_API_KEY,
        temperature=0.3
    )

# Graph State
class QuizState(TypedDict):
    text_content: str
    raw_questions: List[dict]
    validated_questions: List[dict]
    quality_score: int
    attempt: int

# --- NODE 1: GENERATOR ---
def generator_node(state: QuizState):
    print(f"--- GENERATING (Attempt {state['attempt']}) ---")
    prompt = f"""
    You are an expert teacher. Create 15 multiple-choice questions based on the text below.
    Format strictly as a JSON list of objects.
    Each object must have: id (1-15), text, options (list of 4 strings), correct_answer (string matching one option), explanation.
    
    TEXT: {state['text_content'][:15000]}... (truncated)
    """
    
    # Instantiate the LLM at runtime (clear error if missing API key)
    llm = get_llm()
    response = llm.invoke([SystemMessage(content="JSON Output Only."), HumanMessage(content=prompt)])
    content = getattr(response, 'content', '')
    content = content.replace("```json", "").replace("```", "") if isinstance(content, str) else ''
    try:
        questions = json.loads(content)
    except Exception:
        questions = []
        
    return {"raw_questions": questions, "attempt": state["attempt"] + 1}

# --- NODE 2: VALIDATOR ---
def validator_node(state: QuizState):
    print("--- VALIDATING ---")
    questions = state["raw_questions"]
    
    # Simple heuristic validation (can be replaced with LLM critique)
    valid_q = []
    for q in questions:
        if len(q.get("options", [])) == 4 and q.get("correct_answer") in q["options"]:
            valid_q.append(q)
            
    # Select best 10
    final_selection = valid_q[:10]
    score = len(final_selection) * 10 # Mock score: 10 pts per valid question
    
    return {"validated_questions": final_selection, "quality_score": score}

# --- EDGE LOGIC ---
def should_continue(state: QuizState):
    if state["quality_score"] >= 80: # Need at least 8 valid questions
        return "end"
    if state["attempt"] > 3: # Max retries
        return "end" # Fail safe, return whatever we have
    return "generate"

# --- GRAPH CONSTRUCTION ---
workflow = StateGraph(QuizState)
workflow.add_node("generator", generator_node)
workflow.add_node("validator", validator_node)

workflow.set_entry_point("generator")
workflow.add_edge("generator", "validator")
workflow.add_conditional_edges(
    "validator",
    should_continue,
    {
        "end": END,
        "generate": "generator"
    }
)

app_workflow = workflow.compile()

async def generate_quiz_from_text(text: str):
    inputs = {
        "text_content": text, 
        "raw_questions": [], 
        "validated_questions": [], 
        "quality_score": 0, 
        "attempt": 1
    }
    result = await app_workflow.ainvoke(inputs)
    return result.get("validated_questions", [])

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, quizzes

app = FastAPI(title="PDF to Quiz Agent")

# CORS Configuration (development-friendly)
# Allow all origins for local dev; do NOT use this in production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth, prefix="/auth", tags=["Auth"])
app.include_router(quizzes, prefix="/api/quizzes", tags=["Quizzes"])

@app.get("/")
def root():
    return {"message": "API is running"}

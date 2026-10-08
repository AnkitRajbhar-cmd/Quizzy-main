# PDF-to-Quiz Agent (Monorepo) ✅

A full-stack PDF → Quiz agent built with **FastAPI** backend and **React + Vite** frontend. The app extracts text from uploaded PDFs, uses an LLM workflow (LangChain / LangGraph with Google Gemini) to generate multiple-choice questions, stores quizzes in MongoDB, and lets users take and submit quizzes.

---

## 🔧 What's included

- server/ (FastAPI)
  - app/core: configuration & security helpers (`config.py`, `security.py`)
  - app/db: MongoDB connection (`database.py`)
  - app/models: Pydantic schemas (`schemas.py`)
  - app/services: AI workflow + PDF parser (`langgraph_workflow.py`, `pdf_parser.py`)
  - app/routers: auth and quizzes endpoints (`auth.py`, `quizzes.py`)
  - main.py: FastAPI app entry
  - requirements.txt: Python dependencies

- client/ (React + Vite)
  - src/api: axios instance with interceptors
  - src/context: `AuthContext` (login/logout)
  - src/pages: `UploadQuiz`, `QuizTaker`, `Results`, `Login`, `Signup`
  - Tailwind + Vite config

- `.env.example` with recommended environment variables

---

## 🚀 Quick start (development)

### 1) Backend

1. cd server
2. python -m venv .venv
3. .venv\Scripts\activate   (Windows) or `source .venv/bin/activate` (macOS / Linux)
4. pip install -r requirements.txt
5. Copy `.env.example` → `.env` and set values (especially `MONGODB_URL` and `GOOGLE_API_KEY`)
6. Run:

   uvicorn main:app --reload --host 0.0.0.0 --port 8000

The API root will be available at http://localhost:8000

### 2) Frontend

1. cd client
2. npm install
3. npm run dev
4. Open the Vite URL (default: http://localhost:5173)

The frontend expects `VITE_API_URL` to point to the backend (default in `.env.example` is http://localhost:8000).

---

## 🔐 Authentication

- `/auth/signup` — POST `{ email, password, full_name }` to create an account
- `/auth/login` — POST `{ email, password }` (returns `access_token`)
- The client stores `token` in `localStorage` and sends Bearer token in Axios headers.

Note: A minimal OAuth2 `/auth/token` endpoint exists for form-based access but the frontend uses `/auth/login` JSON endpoint.

---

## 🧠 AI Workflow

- The LLM workflow is implemented in `server/app/services/langgraph_workflow.py` using a generator + validator graph.
- `server/app/services/pdf_parser.py` uses `pypdf` to extract text.
- The code expects a `GOOGLE_API_KEY` environment variable to use Gemini via `langchain-google-genai`.

Be aware of costs and quotas when invoking LLM APIs.

---

## 📄 API Endpoints (summary)

- POST `/auth/signup` — create user
- POST `/auth/login` — login (JSON)
- POST `/api/quizzes/generate` — upload PDF file (multipart/form-data) → returns quiz (answers stripped)
- GET `/api/quizzes/{id}` — get quiz (taker view, answers stripped)
- POST `/api/quizzes/submit/{id}` — submit answers and get result (score, percentage, analysis)

---

## ✅ Notes & next steps (suggested)

- Add a protected route HOC on the frontend to restrict pages to authenticated users.
- Add tests for backend routers and services (pytest / HTTPX & FastAPI test client).
- Add Docker and docker-compose for local dev with MongoDB and a single-command startup.
- Improve LLM prompt engineering / safety and add retry / rate-limit handling.

---


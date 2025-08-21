# Shohoj Niyog

Shohoj Niyog is an **AI–powered full-stack recruitment platform** where recruiters can create AI-generated interview sessions, invite candidates, and evaluate their responses automatically using semantic similarity scoring.

The project backend is built with **Django** + **Django REST Framework**, with **LangGraph** for agentic workflows and **HuggingFacePipeline** for AI-powered interview question generation.

---

## 🚀 Features

- **User Roles:** Recruiter & Candidate.
- **Authentication & Authorization** with JWT.
- **AI-Generated Interview Questions** using LangGraph & HuggingFace.
- **Video Answer Submission** for candidates.
- **Semantic Similarity Scoring** of candidate responses.
- **Recruiter Dashboard** to view scores and update hiring status.
- **Candidate Dashboard** to view interview statuses.

---

## 🛠️ Tech Stack

**Backend:**
- Django
- Django REST Framework
- LangGraph (Agentic workflows)
- HuggingFacePipeline (AI question generation)
- MongoDB (Data storage)

**Other Tools:**
- Llama-3.2-3B (for QA generation)
- Whisper (for video transcription)
- all-MiniLM-L6-v2 (for semantic similarity)
- JWT Authentication
---

## 📂 Project Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Anindya21/Shohoj-Niyog.git
```

### 2️⃣ Create a Virtual Environment & Activate
```bash
uv venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
uv sync
```

### 4️⃣ Set Environment Variables
Create a `.env` file in the root directory:
```env
SECRET_KEY=your_django_secret_key
DEBUG=True
mongo_uri=your_mongodb_connection_uri
HUGGINGFACE_API_KEY=your_huggingface_api_key
```

### 5️⃣ Run Database Migrations
```bash
cd backend
python manage.py migrate
```

### 6️⃣ Start the Server
```bash
python manage.py runserver
```
Backend will run at:
```
http://127.0.0.1:8000/
```

---

## 🔗 API Endpoints

### Authentication
- **Sign Up** – `POST /accounts/signup/`
- **Login** – `POST /accounts/login/`

### Recruiter
- **Create Interview Session** – `POST /api/gen/` *(Authenticated, Role: Recruiter)*
- **Get All Sessions(Recruiter/Candidate)** – `GET /api/findall/`
- **Update Hiring Status** – `PATCH /api/decide/`

### Candidate
- **Submit Video Responses** – `POST /api/response/`
- **View Interview Status** – `GET /api/results/`
- **Joining Confirmation**- `POST /api/decide`

---

## 📌 Example Flow

1. **Sign up** as Recruiter or Candidate.
2. **Recruiter logs in** and creates an interview session with position, stacks, level, allowed candidates, and number of questions.
3. **AI generates** questions and ideal answers stores them as a session.
4. **Candidates log in** and submit video answers for each question.
5. **AI transcribes and scores** answers against ideal answers.
6. **Recruiter updates hiring status** for candidates.
7. **Candidates checks and confirms hiring decision** in the dashboard.

---

## 📜 License
This project is licensed under the MIT License.



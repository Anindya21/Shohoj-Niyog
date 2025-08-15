# Shohoj Niyog

Shohoj Niyog is a **machine learning–powered full-stack recruitment platform** where recruiters can create AI-generated interview sessions, invite candidates, and evaluate their responses automatically using AI scoring.

The project backend is built with **Django** + **Django REST Framework**, with **LangGraph** for agentic workflows and **HuggingFacePipeline** for AI-powered interview question generation. The frontend (planned) will be developed with **Next.js**, **TypeScript**, and **Tailwind CSS**.

---

## 🚀 Features

- **User Roles:** Recruiter & Candidate.
- **Authentication & Authorization** with JWT.
- **AI-Generated Interview Questions** using LangGraph & HuggingFace.
- **Video Answer Submission** for candidates.
- **Automatic AI Scoring** of candidate responses.
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

**Frontend (Planned):**
- Next.js
- TypeScript
- Tailwind CSS

**Other Tools:**
- Whisper (for video transcription)
- JWT Authentication

---

## 📂 Project Setup

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Anindya21/Shohoj-Niyog.git
cd Shohoj-Niyog
```

### 2️⃣ Create a Virtual Environment & Activate
```bash
python -m venv .venv
source .venv/bin/activate   # Linux/Mac
.venv\Scripts\activate      # Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
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
- **Sign Up** – `POST /accounts/signup`
- **Login** – `POST /accounts/login`

### Recruiter
- **Create Interview Session** – `POST /api/gen` *(Authenticated, Role: Recruiter)*
- **Get All Sessions** – `GET /api/findall/`
- **Update Candidate Status** – `PATCH /api/update_status/`

### Candidate
- **Submit Video Responses** – `POST /response/`
- **View Interview Status** – `GET /status/`

---

## 📌 Example Flow

1. **Sign up** as Recruiter or Candidate.
2. **Recruiter logs in** and creates an interview session with position, stacks, level, allowed candidates, and number of questions.
3. **AI generates questions** and stores them in the session.
4. **Candidates log in** and submit video answers for each question.
5. **AI transcribes and scores** answers against ideal answers.
6. **Recruiter updates hiring status** for candidates.
7. **Candidates check their results** in the dashboard.

---

## 📜 License
This project is licensed under the MIT License.

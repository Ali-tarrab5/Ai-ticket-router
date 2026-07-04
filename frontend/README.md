# 🤖 AI Support Ticket Router (Enterprise NLP System)

An enterprise-grade, end-to-end Machine Learning pipeline that automatically classifies and routes customer support tickets using State-of-the-Art (SOTA) Contextual AI. Built with a React frontend, FastAPI backend, and an integrated Human-in-the-Loop (HITL) feedback system.

## ✨ Key Features
* **Contextual Zero-Shot Classification:** Replaced legacy TF-IDF/Naive Bayes with HuggingFace's `BART-large-mnli` model. It understands the true context of complex sentences, handling unseen vocabulary and mixed emotions effortlessly.
* **Human-in-the-Loop (HITL):** Built-in manual override feature. Human agents can correct AI predictions, updating the database in real-time to facilitate future model retraining (MLOps pipeline foundation).
* **Persistent Storage (CRUD):** Fully integrated SQLite database via SQLAlchemy to store tickets, confidence scores, and correction statuses permanently.
* **Optimized Local Storage:** Configured `HF_HOME` environment variables to download large transformer models to a secondary drive (D:/), saving critical C:/ drive space.
* **Modern UI:** Responsive, clean React dashboard with live API polling and intuitive state management.

## 🛠️ Technology Stack
* **Frontend:** React.js, Vite, Axios
* **Backend:** Python, FastAPI, Uvicorn, SQLAlchemy
* **AI/NLP Engine:** HuggingFace Transformers (`facebook/bart-large-mnli`), PyTorch
* **Database:** SQLite

## 🚀 Installation & Setup

### 1. Backend Setup (FastAPI + AI)
Navigate to your main project directory, create a virtual environment, and install the required dependencies.

```bash
# Create and activate virtual environment
python -m venv venv
source venv/Scripts/activate  # (For Windows)

# Install required packages
pip install fastapi uvicorn sqlalchemy transformers torch pydantic


## backend :
uvicorn main:app --reload


## frontend:
npm run dev

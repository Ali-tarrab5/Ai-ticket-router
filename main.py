import os
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session
import requests # Naya: API calls karne ke liye

from database import SessionLocal, TicketRecord

app = FastAPI(title="AI Ticket Routing API with Cloud AI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🔴 HUGGINGFACE CLOUD API SETUP
HF_API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

HF_TOKEN = os.getenv("HF_TOKEN")
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

DEPARTMENTS = ["Technical Support", "Billing", "Refunds", "General Inquiry"]

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class TicketInput(BaseModel):
    text: str

class FeedbackInput(BaseModel):
    ticket_id: int
    corrected_department: str

@app.get("/")
def home():
    return {"message": "Cloud-Ready Enterprise API is running successfully!"}

@app.post("/predict")
def route_ticket(ticket: TicketInput, db: Session = Depends(get_db)):
    
    # 1. Cloud AI se API ke zariye prediction mangwana
    payload = {
        "inputs": ticket.text,
        "parameters": {"candidate_labels": DEPARTMENTS}
    }
    
    response = requests.post(HF_API_URL, headers=headers, json=payload)
    ai_result = response.json()
    
    # Agar model internet par sleep mode mein ho toh shuru mein error aa sakta hai
    if "error" in ai_result:
        return {"error": "AI Model is waking up, please try again in 20 seconds!"}
        
    prediction = ai_result['labels'][0]
    confidence_score = ai_result['scores'][0] * 100
    
    # 2. Database mein Save karna
    db_ticket = TicketRecord(
        text=ticket.text,
        predicted_department=prediction,
        actual_department=prediction, 
        confidence_score=round(confidence_score, 2)
    )
    db.add(db_ticket)
    db.commit()
    db.refresh(db_ticket)
    
    return {
        "ticket_id": db_ticket.id,
        "original_text": ticket.text,
        "routed_department": prediction,
        "confidence_score": f"{round(confidence_score, 2)}%"
    }

@app.post("/feedback")
def save_feedback(feedback: FeedbackInput, db: Session = Depends(get_db)):
    ticket = db.query(TicketRecord).filter(TicketRecord.id == feedback.ticket_id).first()
    if ticket:
        ticket.actual_department = feedback.corrected_department
        ticket.is_corrected = True
        ticket.confidence_score = 100.0
        db.commit()
        return {"message": "Feedback saved successfully!"}
    return {"error": "Ticket not found"}

@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int, db: Session = Depends(get_db)):
    ticket = db.query(TicketRecord).filter(TicketRecord.id == ticket_id).first()
    if ticket:
        db.delete(ticket)
        db.commit()
        return {"message": f"Ticket #{ticket_id} permanently deleted!"}
    return {"error": "Ticket not found"}
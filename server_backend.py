from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import joblib

model = joblib.load("phishing_model.pkl")

app = FastAPI()

class EmailRequest(BaseModel):
    content: str

app.post("/check-email")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_headers=["*"],
)

async def analyze_email(request: EmailRequest):
    print(f"Received data: {request.content[:50]}...")

##################################################
## @brief     Analyze email content to determine if it's phishing or ham.
## @in   request EmailRequest
## @out  dict
##################################################
async def analyze_email(request: EmailRequest):
    if not request.content:
        raise HTTPException(status_code=400, detail="No content provided")
    
    prediction = model.predict([request.content])[0]
    
    probs = model.predict_proba([request.content])[0]
    confidence = float(max(probs))

    return {
        "label": str(prediction),
        "confidence": confidence,
        "is_phishing": True if str(prediction).lower() == 'phishing' else False
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
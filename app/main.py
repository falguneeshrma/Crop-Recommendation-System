import os
import sys
from dotenv import load_dotenv

load_dotenv()

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)

from rag_chain import CropRAGAssistant

MODEL_PATH = os.path.join(ROOT, "models", "crop_model.joblib")
FEATURES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]

app = FastAPI(title="Crop Recommendation + RAG Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# model + RAG chain are both a bit slow to load, so only do it once, on first use
model = None
assistant = None


def get_model():
    global model
    if model is None:
        if not os.path.exists(MODEL_PATH):
            raise HTTPException(500, "no trained model found, run train_model.py first")
        model = joblib.load(MODEL_PATH)
    return model


def get_assistant():
    global assistant
    if assistant is None:
        try:
            assistant = CropRAGAssistant()
        except (ValueError, FileNotFoundError) as e:
            raise HTTPException(500, str(e))
    return assistant


class SoilInput(BaseModel):
    N: float = Field(..., description="Nitrogen (kg/ha)")
    P: float = Field(..., description="Phosphorus (kg/ha)")
    K: float = Field(..., description="Potassium (kg/ha)")
    temperature: float = Field(..., description="Temperature (°C)")
    humidity: float = Field(..., description="Relative humidity (%)")
    ph: float = Field(..., description="Soil pH")
    rainfall: float = Field(..., description="Rainfall (mm)")


class AskRequest(BaseModel):
    question: str
    crop: str | None = Field(None, description="crop name to focus the answer on, optional")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/predict")
def predict(payload: SoilInput):
    clf = get_model()
    row = pd.DataFrame([[getattr(payload, f) for f in FEATURES]], columns=FEATURES)
    crop = clf.predict(row)[0]
    proba = clf.predict_proba(row)[0]
    confidence = float(max(proba))
    return {"crop": crop, "confidence": round(confidence, 3)}


@app.post("/predict-and-explain")
def predict_and_explain(payload: SoilInput):
    pred = predict(payload)
    bot = get_assistant()
    explanation = bot.explain_recommendation(pred["crop"], payload.model_dump())
    return {**pred, "explanation": explanation}


@app.post("/ask")
def ask(payload: AskRequest):
    bot = get_assistant()
    return bot.ask(payload.question, crop=payload.crop)


# serve the frontend (static/index.html + assets) from the same server so
# there's only one thing to run for the demo
app.mount("/static", StaticFiles(directory=os.path.join(HERE, "static")), name="static")


@app.get("/")
def index():
    return FileResponse(os.path.join(HERE, "static", "index.html"))

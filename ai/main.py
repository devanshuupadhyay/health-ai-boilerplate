# ai/main.py
from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI(title="Health AI Service")

# Initialize the summarizer when the application starts
# This will download the model on the first run
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")


class SummarizationRequest(BaseModel):
    text: str


class SummarizationResponse(BaseModel):
    summary: str


@app.post("/summarize", response_model=SummarizationResponse)
def summarize_text(request: SummarizationRequest):
    """
    Generates a summary for the given text.
    """
    if not request.text:
        return {"summary": ""}

    summary_result = summarizer(
        request.text, max_length=150, min_length=30, do_sample=False
    )
    return {"summary": summary_result[0]["summary_text"]}


@app.get("/health")
def health_check():
    return {"status": "ok"}

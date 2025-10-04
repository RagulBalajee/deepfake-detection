from fastapi import FastAPI, UploadFile, Form
from models.fake_news import detect_fake_news
from models.deepfake_img import detect_image_fake
from models.deepfake_vid import detect_video_fake
from models.deepfake_audio import detect_audio_fake
from utils.existence import verify_existence
from utils.explainable import explain_result

import uvicorn

app = FastAPI(title="Fake News & Deepfake Detection")

@app.post("/analyze_text/")
async def analyze_text(text: str = Form(...), lang: str = Form("en")):
    fake_score = detect_fake_news(text, lang)
    existence = verify_existence(text)
    explanation = explain_result("text", fake_score)
    return {
        "input": text,
        "fake_score": fake_score,
        "existence": existence,
        "explanation": explanation
    }

@app.post("/analyze_image/")
async def analyze_image(file: UploadFile):
    result = await detect_image_fake(file)
    explanation = explain_result("image", result["score"])
    return {**result, "explanation": explanation}

@app.post("/analyze_video/")
async def analyze_video(file: UploadFile):
    result = await detect_video_fake(file)
    explanation = explain_result("video", result["score"])
    return {**result, "explanation": explanation}

@app.post("/analyze_audio/")
async def analyze_audio(file: UploadFile):
    result = await detect_audio_fake(file)
    explanation = explain_result("audio", result["score"])
    return {**result, "explanation": explanation}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

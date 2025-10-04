from fastapi import FastAPI, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.models.fake_news import detect_fake_news
from backend.models.deepfake_img import detect_image_fake
from backend.models.deepfake_vid import detect_video_fake
from backend.models.deepfake_audio import detect_audio_fake
from utils.existence import verify_existence
from utils.explainable_enhanced import explain_result
from utils.cultural_context import analyze_cultural_context
from utils.credibility import calculate_credibility_score
from utils.psychological import detect_psychological_impact
from utils.traceability import track_content_spread
from utils.blockchain import store_content_hash, verify_content_hash
from utils.reporting import submit_user_report, get_community_reports
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
import asyncio
import json
from datetime import datetime

app = FastAPI(
    title="Fake News & Deepfake Detection System",
    description="Advanced AI-powered platform for detecting fake news and deepfake content with innovative verification features",
    version="2.0.0"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Pydantic models for request/response
class AnalysisRequest(BaseModel):
    content: str
    content_type: str  # "text", "image", "video", "audio"
    language: Optional[str] = "en"
    source_url: Optional[str] = None
    user_context: Optional[Dict[str, Any]] = None

class AnalysisResponse(BaseModel):
    content_id: str
    analysis_type: str
    fake_score: float
    confidence: float
    explanation: Dict[str, Any]
    credibility_score: Optional[float] = None
    cultural_context: Optional[Dict[str, Any]] = None
    psychological_impact: Optional[Dict[str, Any]] = None
    existence_verification: Optional[Dict[str, Any]] = None
    blockchain_hash: Optional[str] = None
    traceability: Optional[Dict[str, Any]] = None
    timestamp: datetime

# Enhanced API endpoints with all innovative features

@app.post("/analyze/", response_model=AnalysisResponse)
async def comprehensive_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Comprehensive analysis endpoint with all innovative features
    """
    try:
        content_id = f"content_{datetime.now().timestamp()}"
        
        # Core detection based on content type
        if request.content_type == "text":
            fake_result = detect_fake_news(request.content, request.language)
            fake_score = fake_result.get("score", 0.0)
        else:
            # For media files, we'll need to implement file handling
            fake_score = 0.5  # Placeholder
        
        # Run all innovative features in parallel
        tasks = []
        
        # Existence verification
        tasks.append(verify_existence(request.content))
        
        # Cultural context analysis
        tasks.append(analyze_cultural_context(request.content, request.language))
        
        # Credibility scoring
        tasks.append(calculate_credibility_score(request.source_url))
        
        # Psychological impact detection
        tasks.append(detect_psychological_impact(request.content))
        
        # Blockchain hash storage
        blockchain_hash = await store_content_hash(request.content, content_id)
        
        # Traceability tracking
        traceability = await track_content_spread(request.content, request.source_url)
        
        # Wait for all tasks to complete
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        existence_verification = results[0] if not isinstance(results[0], Exception) else None
        cultural_context = results[1] if not isinstance(results[1], Exception) else None
        credibility_score = results[2] if not isinstance(results[2], Exception) else None
        psychological_impact = results[3] if not isinstance(results[3], Exception) else None
        
        # Generate comprehensive explanation
        explanation = explain_result(
            request.content_type, 
            fake_score, 
            existence_verification,
            cultural_context,
            psychological_impact
        )
        
        # Background task for community reporting
        background_tasks.add_task(update_community_reports, content_id, fake_score)
        
        return AnalysisResponse(
            content_id=content_id,
            analysis_type=request.content_type,
            fake_score=fake_score,
            confidence=calculate_confidence(fake_score, existence_verification, credibility_score),
            explanation=explanation,
            credibility_score=credibility_score,
            cultural_context=cultural_context,
            psychological_impact=psychological_impact,
            existence_verification=existence_verification,
            blockchain_hash=blockchain_hash,
            traceability=traceability,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/analyze_text/")
async def analyze_text(text: str = Form(...), lang: str = Form("en"), source_url: str = Form(None)):
    """Legacy endpoint for backward compatibility"""
    request = AnalysisRequest(
        content=text,
        content_type="text",
        language=lang,
        source_url=source_url
    )
    return await comprehensive_analysis(request, BackgroundTasks())

@app.post("/analyze_image/")
async def analyze_image(file: UploadFile, source_url: str = Form(None)):
    """Enhanced image analysis with all features"""
    result = await detect_image_fake(file)
    
    # Read file content for comprehensive analysis
    content = await file.read()
    request = AnalysisRequest(
        content=content.decode('utf-8', errors='ignore'),
        content_type="image",
        source_url=source_url
    )
    
    # Get comprehensive analysis
    analysis = await comprehensive_analysis(request, BackgroundTasks())
    analysis.fake_score = result["score"]
    
    return analysis

@app.post("/analyze_video/")
async def analyze_video(file: UploadFile, source_url: str = Form(None)):
    """Enhanced video analysis with all features"""
    result = await detect_video_fake(file)
    
    # Read file content for comprehensive analysis
    content = await file.read()
    request = AnalysisRequest(
        content=content.decode('utf-8', errors='ignore'),
        content_type="video",
        source_url=source_url
    )
    
    # Get comprehensive analysis
    analysis = await comprehensive_analysis(request, BackgroundTasks())
    analysis.fake_score = result["score"]
    
    return analysis

@app.post("/analyze_audio/")
async def analyze_audio(file: UploadFile, source_url: str = Form(None)):
    """Enhanced audio analysis with all features"""
    result = await detect_audio_fake(file)
    
    # Read file content for comprehensive analysis
    content = await file.read()
    request = AnalysisRequest(
        content=content.decode('utf-8', errors='ignore'),
        content_type="audio",
        source_url=source_url
    )
    
    # Get comprehensive analysis
    analysis = await comprehensive_analysis(request, BackgroundTasks())
    analysis.fake_score = result["score"]
    
    return analysis

# New innovative endpoints

@app.post("/report/")
async def submit_report(content_id: str, report_type: str, description: str, user_id: str = None):
    """Submit user report for suspicious content"""
    return await submit_user_report(content_id, report_type, description, user_id)

@app.get("/reports/{content_id}")
async def get_reports(content_id: str):
    """Get community reports for specific content"""
    return await get_community_reports(content_id)

@app.get("/traceability/{content_id}")
async def get_traceability(content_id: str):
    """Get content spread traceability map"""
    return await track_content_spread(None, None, content_id)

@app.get("/credibility/{source_url}")
async def get_credibility(source_url: str):
    """Get source credibility score"""
    return await calculate_credibility_score(source_url)

@app.get("/dashboard/")
async def get_dashboard():
    """Get system dashboard with statistics"""
    return {
        "total_analyses": 0,  # Implement with database
        "fake_detection_rate": 0.15,
        "community_reports": 0,
        "verified_sources": 0,
        "blockchain_verifications": 0
    }

# Helper functions
def calculate_confidence(fake_score, existence_verification, credibility_score):
    """Calculate overall confidence score"""
    base_confidence = abs(fake_score - 0.5) * 2  # Convert to 0-1 scale
    
    if existence_verification and existence_verification.get("exists"):
        base_confidence += 0.2
    
    if credibility_score and credibility_score > 0.7:
        base_confidence += 0.1
    
    return min(base_confidence, 1.0)

async def update_community_reports(content_id: str, fake_score: float):
    """Update community reports in background"""
    # Implement database update
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

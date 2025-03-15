from fastapi import APIRouter, Depends, HTTPException
from app.models.acceleration import AccelerationData
from app.models.analysis import AnalysisRequest, AnalysisResponse
from app.services.analysis import AnalysisService

router = APIRouter()
analysis_service = AnalysisService()


@router.post("/analyze", response_model=AnalysisResponse)
async def analyze_data(request: AnalysisRequest):
    """Analyze accelerometer data and return insights and recommendations."""
    try:
        response = analysis_service.analyze(request)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error analyzing data: {str(e)}")

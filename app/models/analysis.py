from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.acceleration import AccelerationData, ActivityMetrics


class Insight(BaseModel):
    """Model for an insight generated from activity data."""

    id: Optional[str] = None
    insight_type: str
    message: str
    priority: str  # 'high', 'medium', or 'low'


class Recommendation(BaseModel):
    """Model for a recommendation generated from activity data."""

    id: Optional[str] = None
    recommendation_type: str
    title: str
    message: str
    priority: str  # 'high', 'medium', or 'low'


class AnalysisRequest(BaseModel):
    """Model for a request to analyze accelerometer data."""

    acceleration_data: AccelerationData
    include_insights: bool = True
    include_recommendations: bool = True
    user_id: str


class AnalysisResponse(BaseModel):
    """Model for a response containing analysis results."""

    status: str
    message: Optional[str] = None
    insights: List[Insight] = []
    recommendations: List[Recommendation] = []
    metrics: Optional[ActivityMetrics] = None

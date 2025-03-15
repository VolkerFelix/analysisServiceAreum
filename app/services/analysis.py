from app.models.analysis import AnalysisRequest, AnalysisResponse
from app.models.acceleration import ActivityMetrics
from app.utils.metrics import calculate_activity_metrics
from app.utils.patterns import detect_activity_patterns
from app.services.insights import generate_insights, generate_recommendations


class AnalysisService:
    """Service for analyzing accelerometer data."""

    def analyze(self, request: AnalysisRequest) -> AnalysisResponse:
        """Analyze accelerometer data and generate insights and recommendations."""

        # Calculate metrics
        metrics = calculate_activity_metrics(request.acceleration_data)

        # Detect patterns
        patterns = detect_activity_patterns(request.acceleration_data)

        # Initialize response
        response = AnalysisResponse(status="success", metrics=metrics)

        # Generate insights if requested
        if request.include_insights:
            response.insights = generate_insights(metrics, patterns)

        # Generate recommendations if requested
        if request.include_recommendations:
            response.recommendations = generate_recommendations(metrics, patterns)

        return response

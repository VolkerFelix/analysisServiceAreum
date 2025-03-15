import pytest

from app.models.analysis import AnalysisRequest
from app.services.analysis import AnalysisService


@pytest.fixture
def analysis_service():
    """Create an instance of the analysis service for testing."""
    return AnalysisService()


def test_analyze_with_insights_and_recommendations(
    analysis_service, sample_acceleration_data
):
    """Test that the analyze method returns insights and recommendations when requested."""
    # Create request
    request = AnalysisRequest(
        acceleration_data=sample_acceleration_data,
        include_insights=True,
        include_recommendations=True,
        user_id="test-user-1",
    )

    # Call the service
    response = analysis_service.analyze(request)

    # Verify response
    assert response.status == "success"
    assert response.metrics is not None
    assert len(response.insights) > 0
    assert len(response.recommendations) > 0


def test_analyze_without_insights_and_recommendations(
    analysis_service, sample_acceleration_data
):
    """Test that the analyze method doesn't return insights or recommendations when not requested."""
    # Create request
    request = AnalysisRequest(
        acceleration_data=sample_acceleration_data,
        include_insights=False,
        include_recommendations=False,
        user_id="test-user-1",
    )

    # Call the service
    response = analysis_service.analyze(request)

    # Verify response
    assert response.status == "success"
    assert response.metrics is not None
    assert len(response.insights) == 0
    assert len(response.recommendations) == 0


def test_analyze_with_active_data(analysis_service, sample_active_acceleration_data):
    """Test that the analyze method correctly identifies high activity."""
    # Create request
    request = AnalysisRequest(
        acceleration_data=sample_active_acceleration_data,
        include_insights=True,
        include_recommendations=True,
        user_id="test-user-1",
    )

    # Call the service
    response = analysis_service.analyze(request)

    # Verify metrics
    assert response.metrics is not None
    assert response.metrics.avg_intensity > 0.3  # Should detect above-average activity

    # Check for activity-related insights
    activity_insights = [
        i for i in response.insights if i.insight_type == "activity_level"
    ]
    assert len(activity_insights) > 0


def test_analyze_with_inactive_data(
    analysis_service, sample_inactive_acceleration_data
):
    """Test that the analyze method correctly identifies inactivity periods."""
    # Create request
    request = AnalysisRequest(
        acceleration_data=sample_inactive_acceleration_data,
        include_insights=True,
        include_recommendations=True,
        user_id="test-user-1",
    )

    # Call the service
    response = analysis_service.analyze(request)

    # Verify inactivity detection
    inactivity_insights = [
        i for i in response.insights if i.insight_type == "inactivity"
    ]
    assert len(inactivity_insights) > 0

    # Check for inactivity recommendations
    inactivity_recommendations = [
        r for r in response.recommendations if r.recommendation_type == "inactivity"
    ]
    assert len(inactivity_recommendations) > 0

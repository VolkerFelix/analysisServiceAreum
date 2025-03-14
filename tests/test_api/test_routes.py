import json
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.models.analysis import AnalysisRequest


client = TestClient(app)


def test_health_check():
    """Test that the health check endpoint returns successfully."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_analyze_endpoint(sample_acceleration_data):
    """Test that the analyze endpoint processes data correctly."""
    # Create a valid request
    request = AnalysisRequest(
        acceleration_data=sample_acceleration_data,
        include_insights=True,
        include_recommendations=True,
        user_id="test-user-1"
    )
    # First convert to JSON string, then parse back to dictionary
    json_str = request.json()
    json_dict = json.loads(json_str)
    
    # Call the endpoint
    response = client.post("/analyze", json=json_dict)
    
    # Check response
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "success"
    assert "metrics" in data
    assert isinstance(data["insights"], list)
    assert isinstance(data["recommendations"], list)


def test_analyze_endpoint_invalid_data():
    """Test that the analyze endpoint handles invalid data gracefully."""
    # Missing required fields
    invalid_request = {
        "acceleration_data": {
            # Missing required fields
        },
        "user_id": "test-user-1"
    }
    
    response = client.post("/analyze", json=invalid_request)
    
    # Should return a validation error
    assert response.status_code == 422  # Unprocessable Entity
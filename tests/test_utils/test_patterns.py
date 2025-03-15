import pytest
from datetime import datetime, timedelta
import numpy as np

from app.models.acceleration import AccelerationData, AccelerationSample
from app.utils.patterns import detect_activity_patterns


def test_detect_activity_patterns_empty_data():
    """Test that the function handles empty data gracefully."""
    # Create empty acceleration data
    empty_data = AccelerationData(
        data_type="acceleration",
        device_info={},
        sampling_rate_hz=10,
        start_time=datetime.utcnow(),
        samples=[],
        id="empty-data",
    )

    # Detect patterns
    patterns = detect_activity_patterns(empty_data)

    # Verify empty result
    assert len(patterns.inactivity_periods) == 0
    assert len(patterns.activity_patterns) == 0


def test_detect_activity_patterns_no_inactivity():
    """Test that the function correctly detects no inactivity in active data."""
    # Create very active data
    base_time = datetime.utcnow()
    samples = []

    for i in range(100):
        # Add significant movement
        x = 0.8 * np.sin(i * 0.1)  # Large x movement
        y = 0.7 * np.cos(i * 0.1)  # Large y movement
        z = 0.6 + 0.5 * np.sin(i * 0.05)  # Varying z

        sample_time = base_time + timedelta(milliseconds=i * 100)

        samples.append(AccelerationSample(timestamp=sample_time, x=x, y=y, z=z))

    active_data = AccelerationData(
        data_type="acceleration",
        device_info={"device": "test", "model": "unit-test"},
        sampling_rate_hz=10,
        start_time=base_time,
        samples=samples,
        id="active-data",
    )

    # Detect patterns
    patterns = detect_activity_patterns(active_data)

    # Verify no inactivity
    assert len(patterns.inactivity_periods) == 0


def test_detect_activity_patterns_with_inactivity(sample_inactive_acceleration_data):
    """Test that the function correctly detects inactivity periods."""
    # Detect patterns
    patterns = detect_activity_patterns(sample_inactive_acceleration_data)

    # Verify inactivity periods
    assert len(patterns.inactivity_periods) > 0

    # Verify period properties
    for period in patterns.inactivity_periods:
        assert period.start_time < period.end_time  # Valid time range
        assert period.duration > 0  # Positive duration
        assert isinstance(period.duration, float)  # Duration is a float

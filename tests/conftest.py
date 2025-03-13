import pytest
from datetime import datetime, timedelta
from typing import List

from app.models.acceleration import AccelerationData, AccelerationSample


@pytest.fixture
def sample_acceleration_data() -> AccelerationData:
    """Create sample acceleration data for testing."""
    # Create 100 samples at 10Hz (10 seconds of data)
    base_time = datetime.utcnow()
    samples = []
    
    for i in range(100):
        # Add some variation to make it realistic
        x = 0.1 * (i % 5)  # Small x movement
        y = 0.2 * ((i // 10) % 3)  # Small y movement
        z = 0.9 + 0.05 * (i % 7)  # Mostly gravity with small variations
        
        sample_time = base_time + timedelta(milliseconds=i*100)  # 100ms intervals (10Hz)
        
        samples.append(
            AccelerationSample(
                timestamp=sample_time,
                x=x,
                y=y,
                z=z
            )
        )
    
    return AccelerationData(
        data_type="acceleration",
        device_info={"device": "test", "model": "unit-test"},
        sampling_rate_hz=10,
        start_time=base_time,
        samples=samples,
        id="test-data-1"
    )


@pytest.fixture
def sample_active_acceleration_data() -> AccelerationData:
    """Create sample acceleration data with high activity for testing."""
    base_time = datetime.utcnow()
    samples = []
    
    for i in range(100):
        # Add significant movement
        x = 0.5 * np.sin(i * 0.1)  # Oscillating x movement
        y = 0.4 * np.cos(i * 0.1)  # Oscillating y movement
        z = 0.8 + 0.3 * np.sin(i * 0.05)  # Varying z with gravity
        
        sample_time = base_time + timedelta(milliseconds=i*100)
        
        samples.append(
            AccelerationSample(
                timestamp=sample_time,
                x=x,
                y=y,
                z=z
            )
        )
    
    return AccelerationData(
        data_type="acceleration",
        device_info={"device": "test", "model": "unit-test"},
        sampling_rate_hz=10,
        start_time=base_time,
        samples=samples,
        id="test-data-2"
    )


@pytest.fixture
def sample_inactive_acceleration_data() -> AccelerationData:
    """Create sample acceleration data with long inactive periods for testing."""
    base_time = datetime.utcnow()
    samples = []
    
    for i in range(100):
        # Mostly inactive with some small movements
        if i < 30 or (i > 60 and i < 90):
            # Inactive periods
            x = 0.01 * np.sin(i * 0.1)
            y = 0.01 * np.cos(i * 0.1)
            z = 1.0 + 0.01 * np.sin(i * 0.05)
        else:
            # Some activity
            x = 0.3 * np.sin(i * 0.1)
            y = 0.2 * np.cos(i * 0.1)
            z = 0.9 + 0.1 * np.sin(i * 0.05)
        
        sample_time = base_time + timedelta(milliseconds=i*100)
        
        samples.append(
            AccelerationSample(
                timestamp=sample_time,
                x=x,
                y=y,
                z=z
            )
        )
    
    return AccelerationData(
        data_type="acceleration",
        device_info={"device": "test", "model": "unit-test"},
        sampling_rate_hz=10,
        start_time=base_time,
        samples=samples,
        id="test-data-3"
    )
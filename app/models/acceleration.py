from datetime import datetime
from typing import List, Dict, Optional, Any
from uuid import UUID

from pydantic import BaseModel


class AccelerationSample(BaseModel):
    """Model for a single accelerometer data sample."""

    timestamp: datetime
    x: float
    y: float
    z: float


class AccelerationData(BaseModel):
    """Model for a collection of accelerometer data samples."""

    data_type: str
    device_info: Dict[str, Any]
    sampling_rate_hz: int
    start_time: datetime
    samples: List[AccelerationSample]
    metadata: Optional[Dict[str, Any]] = None
    id: Optional[str] = None


class ActivityMetrics(BaseModel):
    """Model for activity metrics calculated from accelerometer data."""

    avg_intensity: float
    peak_intensity: float
    movement_consistency: float
    active_minutes: float
    total_duration: float


class InactivityPeriod(BaseModel):
    """Model for a period of inactivity detected in accelerometer data."""

    start_time: datetime
    end_time: datetime
    duration: float  # in seconds


class ActivityPatterns(BaseModel):
    """Model for activity patterns detected in accelerometer data."""

    inactivity_periods: List[InactivityPeriod]
    activity_patterns: List[str] = []

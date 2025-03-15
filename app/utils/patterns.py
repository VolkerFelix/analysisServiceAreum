import numpy as np
import pandas as pd
from datetime import datetime

from app.models.acceleration import AccelerationData, ActivityPatterns, InactivityPeriod


def detect_activity_patterns(data: AccelerationData) -> ActivityPatterns:
    """Detect patterns in accelerometer data like periods of inactivity."""
    samples = data.samples

    if len(samples) < 10:
        return ActivityPatterns(inactivity_periods=[])

    # Convert to DataFrame
    df = pd.DataFrame(
        [
            {
                "timestamp": s.timestamp,
                "x": s.x,
                "y": s.y,
                "z": s.z,
            }
            for s in samples
        ]
    )

    # Calculate magnitude
    df["magnitude"] = np.sqrt(df["x"] ** 2 + df["y"] ** 2 + df["z"] ** 2)

    # Gravity offset
    gravity_offset = 1.0

    # Normalize magnitude
    df["normalized_magnitude"] = (df["magnitude"] - gravity_offset).abs()

    # Threshold for inactivity
    inactivity_threshold = 0.1

    # Mark inactive samples
    df["inactive"] = df["normalized_magnitude"] < inactivity_threshold

    # Detect periods of inactivity (state changes)
    df["state_change"] = df["inactive"].ne(df["inactive"].shift(1)).cumsum()
    inactive_groups = df[df["inactive"] == True].groupby("state_change")

    # Minimum duration for an inactivity period (in samples)
    min_samples = min(20, len(df) // 5)  # Adjust based on data length

    # Extract inactivity periods
    inactivity_periods = []

    for _, group in inactive_groups:
        if len(group) >= min_samples:
            start_time = group["timestamp"].min()
            end_time = group["timestamp"].max()
            duration = (end_time - start_time).total_seconds()

            inactivity_periods.append(
                InactivityPeriod(
                    start_time=start_time, end_time=end_time, duration=duration
                )
            )

    return ActivityPatterns(inactivity_periods=inactivity_periods)

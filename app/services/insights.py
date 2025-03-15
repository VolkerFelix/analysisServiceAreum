from typing import List
from uuid import uuid4

from app.models.acceleration import ActivityMetrics, ActivityPatterns
from app.models.analysis import Insight, Recommendation


def generate_insights(
    metrics: ActivityMetrics, patterns: ActivityPatterns
) -> List[Insight]:
    """Generate insights based on activity metrics and patterns."""
    insights = []

    # Activity level insights
    if metrics.avg_intensity < 0.2:
        insights.append(
            Insight(
                insight_type="activity_level",
                message="Your activity level has been quite low during this session. Adding more movement to your day can boost your energy levels.",
                priority="medium",
            )
        )
    elif metrics.avg_intensity > 0.7:
        insights.append(
            Insight(
                insight_type="activity_level",
                message="Great job! You had high activity levels during this session.",
                priority="high",
            )
        )
    elif metrics.avg_intensity > 0.3:
        insights.append(
            Insight(
                insight_type="activity_level",
                message="You had a good level of activity during this session.",
                priority="medium",
            )
        )
    else:
        # Add a default insight for any activity level not covered above
        insights.append(
            Insight(
                insight_type="activity_level",
                message="I've analyzed your movement patterns. Consider adding more varied movements to your routine.",
                priority="low",
            )
        )

    # Inactivity insights
    if patterns.inactivity_periods:
        insights.append(
            Insight(
                insight_type="inactivity",
                message=f"I noticed {len(patterns.inactivity_periods)} periods of inactivity. Taking movement breaks can help maintain your energy and focus.",
                priority="high" if len(patterns.inactivity_periods) > 3 else "medium",
            )
        )

    # Movement consistency insights
    if metrics.movement_consistency > 0.7 and metrics.total_duration > 5.0:
        insights.append(
            Insight(
                insight_type="consistency",
                message="Your movement was very consistent during this session. This is great for maintaining steady energy.",
                priority="medium",
            )
        )
    elif metrics.movement_consistency < 0.3 and metrics.total_duration > 5.0:
        insights.append(
            Insight(
                insight_type="consistency",
                message="Your movement patterns showed high variability. This could indicate sporadic activity.",
                priority="low",
            )
        )

    # Add IDs to insights
    for insight in insights:
        insight.id = str(uuid4())

    return insights


def generate_recommendations(
    metrics: ActivityMetrics, patterns: ActivityPatterns
) -> List[Recommendation]:
    """Generate recommendations based on activity metrics and patterns."""
    recommendations = []

    # Activity level recommendations
    if metrics.avg_intensity < 0.2:
        recommendations.append(
            Recommendation(
                recommendation_type="activity_level",
                title="Increase Your Movement",
                message="Try to incorporate more movement throughout your day. Even small actions like standing up and stretching can make a difference.",
                priority="high",
            )
        )
    elif metrics.avg_intensity > 0.7:
        recommendations.append(
            Recommendation(
                recommendation_type="activity_level",
                title="Great Activity Level",
                message="You're maintaining a good activity level. Keep up the great work!",
                priority="low",
            )
        )
    else:
        # Add a default recommendation if no activity level triggers
        recommendations.append(
            Recommendation(
                recommendation_type="activity_level",
                title="Optimize Your Movement Patterns",
                message="Consider adding variety to your movement patterns for better overall health.",
                priority="medium",
            )
        )

    # Inactivity recommendations
    if patterns.inactivity_periods:
        recommendations.append(
            Recommendation(
                recommendation_type="inactivity",
                title="Break Up Sitting Periods",
                message="I noticed periods of inactivity. Try setting a timer to remind you to move every 30 minutes.",
                priority="high",
            )
        )

    # Consistency recommendations
    if metrics.movement_consistency < 0.3 and metrics.total_duration > 5.0:
        recommendations.append(
            Recommendation(
                recommendation_type="consistency",
                title="Find Steady Rhythms",
                message="Your movement patterns show high variability. Finding more consistent, rhythmic movements might help you maintain energy throughout the day.",
                priority="medium",
            )
        )

    # Daily activity goals
    if metrics.active_minutes < 5.0 and metrics.total_duration > 10.0:
        recommendations.append(
            Recommendation(
                recommendation_type="daily_goal",
                title="Set a Small Movement Goal",
                message="Try to include at least 10 minutes of active movement in your next session.",
                priority="medium",
            )
        )
    elif metrics.active_minutes > 20.0:
        recommendations.append(
            Recommendation(
                recommendation_type="daily_goal",
                title="You're Meeting Activity Goals",
                message="You've reached over 20 minutes of active movement. Keep maintaining this healthy pattern!",
                priority="low",
            )
        )

    # Add IDs to recommendations
    for recommendation in recommendations:
        recommendation.id = str(uuid4())

    return recommendations

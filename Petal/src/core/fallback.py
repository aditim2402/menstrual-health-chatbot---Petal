# src/core/fallback.py

def fallback_response(query: str) -> str:
    """
    Return a default fallback response when other systems fail or return low-confidence answers.
    """
    return (
        "Hey there! I'm here to help with menstrual health questions! What's on your mind today?"
    )

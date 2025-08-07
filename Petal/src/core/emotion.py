def detect_emotion(text):
    text = text.lower()

    # Menstrual-linked emotional triggers
    if "anxious" in text and "period" in text:
        return "pms_anxiety"
    if "anxious" in text and ("cramp" in text or "bloating" in text or "cycle" in text):
        return "pms_anxiety"

    # Emotion keywords
    sad_keywords = ["sad", "pain", "tired", "bad", "cramp", "hurt", "depressed", "moody", "bloated", "fatigue"]
    happy_keywords = ["happy", "joy", "great", "good", "relieved", "calm"]
    angry_keywords = ["angry", "frustrated", "annoyed", "irritated"]
    confused_keywords = ["confused", "unsure", "don't know", "uncertain", "lost"]

    if any(w in text for w in angry_keywords):
        return "angry"
    if any(w in text for w in sad_keywords):
        return "sad"
    if any(w in text for w in confused_keywords):
        return "confused"
    if any(w in text for w in happy_keywords):
        return "happy"

    return "neutral"


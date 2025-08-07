# src/graph/graph_config.py - Enhanced for comprehensive coverage

# Enhanced graph structure covering ALL menstrual health topics
graph = {
    # Period Basics
    "period_basics": ["cycle_length", "period_duration", "cycle_phases", "symptoms", "irregularities"],
    "cycle_length": ["period_basics", "irregularities", "fertility"],
    "period_duration": ["period_basics", "symptoms", "lifestyle"],
    "cycle_phases": ["period_basics", "fertility", "hormones"],
    
    # Symptoms & Discomfort
    "symptoms": ["cramps", "bloating", "fatigue", "mood_changes", "treatment"],
    "cramps": ["treatment", "exercise", "nutrition", "hot_compress"],
    "bloating": ["nutrition", "hydration", "lifestyle", "hormones"],
    "fatigue": ["nutrition", "sleep", "exercise", "iron_deficiency"],
    "mood_changes": ["emotional", "pms", "pmdd", "hormones"],
    "heavy_bleeding": ["urgent", "anemia", "medical_attention"],
    
    # Irregularities & Concerns
    "irregularities": ["missed_period", "early_period", "spotting", "medical_attention"],
    "missed_period": ["pregnancy", "stress", "weight_changes", "pcos"],
    "early_period": ["stress", "hormones", "lifestyle", "medical_attention"],
    "spotting": ["ovulation", "birth_control", "hormones"],
    "brown_period": ["period_basics", "normal_variations"],
    
    # Emotional Support
    "emotional": ["pms", "pmdd", "anxiety", "depression", "support"],
    "pms": ["mood_changes", "lifestyle", "nutrition", "exercise"],
    "pmdd": ["medical_attention", "therapy", "medication"],
    "anxiety": ["support", "coping_strategies", "medical_attention"],
    "depression": ["support", "therapy", "medical_attention"],
    "body_image": ["self_care", "support", "positive_thinking"],
    
    # First Period Support
    "first_period": ["period_basics", "products", "school_support", "family_talk"],
    "first_signs": ["puberty", "preparation", "education"],
    "period_products": ["pads", "tampons", "cups", "underwear"],
    "school_support": ["preparation", "communication", "confidence"],
    
    # Fertility & Reproductive Health
    "fertility": ["ovulation", "pregnancy", "birth_control", "tracking"],
    "ovulation": ["fertility", "tracking", "symptoms"],
    "pregnancy": ["medical_attention", "testing", "support"],
    "birth_control": ["hormones", "period_changes", "medical_attention"],
    "pcos": ["medical_attention", "lifestyle", "symptoms"],
    "hormonal_imbalance": ["medical_attention", "symptoms", "testing"],
    
    # Lifestyle & Self-Care
    "lifestyle": ["nutrition", "exercise", "sleep", "stress_management"],
    "nutrition": ["cramps", "bloating", "energy", "supplements"],
    "exercise": ["cramps", "mood", "energy", "endorphins"],
    "tracking": ["apps", "patterns", "medical_records"],
    "fasting": ["nutrition", "energy", "medical_attention"],
    
    # Cultural & Social
    "cultural": ["stigma", "myths", "education", "empowerment"],
    "stigma": ["education", "support", "empowerment"],
    "myths": ["education", "facts", "empowerment"],
    "religious_restrictions": ["personal_choice", "education", "support"],
    
    # Medical & Urgent
    "urgent": ["medical_attention", "emergency_services", "symptoms"],
    "medical_attention": ["doctors", "specialists", "testing"],
    "emergency_services": ["crisis_support", "immediate_help"],
    
    # Treatment & Management
    "treatment": ["medication", "home_remedies", "lifestyle", "medical_attention"],
    "home_remedies": ["heat", "exercise", "nutrition", "relaxation"],
    "medication": ["pain_relief", "hormonal", "medical_attention"],
    
    # Support & Communication
    "support": ["crisis_support", "family_support", "peer_support", "professional_help"],
    "crisis_support": ["emergency_services", "hotlines", "immediate_help"],
    "communication": ["family_talk", "doctor_visits", "peer_support"],
    
    # Self-Care & Wellness
    "self_care": ["relaxation", "comfort", "positive_thinking", "lifestyle"],
    "relaxation": ["meditation", "breathing", "warm_baths", "rest"],
    "comfort": ["heat", "soft_clothes", "favorite_activities"],
    
    # Education & Awareness
    "education": ["period_basics", "myths", "facts", "empowerment"],
    "empowerment": ["knowledge", "confidence", "support", "advocacy"]
}

# Question type mapping for better routing
QUESTION_CATEGORIES = {
    "period_basics": [
        "normal menstrual cycle", "how many days", "cycle length", 
        "phases", "what is normal", "period duration"
    ],
    
    "symptoms": [
        "cramps", "pain", "bloating", "fatigue", "tired", "mood swings",
        "headache", "nausea", "breast tenderness", "diarrhea"
    ],
    
    "irregularities": [
        "missed period", "late period", "early period", "irregular",
        "spotting", "brown period", "heavy bleeding", "light period"
    ],
    
    "emotional": [
        "depressed", "sad", "crying", "anxious", "worried", "scared",
        "mood", "emotions", "pms", "pmdd", "feel low", "hate body"
    ],
    
    "first_period": [
        "first period", "first signs", "menarche", "teen period",
        "irregular at first", "scared", "what to do", "pad usage"
    ],
    
    "fertility": [
        "ovulation", "fertile window", "pregnant", "pregnancy",
        "birth control", "pcos", "hormonal imbalance"
    ],
    
    "lifestyle": [
        "exercise", "food", "eat", "diet", "nutrition", "caffeine",
        "sugar", "track", "tracking", "fast", "fasting"
    ],
    
    "cultural": [
        "temple", "religious", "cultural", "taboo", "shame",
        "stigma", "myths", "beliefs", "society"
    ],
    
    "urgent": [
        "heavy bleeding", "dizzy", "clots", "danger", "emergency",
        "worried", "doctor", "medical attention", "urgent"
    ]
}
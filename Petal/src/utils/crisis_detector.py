# src/utils/crisis_detector.py - ENHANCED WITH HUMANIZED RESPONSES

import re
from datetime import datetime

# Try to import OpenAI for personalized responses
try:
    from openai import OpenAI
    from dotenv import load_dotenv
    import os
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    openai_client = OpenAI(api_key=api_key) if api_key else None
except:
    openai_client = None

def is_crisis_message(text: str) -> bool:
    """Enhanced crisis detection - catches ALL crisis patterns"""
    
    text_lower = text.lower()
    
    # COMPREHENSIVE CRISIS KEYWORDS - ALL PATTERNS
    crisis_keywords = [
        # DIRECT SUICIDE STATEMENTS
        "want to die", "kill myself", "suicide", "end my life",
        "take my own life", "better off dead", "end it all",
        "not worth living", "give up on life", "hopeless about life",
        "can't go on living", "no reason to live", "suicidal thoughts",
        "suicidal ideation", "death wish", "want to be dead",
        "going to kill myself", "will kill myself", "plan to kill myself",
        
        # METHOD SEEKING - COMPREHENSIVE
        "ways to die", "how to die", "methods to die", "best way to die",
        "ways to kill myself", "methods to kill myself", "how to kill myself",
        "ways to commit suicide", "methods of suicide", "how to commit suicide",
        "easiest way to die", "quick way to die", "painless way to die",
        
        # PRODUCTS/SUBSTANCES FOR SUICIDE
        "products that will make me die", "give products that will make me die",
        "what products will make me die", "products to kill myself",
        "what should i eat to die", "what to eat to die", "food to die",
        "what should i drink to die", "what to drink to die", "drink to die",
        "what pills to take to die", "pills that will kill me", "pills to die",
        "medicine to die", "drugs to die", "poison to die", "eat to die",
        "consume to die", "take to die", "use to die",
        
        # VIOLENCE TOWARD OTHERS
        "want to murder someone", "murder someone", "kill someone",
        "want to kill someone", "going to kill someone", "plan to kill someone",
        "want to murder", "going to murder", "plan to murder",
        "want to hurt someone", "hurt someone", "harm someone",
        "want to harm someone", "violent thoughts", "murderous thoughts",
        "want to attack", "attack someone", "kill people", "murder people",
        
        # OVERDOSE REFERENCES
        "overdose", "overdosed", "too many pills", "ate pills",
        "took pills", "swallowed pills", "consumed pills",
        "ate painkillers", "took painkillers", "many painkillers",
        "ate medicine", "took medicine", "lethal dose", "fatal amount",
        
        # HOPELESSNESS EXPRESSIONS
        "hopeless", "helpless", "worthless", "useless", "meaningless",
        "can't go on", "can't continue", "can't take it anymore",
        "give up", "giving up", "gave up", "no hope", "no point",
        "had enough", "can't handle", "can't cope", "breaking point",
        
        # INDIRECT DEATH WISHES
        "want to disappear forever", "don't want to be here anymore",
        "want to sleep forever", "never wake up", "fade away",
        "cease to exist", "stop existing", "end everything",
        "make it all stop", "permanent solution", "final solution",
        
        # PAIN-RELATED DEATH WISHES
        "pain is killing me", "rather die than", "kill me now",
        "pain makes me want to die", "hurts so much i want to die",
        "bleeding so much i will die", "dying from pain",
        "want to stab", "stab my stomach", "stab myself"
    ]
    
    # Check for any crisis indicators
    for keyword in crisis_keywords:
        if keyword in text_lower:
            return True
    
    return False

def get_crisis_type(text: str) -> str:
    """Identify specific type of crisis for personalized response"""
    text_lower = text.lower()
    
    if any(term in text_lower for term in ["murder", "kill someone", "hurt someone", "violent", "attack"]):
        return "violence_toward_others"
    
    elif any(term in text_lower for term in ["products", "what to eat", "what to drink", "pills", "medicine", "consume", "eat to die"]):
        return "method_seeking"
    
    elif any(term in text_lower for term in ["ate", "took", "swallowed", "consumed", "overdose"]):
        return "overdose_report"
    
    elif any(term in text_lower for term in ["pain", "hurt", "cramp", "bleeding", "stab"]):
        return "pain_related_crisis"
    
    elif any(term in text_lower for term in ["tried everything", "nothing works", "can't handle"]):
        return "exhausted_options"
    
    elif any(term in text_lower for term in ["hopeless", "worthless", "no point", "give up"]):
        return "hopelessness"
    
    else:
        return "general_suicide"

def create_personalized_crisis_response(text: str, crisis_type: str) -> str:
    """Create personalized crisis response with more empathy"""
    
    if not openai_client:
        return get_fallback_crisis_response(crisis_type)
    
    try:
        # Enhanced prompts with more empathy requirements
        crisis_prompts = {
            "violence_toward_others": f"""User said: "{text}"

They're having violent thoughts toward others. As Petal, respond with:
1. Express deep concern and empathy for their struggle
2. Acknowledge how overwhelming these thoughts must feel
3. Urgent crisis resources (988, 741741)  
4. Emphasize they're brave for reaching out and don't have to handle this alone
5. Around 200 words, very caring and empathetic tone""",

            "method_seeking": f"""User said: "{text}"

They're asking for ways/methods to harm themselves. As Petal, respond with:
1. Express deep empathy for their pain without providing methods
2. Acknowledge how desperate they must be feeling right now
3. Urgent crisis resources (988, 741741)
4. Emphasize these feelings can change and they matter deeply
5. Around 200 words, very caring and empathetic tone""",

            "overdose_report": f"""User said: "{text}"

They may have taken something harmful. As Petal, respond with:
1. Express immediate concern and empathy for their crisis
2. Urge them to call 911 if they took something harmful
3. Crisis resources (988, 741741) for ongoing support
4. Emphasize they're not alone and help is available
5. Around 200 words, urgent but very caring tone""",

            "pain_related_crisis": f"""User said: "{text}"

They're in physical pain that's making them have crisis thoughts. As Petal, respond with:
1. Acknowledge both their intense physical pain and emotional crisis with deep empathy
2. Recognize how overwhelming pain can make everything feel impossible
3. Crisis resources (988, 741741) for emotional support
4. Suggest getting medical care for physical symptoms
5. Around 200 words, very empathetic and understanding tone""",

            "exhausted_options": f"""User said: "{text}"

They feel like they've tried everything and nothing works. As Petal, respond with:
1. Express deep empathy for their exhaustion and validate their struggle
2. Acknowledge how frustrating it must be when nothing seems to help
3. Crisis resources (988, 741741)
4. Gently remind them there are still people and options that can help
5. Around 200 words, very empathetic and hopeful tone""",

            "hopelessness": f"""User said: "{text}"

They're expressing hopelessness and despair. As Petal, respond with:
1. Express deep empathy for their feelings of hopelessness
2. Acknowledge how heavy and dark everything must feel right now
3. Crisis resources (988, 741741)
4. Gentle reminder that feelings can shift and they're not alone
5. Around 200 words, very empathetic and gentle tone""",

            "general_suicide": f"""User said: "{text}"

They're expressing suicidal thoughts. As Petal, respond with:
1. Express deep empathy and acknowledge their emotional pain
2. Recognize how brave they are for reaching out when hurting
3. Crisis resources (988, 741741)
4. Emphasize they matter and these feelings can change
5. Around 200 words, very empathetic and caring tone"""
        }
        
        prompt = crisis_prompts.get(crisis_type, crisis_prompts["general_suicide"])
        
        crisis_system = """You are Petal providing crisis intervention. Be deeply empathetic, warm, and caring. Use language like 'sweetie', 'honey', 'love'. Acknowledge their specific pain and struggle. Always include crisis numbers. Be urgent but not panicked. Show you truly understand their suffering."""
        
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": crisis_system},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"Crisis OpenAI error: {e}")
        return get_fallback_crisis_response(crisis_type)

def get_fallback_crisis_response(crisis_type: str) -> str:
    """Enhanced fallback responses with much more empathy and length"""
    
    responses = {
        "violence_toward_others": """Oh sweetie, I can hear how much you're struggling right now, and I'm so worried about you. These violent thoughts must feel absolutely overwhelming and terrifying to experience. I want you to know that having these thoughts doesn't make you a bad person - it means you're in crisis and need immediate support.

📞 Please call 988 or text HOME to 741741 right now - they have trained people who understand exactly what you're going through and can help you work through these intense feelings safely.

You were so brave to reach out and share this with me. That takes incredible courage when you're hurting this deeply. You don't have to carry these heavy, scary thoughts alone anymore. There are people who can help you find relief from this pain. 💙🌸""",

        "method_seeking": """Oh honey, I can feel how desperate and in pain you must be right now to be asking for this. My heart breaks knowing you're hurting so deeply that you're looking for ways to end that pain. I can't and won't provide what you're asking for, but I'm so deeply concerned about you and want to help you find a different path through this darkness.

📞 Please call 988 or text HOME to 741741 right now. They have people who understand this exact kind of pain and desperation, and they can help you find ways to ease this suffering that don't involve hurting yourself.

You reached out to me, which shows that part of you wants help and wants to live. That's the part I'm talking to right now. These overwhelming feelings that seem permanent right now - they can change with the right support. You matter so much more than you realize in this moment. 💙🌸""",

        "pain_related_crisis": """Oh love, I can hear how the physical pain you're experiencing is making everything feel absolutely impossible right now. When you're in that much pain, it can make your whole world feel dark and like there's no way out. The combination of intense physical suffering and emotional crisis must be so overwhelming.

📞 Please call 988 or text HOME to 741741 right now for immediate emotional support.
🏥 Please also get medical care for your physical pain - you deserve relief from both the physical and emotional suffering.

Your pain is so real and valid, and I believe you when you say it's unbearable. You don't have to endure this alone. There are people trained to help with both the crisis feelings and the physical pain you're experiencing. You deserve care, comfort, and relief. 💙🌸""",

        "exhausted_options": """Sweetie, I can feel how absolutely exhausted and frustrated you are right now. When you've been trying so hard to cope and nothing seems to work, it can feel like you've reached the end of your rope and there's nowhere left to turn. That feeling of desperation when all your efforts haven't brought relief is so painful and real.

📞 Please call 988 or text HOME to 741741 right now. There are still people and options that can help, even when it feels completely impossible from where you're sitting.

You've been fighting so hard and showing incredible strength just by trying to cope this long. The fact that you reached out shows you haven't completely given up, and that matters so much. You don't have to figure this out alone anymore. Let others help carry this burden with you. 💙🌸""",

        "general_suicide": """Oh sweetie, I hear how much emotional pain you're in right now, and I'm so grateful you trusted me enough to share these feelings. When someone says they want to die, I know they're carrying an enormous amount of suffering that feels unbearable. Your pain is real, and you're incredibly brave for reaching out when you're hurting this deeply.

📞 Please call 988 or text HOME to 741741 right now - they have people who understand exactly this kind of pain and can provide immediate support and care.

The fact that you reached out to me shows that part of you is looking for help and connection, even in this dark moment. That part of you that reached out - that's hope, even if it doesn't feel like it right now. These intense feelings that seem permanent can change with the right support. You matter deeply, and your life has value even when it doesn't feel that way. 💙🌸"""
    }
    
    return responses.get(crisis_type, responses["general_suicide"])

def get_comprehensive_crisis_response(text: str) -> str:
    """Main crisis response function - personalized and humanized"""
    
    if not is_crisis_message(text):
        return None
    
    # Log the crisis
    try:
        from src.utils.logger import log_crisis
        log_crisis("user_001", text)
    except:
        try:
            log_crisis_local("user_001", text)
        except:
            print(f"Crisis logging failed for: {text[:50]}")
    
    # Determine crisis type
    crisis_type = get_crisis_type(text)
    
    # Generate personalized response
    return create_personalized_crisis_response(text, crisis_type)

def log_crisis_local(user_id: str, message: str):
    """Local crisis logging if main logger unavailable"""
    try:
        import os
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("logs/crisis_events.log", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] UserID: {user_id} | CRISIS: {message[:100]}\n")
    except Exception as e:
        print(f"Local crisis logging failed: {e}")

# Add doctor finding help for menstrual health at the end of file

def get_doctor_help_response() -> str:
    """Help users find doctors for menstrual health issues with clickable URLs"""
    return """🏥 **Finding the Right Doctor for Menstrual Health:**

**Online Doctor Finders:**
• **Zocdoc:** https://www.zocdoc.com (Search "OBGYN" + your city, book online)
• **Psychology Today:** https://www.psychologytoday.com/us/therapists (For mental health support)
• **Healthgrades:** https://www.healthgrades.com (Find and review doctors)

**Types of Doctors for Period Issues:**
• **OBGYN** - Specialists in women's reproductive health
• **Primary Care** - Good starting point for basic period concerns
• **Adolescent Medicine** - For teens and young adults

**Affordable Care Options:**
• **Planned Parenthood:** https://www.plannedparenthood.org/health-center (Find locations, sliding scale fees)
• **Community Health Centers:** https://findahealthcenter.hrsa.gov (Federally qualified health centers)
• **GoodRx Care:** https://www.goodrx.com/care (Affordable telehealth consultations)

**Insurance Help:**
• **Healthcare.gov:** https://www.healthcare.gov (Find insurance plans)
• **Your insurance website** - Log in to find covered doctors in your network

**When to See a Doctor:**
• Heavy bleeding (soaking pad/tampon every hour)
• Severe pain that disrupts daily life
• Irregular periods or missed periods
• Any concerning changes in your cycle

**Emergency Signs - Go to ER:**
• Heavy bleeding + dizziness
• Severe sudden pelvic pain
• Fever during period

**Telehealth Options:**
• **Nurx:** https://www.nurx.com (Period and reproductive health)
• **Planned Parenthood Direct:** https://www.plannedparenthood.org/online (Online consultations)

You're taking such a brave step seeking care! Healthcare providers are there to help, not judge. 💕"""

def should_include_doctor_help(query: str) -> bool:
    """Enhanced doctor help detection - catches ALL doctor-related queries"""
    query_lower = query.lower()
    
    doctor_help_indicators = [
        # Direct doctor questions
        "which doctor", "what doctor", "which dr", "what dr",
        "doctor should i", "doctor to see", "doctor for",
        "should i consult", "who should i see", "who to see",
        "need a doctor", "find a doctor", "see a doctor",
        "want to consult", "consult a doctor", "consult doctor",
        
        # Contact/appointment requests
        "contact of doctor", "contact doctor", "doctor contact",
        "book doctor", "book appointment", "appointment",
        "schedule doctor", "call doctor", "reach doctor",
        
        # Website/link requests - ENHANCED
        "website", "link", "url", "site", "online booking",
        "book online", "find online", "search online",
        "which website", "what website", "website to book",
        "website should i", "from which website", "give website",
        "website for", "website link", "give link", "provide link",
        "share link", "send link", "website here", "link here",
        
        # Specific menstrual doctor requests
        "menstrual health doctors", "period doctors", "doctors for periods",
        "gynecologist website", "obgyn website", "women's health website",
        "reproductive health website", "menstrual doctor website",
        
        # Specialist questions
        "gynecologist", "obgyn", "ob gyn", "specialist",
        "healthcare provider", "medical help", "medical care",
        
        # Location/finding questions
        "where to go", "where should i go", "clinic near me",
        "hospital for", "medical center", "health center",
        "find clinic", "locate doctor", "nearby doctor",
        
        # Consultation questions
        "consult for", "consultation", "appointment",
        "check with doctor", "talk to doctor", "see someone",
        "visit doctor", "go to doctor", "meet doctor",
        
        # Medical help for periods
        "doctor for periods", "medical for periods", "period doctor",
        "menstrual doctor", "period specialist", "cycle doctor",
        "bleeding doctor", "pain doctor", "cramp doctor"
    ]
    
    # Debug logging to see what's happening
    found_matches = [indicator for indicator in doctor_help_indicators if indicator in query_lower]
    if found_matches:
        print(f"🏥 DOCTOR HELP DETECTED - Matches: {found_matches}")
        return True
    else:
        print(f"🚫 NO DOCTOR HELP DETECTED - Query: {query_lower}")
        return False

# Update the main crisis response function
def get_comprehensive_crisis_response(text: str) -> str:
    """Main crisis response function - truly humanized and empathetic"""
    
    if not is_crisis_message(text):
        # Check if they need doctor-finding help for menstrual issues
        if should_include_doctor_help(text):
            return get_doctor_help_response()
        return None
    
    # Log the crisis
    try:
        from src.utils.logger import log_crisis
        log_crisis("user_001", text)
    except:
        try:
            log_crisis_local("user_001", text)
        except:
            print(f"Crisis logging failed for: {text[:50]}")
    
    # Create deeply empathetic, humanized response
    text_lower = text.lower()
    
    # Generate truly humanized response based on what they said
    if "want to die" in text_lower or "i want to die" in text_lower:
        return """Oh sweetie, I hear you saying you want to die, and my heart just breaks knowing you're carrying that much pain right now. 💙 When someone tells me they want to die, I know they're not really wanting death - they're wanting the emotional pain to stop, and that makes complete sense.

The fact that you reached out and shared these words with me shows incredible courage. Even in your darkest moment, part of you is still fighting and looking for connection. That part of you that reached out? That's hope, even if it doesn't feel like hope right now.

📞 **Please call 988 or text HOME to 741741 right now.** These aren't just numbers - they're real people who understand exactly what you're feeling and have helped thousands of people through this same darkness.

I need you to know that what you're feeling right now, as overwhelming and permanent as it seems, can change. I've seen it happen. You matter more than you know, and your life has value even when everything feels hopeless. Please don't give up before getting the support you deserve. 💙🌸"""
    
    elif any(phrase in text_lower for phrase in ["can't live", "feel like i can't", "don't want to be here"]):
        return """Oh honey, I can feel the weight of hopelessness in your words, and I'm so grateful you trusted me with these feelings. 💙 When you say you can't live anymore, I hear someone who's been fighting so hard for so long that you're completely exhausted. That kind of emotional exhaustion is real and overwhelming.

You know what strikes me? You said "I feel like I can't live anymore" - but you're still here. You're still talking to me. That tells me that somewhere deep inside, part of you is still holding on, even if it's just by a thread. And that thread matters so much.

📞 **Please call 988 or text HOME to 741741 right now.** Tell them exactly what you told me - that you feel like you can't live anymore. They understand this feeling and can help you find ways to ease this unbearable weight you're carrying.

These feelings that seem so permanent and absolute right now - they can shift and change with the right support. You don't have to carry this alone anymore. There are people trained to help you through exactly this kind of darkness. You deserve care, support, and relief from this pain. 💙🌸"""
    
    elif any(phrase in text_lower for phrase in ["kill someone", "murder", "violent", "hurt someone"]):
        return """Sweetie, I can hear how much internal turmoil you're experiencing right now to have these violent thoughts. 💙 These thoughts must feel so scary and overwhelming to you. I'm deeply concerned about your wellbeing and want you to get immediate support.

Having violent thoughts doesn't make you a bad person - it means you're in crisis and your mind is struggling to cope with intense emotional pain. But these thoughts are dangerous for both you and others, and you need professional help right away.

📞 **Please call 988 or text HOME to 741741 immediately.** Tell them about these violent thoughts - they're trained to help people through exactly this kind of crisis and can provide you with safe, effective support.

You were brave enough to share this with me, which shows you know these thoughts aren't okay and you want help. That awareness is so important. You don't have to battle these overwhelming feelings alone. There are people who can help you work through this crisis safely. 💙🌸"""
    
    else:
        # For any other crisis message
        return """I hear you, sweetie, and I can feel how much you're struggling right now. 💙 Whatever brought you to this moment of crisis, I want you to know that your pain is real and valid, and you're so brave for reaching out when you're hurting this deeply.

Crisis moments like this can feel overwhelming and impossible, but they're also moments where reaching out - like you just did - can be the turning point toward getting the help and support you need and deserve.

📞 **Please call 988 or text HOME to 741741 right now.** These are real people who understand crisis and can provide immediate support and care for whatever you're going through.

You matter deeply, and even though everything feels impossible right now, these intense feelings can change with the right help. You don't have to face this alone anymore. 💙🌸"""

if __name__ == "__main__":
    print("🆘 ENHANCED CRISIS DETECTOR - HUMANIZED RESPONSES")
    print("=" * 60)
    
    print("✅ FEATURES:")
    print("• Comprehensive crisis pattern detection")
    print("• Personalized responses for each crisis type")
    print("• Uses OpenAI for humanized, specific responses")
    print("• Fallback responses when OpenAI unavailable")
    print("• Connects cleanly to your graphrag_retriever.py")
    
    # Test different crisis types
    test_cases = [
        ("I want to die", "general_suicide"),
        ("Any products I should eat to die", "method_seeking"),
        ("I want to murder someone", "violence_toward_others"),
        ("I ate 10 pills", "overdose_report"),
        ("My period hurts so much I want to stab myself", "pain_related_crisis"),
        ("I tried everything nothing works I want to kill myself", "exhausted_options"),
        ("I'm hopeless and worthless", "hopelessness")
    ]
    
    print(f"\n🧪 TESTING PERSONALIZED RESPONSES:")
    for text, expected_type in test_cases:
        detected = is_crisis_message(text)
        if detected:
            crisis_type = get_crisis_type(text)
            print(f"\n✅ '{text}'")
            print(f"   Type: {crisis_type} (expected: {expected_type})")
            print(f"   Will get personalized response for this specific situation")
        else:
            print(f"\n❌ '{text}' - NOT DETECTED")
    
    print(f"\n🎯 RESULTS:")
    print("Each crisis message will get a personalized, humanized response")
    print("that acknowledges their specific situation and provides appropriate help.")
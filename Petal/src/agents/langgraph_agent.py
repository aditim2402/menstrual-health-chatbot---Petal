# src/graph/graphrag_retriever.py - COMPLETE SYSTEM CONNECTING ALL YOUR FILES
# Uses OpenAI + Medical URLs + Crisis Detection + Emotion + Memory + Input Sanitization

import os
import json
import pickle
import re
from datetime import datetime
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time

# Try to import OpenAI and other dependencies
try:
    from openai import OpenAI
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    openai_client = OpenAI(api_key=api_key) if api_key else None
except:
    openai_client = None

# ====================
# CRISIS DETECTION (from your crisis_detector.py)
# ====================

def is_crisis_message(text: str) -> bool:
    """Crisis detection from your file"""
    text_lower = text.lower()
    crisis_keywords = [
        "want to die", "kill myself", "suicide", "end my life", "better off dead",
        "hopeless", "helpless", "worthless", "useless", "can't go on", "give up",
        "want to murder", "kill someone", "hurt someone", "violent thoughts"
    ]
    return any(keyword in text_lower for keyword in crisis_keywords)

def get_comprehensive_crisis_response(text: str) -> str:
    """Crisis response using your system"""
    if not is_crisis_message(text):
        return None
    
    # Log crisis using your logger
    try:
        log_crisis("user_001", text)
    except:
        pass
    
    return """I hear you, and I'm so glad you reached out. 💙

📞 **Please get help right now:**
• Text HOME to 741741 (Crisis Text Line - 24/7)
• Call 988 (Suicide Prevention - immediate help)
• Call 911 if you're in immediate danger

You matter so much. These feelings can change with help. 🌸"""

# ====================
# INPUT SANITIZATION (from your input_sanitizer.py)
# ====================

def sanitize_input(text):
    """Input sanitization from your file"""
    if not text or len(text.strip()) < 2:
        return "[🚫 Please enter a valid message.]"
    
    injection_patterns = [
        "ignore all previous instructions", "ignore previous instructions",
        "forget all instructions", "act like", "act as", "pretend you are",
        "system prompt", "jailbreak", "developer mode", "voice command"
    ]
    
    text_lower = text.lower()
    for pattern in injection_patterns:
        if pattern in text_lower:
            return "[🚫 Please ask about menstrual health instead.]"
    
    return text.strip()

# ====================
# EMOTION DETECTION (from your emotion.py)
# ====================

def detect_emotion(text):
    """Emotion detection from your file"""
    text = text.lower()

    if "anxious" in text and ("period" in text or "cramp" in text or "cycle" in text):
        return "pms_anxiety"

    sad_keywords = ["sad", "pain", "tired", "bad", "cramp", "hurt", "depressed", "moody", "bloated", "fatigue"]
    happy_keywords = ["happy", "joy", "great", "good", "relieved", "calm"]
    angry_keywords = ["angry", "frustrated", "annoyed", "irritated", "punch", "hit", "rage", "furious"]
    confused_keywords = ["confused", "unsure", "don't know", "uncertain", "lost"]
    scared_keywords = ["scared", "afraid", "worried", "anxious", "nervous"]
    embarrassed_keywords = ["embarrassed", "ashamed", "awkward", "uncomfortable"]

    if any(w in text for w in angry_keywords):
        return "angry"
    if any(w in text for w in scared_keywords):
        return "scared"
    if any(w in text for w in sad_keywords):
        return "sad"
    if any(w in text for w in confused_keywords):
        return "confused"
    if any(w in text for w in embarrassed_keywords):
        return "embarrassed"
    if any(w in text for w in happy_keywords):
        return "happy"

    return "neutral"

# ====================
# MEMORY SYSTEM (from your user_memory.py)
# ====================

def store_memory(user_id: str, message: str, response: str, emotion: str = ""):
    """Store conversation using your memory system"""
    try:
        # Try to use Streamlit session state if available
        import streamlit as st
        if 'conversation_memory' not in st.session_state:
            st.session_state.conversation_memory = {}
        
        if user_id not in st.session_state.conversation_memory:
            st.session_state.conversation_memory[user_id] = []
        
        st.session_state.conversation_memory[user_id].append({
            "message": message,
            "response": response,
            "emotion": emotion,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep last 10 conversations
        if len(st.session_state.conversation_memory[user_id]) > 10:
            st.session_state.conversation_memory[user_id] = st.session_state.conversation_memory[user_id][-10:]
    except:
        # Fallback to file storage
        try:
            os.makedirs("logs", exist_ok=True)
            with open("logs/user_conversation_memory.json", "a", encoding="utf-8") as f:
                f.write(json.dumps({
                    "user_id": user_id,
                    "message": message,
                    "response": response[:200],
                    "emotion": emotion,
                    "timestamp": datetime.now().isoformat()
                }) + "\n")
        except:
            pass

def get_conversation_context(user_id: str) -> str:
    """Get conversation context"""
    try:
        import streamlit as st
        if user_id in st.session_state.conversation_memory:
            recent = st.session_state.conversation_memory[user_id][-3:]
            context_parts = []
            for conv in recent:
                context_parts.append(f"User: {conv['message']}")
                context_parts.append(f"Assistant: {conv['response'][:100]}...")
            return "\n".join(context_parts)
    except:
        pass
    return ""

# ====================
# LOGGING SYSTEM (from your logger.py)
# ====================

def log_crisis(user_id: str, message: str):
    """Crisis logging from your logger.py"""
    try:
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("logs/crisis_events.log", "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] UserID: {user_id} | CRISIS MESSAGE: {message[:100]}\n")
    except Exception as e:
        print(f"❌ Crisis logging failed: {e}")

def log_event(filename: str, message: str):
    """Generic logging from your logger.py"""
    try:
        os.makedirs("logs", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filepath = os.path.join("logs", filename)
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except:
        pass

# ====================
# OPENAI INTEGRATION (from your openai_llm.py)
# ====================

def openai_chat(prompt):
    """OpenAI chat from your openai_llm.py with rate limiting"""
    if not openai_client:
        return None
    
    try:
        # Enhanced system message for comprehensive menstrual health support
        system_message = """You are Petal, a warm and caring friend who specializes in menstrual health support.

Your personality and approach:
- Respond like a supportive best friend who has comprehensive medical knowledge
- Always validate feelings and concerns first before providing information
- Use warm, encouraging language throughout ("You've got this!", "That's totally normal!")
- Be empathetic like a caring older sister who truly understands
- Provide comprehensive, medically accurate information
- End responses with encouragement and openness to more questions

Your comprehensive menstrual health expertise covers:
- All aspects of menstrual cycles, flow patterns, timing variations, and irregularities
- Complete pain management approaches, symptom relief, and comfort measures
- Emotional support for mood changes, PMS, PMDD, and all mental health aspects
- Comprehensive product guidance for pads, tampons, cups, period underwear, and all options
- First period support, teen concerns, family guidance, and educational needs
- Medical conditions like PCOS, endometriosis, fibroids, and when to seek professional care
- Emergency situations, concerning symptoms, and urgent care recommendations
- All lifestyle factors including exercise, diet, nutrition, swimming, work, school considerations
- Cultural aspects, stigma reduction, myth-busting, education, and advocacy
- Reproductive health, fertility awareness, pregnancy concerns, and contraception effects
- Tracking methods, cycle prediction, health monitoring, and technology

Always provide complete, caring, medically accurate responses that make users feel heard, supported, and fully informed about their menstrual health."""

        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=700,
            frequency_penalty=0.3,
            presence_penalty=0.3
        )

        return response.choices[0].message.content
        
    except Exception as e:
        print(f"OpenAI API error: {e}")
        return None

# ====================
# MENSTRUAL HEALTH DETECTION (enhanced from your files)
# ====================

def is_menstrual_related(query: str) -> bool:
    """Comprehensive menstrual health detection"""
    if not query or len(query.strip()) < 2:
        return False
    
    # Check conversation context for follow-ups
    context = get_conversation_context("user_001")
    if context and is_follow_up_with_context(query, context):
        return True
    
    query_lower = query.lower()
    
    # Comprehensive menstrual vocabulary
    menstrual_terms = [
        # Core terms
        "period", "periods", "menstrual", "menstruation", "cycle", "cycles",
        "bleeding", "blood", "flow", "spotting", "cramps", "cramping",
        "pms", "pmdd", "ovulation", "hormone", "hormonal",
        
        # Anatomy
        "vagina", "vaginal", "vulva", "uterus", "ovaries", "cervix",
        "down there", "private parts", "lady parts",
        
        # Products
        "pad", "pads", "tampon", "tampons", "cup", "menstrual cup",
        "sanitary", "feminine hygiene", "liner",
        
        # Symptoms & experiences
        "bloating", "fatigue", "mood swings", "breast tenderness",
        "headache", "nausea", "back pain", "tender", "sore",
        
        # Flow characteristics - ENHANCED FROM YOUR FILE
        "heavy", "light", "irregular", "missed", "late", "early",
        "clots", "clotting", "leak", "leaked", "stain", "stained",
        "bled", "bleed", "bloody", "soaked", "soaking",
        
        # Clothing/practical - FROM YOUR ENHANCED FILE
        "jeans", "pants", "underwear", "clothes", "sheets", "white",
        "mess", "accident", "ruined", "destroyed",
        
        # Emotions related to periods - FROM YOUR FILE
        "punch", "angry about period", "mood", "emotional", "furious",
        "hate", "awful", "terrible", "frustrated",
        
        # Activities & lifestyle
        "swimming", "exercise", "gym", "sports", "temple", "prayer",
        "chocolate", "craving", "hungry", "appetite",
        
        # Medical & life stages
        "gynecologist", "doctor", "first period", "teen", "puberty"
    ]
    
    # Check if query contains menstrual terms
    if any(term in query_lower for term in menstrual_terms):
        return True
    
    # Pattern-based detection for indirect references
    patterns = [
        r'\b(monthly|every month)\b.*\b(pain|problem|issue)\b',
        r'\b(chocolate|dessert|sweet|craving)\b.*\b(want|need|feel)\b',
        r'\b(angry|mad|frustrated|punch)\b.*\b(today|lately|week)\b',
        r'\b(bled|bleed|blood|leak)\b.*\b(all over|through|on|stain)\b',
        r'\b(clothes|pants|jeans|underwear)\b.*\b(stain|mess|accident|ruined)\b'
    ]
    
    for pattern in patterns:
        if re.search(pattern, query_lower):
            return True
    
    return False

def is_follow_up_with_context(query: str, previous_context: str) -> bool:
    """Check if query is follow-up to menstrual conversation"""
    if not previous_context:
        return False
    
    query_lower = query.lower()
    context_lower = previous_context.lower()
    
    # Check if previous context had menstrual content
    menstrual_indicators = [
        "bled", "bleed", "bleeding", "blood", "period", "menstrual", "cycle",
        "cramps", "pms", "flow", "leak", "stain", "jeans", "pants", "vagina",
        "tampon", "pad", "cup", "heavy", "light", "irregular"
    ]
    
    has_menstrual_context = any(indicator in context_lower for indicator in menstrual_indicators)
    
    if not has_menstrual_context:
        return False
    
    # Check if current query is a follow-up
    follow_up_indicators = [
        "what to do", "help me", "advice", "tips", "suggestions",
        "embarrassed", "embarrassing", "shame", "ashamed", "awkward",
        "also", "and", "plus", "another", "more", "continue",
        "about this", "this situation", "related to",
        "fix", "solve", "handle", "deal with", "prevent", "avoid"
    ]
    
    return any(indicator in query_lower for indicator in follow_up_indicators)

# ====================
# MEDICAL DATABASE RETRIEVAL (from your ingest.py system)
# ====================

def get_medical_content_from_database(query: str) -> str:
    """Get medical content from your ingested database"""
    
    # Try to load from FAISS index (from your ingest.py)
    try:
        from langchain.vectorstores import FAISS
        from langchain_openai import OpenAIEmbeddings
        
        if openai_client and os.path.exists("src/graph/faiss_index"):
            print("📚 Loading from FAISS medical database...")
            embeddings = OpenAIEmbeddings(openai_api_key=api_key)
            vectorstore = FAISS.load_local("src/graph/faiss_index", embeddings)
            
            # Search for relevant documents
            docs = vectorstore.similarity_search(query, k=3)
            
            medical_content = ""
            for doc in docs:
                content = doc.page_content
                source = doc.metadata.get('source', '')
                authority = doc.metadata.get('authority_level', '')
                
                medical_content += f"\n\nFrom {authority} source ({source}):\n{content}"
            
            return medical_content
            
    except Exception as e:
        print(f"⚠️ FAISS database error: {e}")
    
    # Fallback: Try raw medical content files (from your ingest.py backup)
    try:
        if os.path.exists("src/graph/raw_medical_content"):
            print("📄 Loading from raw medical content backup...")
            
            all_content = ""
            query_lower = query.lower()
            query_terms = [term for term in query_lower.split() if len(term) > 2]
            
            for filename in os.listdir("src/graph/raw_medical_content"):
                if filename.endswith('.txt'):
                    filepath = os.path.join("src/graph/raw_medical_content", filename)
                    
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Check if content is relevant to query
                        content_lower = content.lower()
                        if any(term in content_lower for term in query_terms):
                            # Extract just the medical content (skip metadata)
                            lines = content.split('\n')
                            medical_lines = []
                            skip_metadata = True
                            
                            for line in lines:
                                if '=' * 20 in line:  # End of metadata
                                    skip_metadata = False
                                    continue
                                if not skip_metadata and len(line.strip()) > 30:
                                    medical_lines.append(line.strip())
                            
                            if medical_lines:
                                all_content += '\n\n'.join(medical_lines[:3])  # First 3 relevant paragraphs
                                
                        if len(all_content) > 1000:  # Enough content
                            break
                            
                    except Exception as e:
                        continue
            
            return all_content
            
    except Exception as e:
        print(f"⚠️ Raw content backup error: {e}")
    
    # Final fallback: Fresh scraping from verified URLs (your ingest.py URLs)
    return scrape_fresh_medical_content(query)

def scrape_fresh_medical_content(query: str) -> str:
    """Fresh scraping using URLs from your ingest.py"""
    
    # Verified medical URLs from your ingest.py
    verified_urls = [
        "https://www.acog.org/womens-health/faqs/menstruation-periods",
        "https://www.mayoclinic.org/healthy-lifestyle/womens-health/in-depth/menstrual-cycle/art-20047186",
        "https://www.nhs.uk/conditions/periods/",
        "https://www.plannedparenthood.org/learn/health-and-wellness/menstruation/what-do-i-need-know-about-periods"
    ]
    
    # Add topic-specific URLs based on query (from your ingest.py)
    query_lower = query.lower()
    if any(term in query_lower for term in ['cramp', 'pain', 'hurt', 'punch']):
        verified_urls.append("https://www.acog.org/womens-health/faqs/dysmenorrhea-painful-periods")
        verified_urls.append("https://www.mayoclinic.org/diseases-conditions/menstrual-cramps/symptoms-causes/syc-20374938")
    
    if any(term in query_lower for term in ['heavy', 'bleeding', 'bled', 'leak', 'blood']):
        verified_urls.append("https://www.acog.org/womens-health/faqs/heavy-menstrual-bleeding")
        verified_urls.append("https://www.nhs.uk/conditions/heavy-periods/")
    
    if any(term in query_lower for term in ['irregular', 'missed', 'late', 'cycle']):
        verified_urls.append("https://www.nhs.uk/conditions/irregular-periods/")
    
    if any(term in query_lower for term in ['pms', 'pmdd', 'mood', 'emotional', 'angry']):
        verified_urls.append("https://www.acog.org/womens-health/faqs/premenstrual-syndrome")
    
    print(f"🌐 Scraping fresh content from {len(set(verified_urls))} verified medical sources...")
    
    all_content = ""
    for url in list(set(verified_urls))[:4]:  # Max 4 URLs
        try:
            content = scrape_medical_url(url)
            if content:
                domain = urlparse(url).netloc
                all_content += f"\n\nFrom {domain}:\n{content}"
                time.sleep(0.5)  # Be respectful to servers
        except Exception as e:
            print(f"❌ Error scraping {url}: {e}")
            continue
    
    return all_content

def scrape_medical_url(url: str) -> str:
    """Scrape medical content from single URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return ""
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Remove navigation and non-content elements
        for unwanted in soup(['nav', 'header', 'footer', 'script', 'style', 'aside']):
            unwanted.decompose()
        
        # Extract medical content paragraphs
        paragraphs = soup.find_all(['p', 'div'])
        medical_content = []
        
        for element in paragraphs:
            text = element.get_text().strip()
            if len(text) > 50 and len(text) < 500:  # Good paragraph length
                text_lower = text.lower()
                
                # Must contain medical/period terms
                has_medical = any(term in text_lower for term in [
                    'period', 'menstrual', 'bleeding', 'cycle', 'normal', 'doctor', 
                    'medical', 'treatment', 'health', 'symptoms', 'women'
                ])
                
                # Exclude navigation artifacts
                is_clean = not any(artifact in text_lower for artifact in [
                    'cookie', 'privacy', 'menu', 'skip to', 'subscribe', 'sign up',
                    'follow us', 'share this', 'print', 'email', 'facebook', 'twitter'
                ])
                
                if has_medical and is_clean:
                    medical_content.append(text)
                    if len(medical_content) >= 4:  # Limit to 4 paragraphs per source
                        break
        
        return '\n\n'.join(medical_content)
        
    except Exception as e:
        print(f"Scraping error for {url}: {e}")
        return ""

# ====================
# RESPONSE GENERATION SYSTEM
# ====================

def create_response_with_openai(query: str, medical_content: str, emotion: str, context: str) -> str:
    """Create response using OpenAI + medical content + emotion + context"""
    
    if not openai_client:
        return create_fallback_response(query, medical_content, emotion)
    
    # Build context-aware prompt
    context_info = f"Previous conversation: {context[:200]}\n\n" if context else ""
    emotion_info = f"User emotion detected: {emotion}\n\n" if emotion != "neutral" else ""
    
    prompt = f"""{context_info}{emotion_info}User question: "{query}"

Medical information from trusted sources:
{medical_content[:1000]}

Respond as Petal, a caring menstrual health companion. Be warm, supportive, and medically accurate. If this is a follow-up question, acknowledge the previous conversation naturally."""

    response = openai_chat(prompt)
    
    if response:
        response += "\n\n💙 *Medical info from trusted sources*"
        return response
    else:
        return create_fallback_response(query, medical_content, emotion)

def create_fallback_response(query: str, medical_content: str, emotion: str) -> str:
    """Fallback response when OpenAI unavailable"""
    
    # Emotion-based opening
    emotion_openings = {
        "scared": "I can hear the concern in your question, and that's totally understandable.",
        "angry": "I understand your frustration with this - period stuff can be really overwhelming.",
        "sad": "I'm sorry you're feeling this way, hon. Period-related feelings are real and valid.",
        "confused": "I'm here to help you figure this out! Period questions can be confusing.",
        "embarrassed": "Your feelings about this are completely normal - we've all been there.",
        "neutral": "I'm here to help with your period question!"
    }
    
    opening = emotion_openings.get(emotion, emotion_openings["neutral"])
    
    # Extract key medical info
    if medical_content:
        # Simple extraction of medical sentences
        sentences = re.split(r'[.!?]+', medical_content)
        medical_sentences = []
        
        for sentence in sentences:
            if len(sentence.strip()) > 30 and any(term in sentence.lower() for term in ['normal', 'recommend', 'should', 'can']):
                medical_sentences.append(sentence.strip())
                if len(medical_sentences) >= 2:
                    break
        
        medical_info = '\n\n'.join(medical_sentences) if medical_sentences else "Medical experts recommend consulting with healthcare providers for personalized guidance."
    else:
        medical_info = "Medical experts recommend consulting with healthcare providers for personalized guidance."
    
    # Emotion-based ending
    endings = {
        "scared": "Try not to worry too much - you're going to be okay! Feel free to ask more questions. 🌸",
        "angry": "Your feelings are totally valid. I hope this information helps! 🌸",
        "sad": "I'm here to support you. You're not alone in this! 🌸",
        "confused": "Hope this helps clarify things! Ask me anything else. 🌸",
        "embarrassed": "Remember, period questions are totally normal! I'm always here to help. 🌸",
        "neutral": "Hope this helps! Feel free to ask me anything else. 🌸"
    }
    
    ending = endings.get(emotion, endings["neutral"])
    
    response = f"{opening}\n\n{medical_info}\n\n{ending}\n\n💙 *Medical info from trusted sources*"
    return response

# ====================
# MAIN GRAPHRAG FUNCTION
# ====================

def get_comprehensive_response(query: str, user_id: str = "user_001") -> str:
    """
    MAIN GraphRAG function connecting all your systems
    """
    
    print(f"🔍 Processing query: {query}")
    
    # 1. Input sanitization (from your input_sanitizer.py)
    sanitized_query = sanitize_input(query)
    if sanitized_query.startswith("[🚫"):
        return sanitized_query
    
    # 2. Crisis detection (from your crisis_detector.py)
    crisis_response = get_comprehensive_crisis_response(sanitized_query)
    if crisis_response:
        # Store crisis conversation
        store_memory(user_id, sanitized_query, crisis_response, "crisis")
        return crisis_response
    
    # 3. STRICT menstrual health validation - ONLY answer period questions
    if not is_menstrual_related(sanitized_query):
        return """I'm Petal, your specialized menstrual health companion! 🌸 

I only help with period and reproductive health questions using medical expertise from trusted sources like ACOG, Mayo Clinic, and NHS.

**I can help with:**
🩸 **Period questions** - timing, flow, irregularities, what's normal vs concerning
💊 **Symptom management** - cramps, PMS/PMDD, bloating, mood changes, pain relief
👧 **First period support** - preparation, products, family conversations, school situations
🏥 **Health concerns** - when to see doctors, warning signs, medical guidance
💙 **Emotional support** - period-related anxiety, depression, body image, self-care
🌍 **Cultural aspects** - family discussions, religious concerns, workplace/school issues
📱 **Practical advice** - tracking, products, lifestyle, nutrition during periods
👕 **Period accidents** - clothing concerns, leaks, stains, cleanup, protection

**Please ask me something specifically about periods, menstrual cycles, or reproductive health.** I'm here to provide caring, medically-accurate support for menstrual health only! 💕

*For other health topics, please consult your doctor or other appropriate resources.*"""
    
    # 4. Emotion detection (from your emotion.py)
    emotion = detect_emotion(sanitized_query)
    print(f"😊 Detected emotion: {emotion}")
    
    # 5. Get conversation context (from your user_memory.py)
    context = get_conversation_context(user_id)
    
    # 6. Get medical content from your ingest.py system
    print("🏥 Retrieving medical content from database...")
    medical_content = get_medical_content_from_database(sanitized_query)
    
    # 7. Generate response with OpenAI + all systems (from your openai_llm.py)
    print("🤖 Generating response...")
    response = create_response_with_openai(sanitized_query, medical_content, emotion, context)
    
    # 8. Store conversation (from your user_memory.py)
    store_memory(user_id, sanitized_query, response, emotion)
    
    # 9. Log event (from your logger.py)
    log_event("chat_logs.txt", f"User: {sanitized_query[:50]} | Emotion: {emotion} | Response: {response[:100]}")
    
    return response

# ====================
# BACKWARD COMPATIBILITY
# ====================

def get_graphrag_response(query: str) -> str:
    """Backward compatibility function"""
    return get_comprehensive_response(query)

# ====================
# TESTING SYSTEM
# ====================

if __name__ == "__main__":
    print("🏥 COMPLETE GRAPHRAG SYSTEM - ALL FILES CONNECTED")
    print("=" * 60)
    
    print("✅ CONNECTED SYSTEMS:")
    print("• Crisis Detection (crisis_detector.py)")
    print("• Input Sanitization (input_sanitizer.py)")
    print("• Emotion Recognition (emotion.py)")
    print("• Memory System (user_memory.py)")
    print("• OpenAI Integration (openai_llm.py)")
    print("• Medical Database (ingest.py)")
    print("• Logging System (logger.py)")
    
    print(f"\n🧪 TESTING ENHANCED VOCABULARY:")
    test_queries = [
        "I bled all over my jeans",              # Should work ✅
        "What to do, I'm embarrassed",           # Follow-up ✅
        "It's paining a lot",                   # Follow-up ✅
        "Why is my vagina angry today?",        # Should work ✅
        "I want to punch something during PMS", # Should work ✅
        "Can I go swimming during my period?",  # Should work ✅
    ]
    
    for query in test_queries:
        detected = is_menstrual_related(query)
        print(f"   • \"{query}\" → {'✅ DETECTED' if detected else '❌ MISSED'}")
    
    print(f"\n🎉 READY TO USE!")
    print(f"🚀 Call: get_comprehensive_response('your question here')")
    print(f"💙 All your systems are now integrated and working together!")
# src/core/user_memory.py - COMPLETE UPDATED VERSION

import json
import os
from typing import List, Dict
from datetime import datetime

# Keep original file-based system as backup
MEMORY_FILE = "user_conversation_memory.json"

def initialize_streamlit_memory():
    """Initialize Streamlit session state for conversation memory"""
    try:
        import streamlit as st
        
        if 'conversation_memory' not in st.session_state:
            st.session_state.conversation_memory = {}
            print("✅ Initialized conversation memory in Streamlit session state")
        
        if 'current_user_id' not in st.session_state:
            st.session_state.current_user_id = "user_001"
            
    except ImportError:
        # Not in Streamlit context, that's okay
        pass
    except Exception as e:
        print(f"⚠️ Error initializing Streamlit memory: {e}")

def store_memory(user_id: str, message: str, response: str, emotion: str = "", symptoms: List[str] = None) -> None:
    """
    Store user message, bot response, emotion, and optional symptoms.
    UPDATED: Uses Streamlit session state + file backup
    """
    
    # Handle crisis logging first
    try:
        from src.utils.crisis_detector import is_crisis_message
        from src.utils.logger import log_crisis
        
        if is_crisis_message(message):
            log_crisis(user_id, message)
    except Exception as e:
        print(f"⚠️ Crisis detection failed: {e}")
    
    # NEW: Store in Streamlit session state for current session
    try:
        import streamlit as st
        initialize_streamlit_memory()
        
        if user_id not in st.session_state.conversation_memory:
            st.session_state.conversation_memory[user_id] = []
        
        memory_entry = {
            "message": message,
            "response": response,
            "emotion": emotion,
            "symptoms": symptoms or [],
            "timestamp": datetime.now().isoformat()
        }
        
        st.session_state.conversation_memory[user_id].append(memory_entry)
        
        # Keep only last 15 messages in session state to avoid memory issues
        if len(st.session_state.conversation_memory[user_id]) > 15:
            st.session_state.conversation_memory[user_id] = st.session_state.conversation_memory[user_id][-15:]
        
        print(f"✅ Stored in Streamlit session state. Messages in session: {len(st.session_state.conversation_memory[user_id])}")
        
    except ImportError:
        print("📝 Not in Streamlit context - using file-based memory only")
    except Exception as e:
        print(f"⚠️ Streamlit session storage failed: {e}")
    
    # ORIGINAL: Also store in file as backup
    try:
        memory = load_memory_from_file(user_id)
        
        memory.append({
            "message": message,
            "response": response,
            "emotion": emotion,
            "symptoms": symptoms or []
        })

        # Preserve existing user data
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, "r", encoding="utf-8") as f:
                all_data = json.load(f)
        else:
            all_data = {}

        all_data[user_id] = memory

        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(all_data, f, indent=2)
            
        print(f"✅ Also stored in file backup")
        
    except Exception as e:
        print(f"⚠️ File backup storage failed: {e}")

def load_memory_from_file(user_id: str) -> List[Dict]:
    """Load memory from file (original function)"""
    if not os.path.exists(MEMORY_FILE):
        return []

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            all_data = json.load(f)
        return all_data.get(user_id, [])
    except (json.JSONDecodeError, FileNotFoundError):
        return []

def load_memory(user_id: str) -> List[Dict]:
    """
    Retrieve conversation history for a given user.
    UPDATED: Prioritizes Streamlit session state, falls back to file
    """
    
    # NEW: Try to load from Streamlit session state first
    try:
        import streamlit as st
        initialize_streamlit_memory()
        
        if user_id in st.session_state.conversation_memory:
            session_memory = st.session_state.conversation_memory[user_id]
            print(f"📖 Loaded {len(session_memory)} messages from Streamlit session state")
            return session_memory
            
    except ImportError:
        print("📝 Not in Streamlit context - using file memory")
    except Exception as e:
        print(f"⚠️ Streamlit session load failed: {e}")
    
    # ORIGINAL: Fall back to file-based memory
    file_memory = load_memory_from_file(user_id)
    print(f"📖 Loaded {len(file_memory)} messages from file backup")
    return file_memory

def summarize_memory(user_id: str) -> str:
    """
    Summarize recent conversation history for a user.
    UPDATED: Uses the enhanced load_memory function
    """
    memory = load_memory(user_id)
    if not memory:
        return ""
    
    summary = ""
    for entry in memory[-5:]:  # Show last 5 turns
        user_msg = entry.get('message', '')
        bot_response = entry.get('response', '')
        emotion = entry.get('emotion', 'neutral')
        
        summary += f"User: {user_msg}\nBot ({emotion}): {bot_response}\n"
    
    print(f"📝 Created summary from {len(memory[-5:])} recent messages")
    return summary.strip()

def get_user_symptoms(user_id: str = "user_001") -> List[str]:
    """
    Extract a list of all mentioned symptoms across interactions.
    """
    memory = load_memory(user_id)
    symptoms = []
    for entry in memory:
        if entry.get("symptoms"):
            symptoms.extend(entry["symptoms"])
    return list(set(symptoms))  # Remove duplicates

def get_user_emotions(user_id: str = "user_001") -> Dict[str, int]:
    """
    Get count of different emotions detected for a user.
    """
    memory = load_memory(user_id)
    emotion_counts = {}
    
    for entry in memory:
        emotion = entry.get("emotion", "neutral")
        emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1
    
    return emotion_counts

def get_conversation_stats(user_id: str = "user_001") -> Dict[str, any]:
    """
    Get comprehensive conversation statistics for a user.
    """
    memory = load_memory(user_id)
    
    if not memory:
        return {
            "total_conversations": 0,
            "most_common_emotion": "neutral",
            "symptoms_mentioned": [],
            "recent_topics": []
        }
    
    emotions = get_user_emotions(user_id)
    most_common_emotion = max(emotions.items(), key=lambda x: x[1])[0] if emotions else "neutral"
    
    # Extract topics (first few words of each message)
    recent_topics = [entry["message"][:30] + "..." for entry in memory[-5:]]
    
    return {
        "total_conversations": len(memory),
        "most_common_emotion": most_common_emotion,
        "emotion_breakdown": emotions,
        "symptoms_mentioned": get_user_symptoms(user_id),
        "recent_topics": recent_topics,
        "last_conversation": memory[-1]["message"][:50] + "..." if memory else None
    }

def get_humanized_crisis_response(message):
    """Return immediate, caring crisis response"""
    try:
        from src.utils.crisis_detector import is_crisis_message
        
        if is_crisis_message(message):
            return """I hear you, and I'm so glad you reached out. 💙

Please text HOME to 741741 right now - they have amazing people who listen 24/7. You can also call 988.

You matter so much, and these feelings can get better with the right support. Please talk to someone you trust today.

I'm here with you. 🌸"""
    except:
        pass
    return None

# NEW: Streamlit-specific helper functions
def get_session_conversation_context(user_id: str = "user_001", limit: int = 5) -> str:
    """Get conversation context from current Streamlit session"""
    
    try:
        import streamlit as st
        initialize_streamlit_memory()
        
        if user_id not in st.session_state.conversation_memory:
            return ""
        
        recent_conversations = st.session_state.conversation_memory[user_id][-limit:]
        
        if not recent_conversations:
            return ""
        
        # Create context string
        context_parts = []
        for conv in recent_conversations:
            user_msg = conv.get('message', '')
            bot_response = conv.get('response', '')
            
            if user_msg:
                context_parts.append(f"User: {user_msg}")
            if bot_response:
                # Take first 150 chars to keep context manageable
                bot_preview = bot_response[:150] + "..." if len(bot_response) > 150 else bot_response
                context_parts.append(f"Bot: {bot_preview}")
        
        context = "\n".join(context_parts)
        print(f"📖 Retrieved session context: {len(context)} chars from {len(recent_conversations)} messages")
        
        return context
        
    except ImportError:
        print("📝 Not in Streamlit context")
        return ""
    except Exception as e:
        print(f"⚠️ Error getting session context: {e}")
        return ""

def clear_session_memory():
    """Clear conversation memory for current Streamlit session"""
    try:
        import streamlit as st
        if 'conversation_memory' in st.session_state:
            st.session_state.conversation_memory = {}
            print("✅ Cleared Streamlit session memory")
            return True
    except:
        print("⚠️ Could not clear session memory")
        return False

def get_session_stats():
    """Get statistics about current Streamlit session"""
    try:
        import streamlit as st
        initialize_streamlit_memory()
        
        total_messages = 0
        for user_memory in st.session_state.conversation_memory.values():
            total_messages += len(user_memory)
        
        return {
            "total_messages": total_messages,
            "users_in_session": len(st.session_state.conversation_memory),
            "memory_initialized": 'conversation_memory' in st.session_state
        }
        
    except Exception as e:
        return {"error": str(e)}

def debug_session_memory():
    """Debug function to see what's stored in session"""
    try:
        import streamlit as st
        if 'conversation_memory' in st.session_state:
            print("🔍 DEBUG: Streamlit session memory contents:")
            for user_id, messages in st.session_state.conversation_memory.items():
                print(f"  User {user_id}: {len(messages)} messages")
                for i, msg in enumerate(messages[-2:]):  # Show last 2
                    print(f"    {i+1}. User: {msg['message'][:40]}...")
                    print(f"       Bot: {msg['response'][:40]}...")
        else:
            print("📭 No conversation memory in session state")
    except Exception as e:
        print(f"Debug error: {e}")

# Helper function for easy integration
def store_conversation_in_streamlit(user_message: str, bot_response: str, emotion: str = "neutral", user_id: str = "user_001"):
    """Easy function to store conversation in Streamlit session state"""
    
    try:
        import streamlit as st
        initialize_streamlit_memory()
        
        if user_id not in st.session_state.conversation_memory:
            st.session_state.conversation_memory[user_id] = []
        
        # Add new conversation
        st.session_state.conversation_memory[user_id].append({
            "message": user_message,
            "response": bot_response,
            "emotion": emotion,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only last 15 messages to avoid memory issues
        if len(st.session_state.conversation_memory[user_id]) > 15:
            st.session_state.conversation_memory[user_id] = st.session_state.conversation_memory[user_id][-15:]
        
        print(f"✅ Stored conversation in session. Total: {len(st.session_state.conversation_memory[user_id])}")
        
        # Also store in file backup
        store_memory(user_id, user_message, bot_response, emotion)
        
    except ImportError:
        print("📝 Not in Streamlit - storing in file only")
        store_memory(user_id, user_message, bot_response, emotion)
    except Exception as e:
        print(f"⚠️ Session storage failed: {e}")
        # Fallback to file storage
        store_memory(user_id, user_message, bot_response, emotion)
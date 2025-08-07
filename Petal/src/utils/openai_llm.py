import os
import time
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

# Store memory in session state
if "chat_history" not in globals():
    chat_history = []

# MUCH MORE REASONABLE rate limiting that allows normal usage
last_request_time = 0
min_request_interval = 1  # Reduced from 2 to 1 second
request_count = 0
max_requests_per_minute = 25  # Increased from 12 to 25
daily_request_count = 0
daily_reset_time = time.time()
max_daily_requests = 800  # Increased from 400 to 800

# Reset tracking for minute counter
minute_reset_time = time.time()

def check_rate_limits():
    """Much more reasonable rate limiting that doesn't block legitimate users"""
    global last_request_time, request_count, daily_request_count, daily_reset_time, minute_reset_time
    
    current_time = time.time()
    
    # Reset daily counter if needed (24 hours)
    if current_time - daily_reset_time > 86400:
        daily_request_count = 0
        daily_reset_time = current_time
        request_count = 0
        minute_reset_time = current_time
        print("🔄 Daily quota reset")
    
    # Reset minute counter every 60 seconds
    if current_time - minute_reset_time > 60:
        request_count = 0
        minute_reset_time = current_time
    
    # Check daily limit (much higher now)
    if daily_request_count >= max_daily_requests:
        return False, f"Daily limit reached ({max_daily_requests} requests). Try again tomorrow."
    
    # Check per-minute limit (more reasonable)
    if request_count >= max_requests_per_minute:
        return False, f"Please wait a moment - you've made {request_count} requests this minute."
    
    # Check minimum interval (much shorter)
    time_since_last = current_time - last_request_time
    if time_since_last < min_request_interval:
        wait_time = min_request_interval - time_since_last
        return False, f"Please wait {wait_time:.1f} seconds."
    
    return True, "OK"

def openai_chat(prompt):
    """Enhanced OpenAI chat with better rate limiting and fallback handling"""
    global chat_history, last_request_time, request_count, daily_request_count
    
    # Check rate limits with more reasonable constraints
    can_proceed, message = check_rate_limits()
    if not can_proceed:
        print(f"Rate limit: {message}")
        return None  # Return None to trigger your comprehensive system fallback
    
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

Special response considerations:
- For worried/scared users: Provide extra reassurance and gentle medical guidance
- For emergency symptoms: Give clear medical advice about seeking immediate care
- For first-time experiences: Offer patient, educational, and encouraging responses
- For emotional distress: Provide validation, support, and appropriate mental health resources
- For family questions: Acknowledge their caring nature and provide comprehensive helpful guidance

Always provide complete, caring, medically accurate responses that make users feel heard, supported, and fully informed about their menstrual health."""

    messages = [{"role": "system", "content": system_message}]
    
    # Include more conversation context for better responses
    messages += chat_history[-10:]  # Keep more context
    messages.append({"role": "user", "content": prompt})

    try:
        # Enhanced parameters for comprehensive responses
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.8,  # Natural and warm responses
            max_tokens=700,   # Allow for comprehensive answers
            frequency_penalty=0.3,
            presence_penalty=0.3
        )

        reply = response.choices[0].message.content
        
        # Update conversation history
        chat_history.append({"role": "user", "content": prompt})
        chat_history.append({"role": "assistant", "content": reply})
        
        # Keep reasonable history length
        if len(chat_history) > 20:
            chat_history = chat_history[-20:]
        
        # Update rate limiting counters
        last_request_time = time.time()
        request_count += 1
        daily_request_count += 1
        
        print(f"✅ OpenAI success. Daily: {daily_request_count}/{max_daily_requests}, Minute: {request_count}/{max_requests_per_minute}")
        
        return reply
        
    except Exception as e:
        error_msg = str(e)
        print(f"OpenAI API error: {error_msg}")
        
        # Update counters even on error to prevent spam
        last_request_time = time.time()
        
        # Handle specific error types gracefully
        if "429" in error_msg or "rate_limit" in error_msg.lower():
            print("🔄 OpenAI rate limited - triggering fallback to comprehensive system")
            return None  # Trigger comprehensive system fallback
        elif "quota" in error_msg.lower() or "billing" in error_msg.lower():
            print("💳 OpenAI quota/billing issue - triggering fallback to comprehensive system")
            return None  # Trigger comprehensive system fallback
        elif "invalid" in error_msg.lower() and "api" in error_msg.lower():
            print("🔑 OpenAI API key issue - triggering fallback to comprehensive system")
            return None  # Trigger comprehensive system fallback
        else:
            print("⚠️ OpenAI general error - triggering fallback to comprehensive system")
            return None  # Let system use comprehensive fallback methods

def get_quota_status():
    """Check current quota usage status with detailed information"""
    current_time = time.time()
    
    return {
        "daily_requests": daily_request_count,
        "max_daily": max_daily_requests,
        "requests_remaining": max_daily_requests - daily_request_count,
        "minute_requests": request_count,
        "max_per_minute": max_requests_per_minute,
        "last_request": last_request_time,
        "time_since_last": current_time - last_request_time,
        "can_make_request": check_rate_limits()[0],
        "daily_usage_percent": (daily_request_count / max_daily_requests) * 100,
        "minute_usage_percent": (request_count / max_requests_per_minute) * 100
    }

def reset_quota_counters():
    """Reset quota counters - useful for testing and development"""
    global daily_request_count, request_count, last_request_time, daily_reset_time, minute_reset_time
    daily_request_count = 0
    request_count = 0
    last_request_time = 0
    daily_reset_time = time.time()
    minute_reset_time = time.time()
    print("✅ All quota counters reset - ready for fresh testing")

def force_reset_if_stuck():
    """Force reset if counters seem stuck"""
    global daily_request_count, request_count, last_request_time
    
    current_time = time.time()
    
    # If it's been more than 2 minutes since last request, reset minute counter
    if current_time - last_request_time > 120:
        request_count = 0
        print("🔄 Auto-reset minute counter (2+ minutes since last request)")
    
    # If daily counter seems stuck (more than 25 hours), reset it
    if current_time - daily_reset_time > 90000:  # 25 hours
        daily_request_count = 0
        daily_reset_time = current_time
        print("🔄 Auto-reset daily counter (25+ hours)")

def test_openai_connection():
    """Test OpenAI connection and quota status with detailed feedback"""
    print("🧪 Testing OpenAI connection...")
    
    if not api_key:
        print("❌ No API key found - check your .env file")
        return False
    
    if not api_key.startswith('sk-'):
        print("❌ Invalid API key format - should start with 'sk-'")
        return False
    
    print(f"🔑 API key format looks correct: sk-...{api_key[-8:]}")
    
    try:
        # Simple test call
        test_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Test"}],
            max_tokens=10
        )
        print("✅ OpenAI connection successful!")
        print(f"📝 Test response: {test_response.choices[0].message.content}")
        return True
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ OpenAI connection failed: {error_msg}")
        
        if "401" in error_msg:
            print("🔑 API key authentication failed - check your key")
        elif "429" in error_msg:
            print("⏱️ Rate limited - try again in a moment")
        elif "quota" in error_msg.lower():
            print("💳 Quota exceeded - check your OpenAI billing")
        else:
            print("⚠️ Other connection issue - check internet/OpenAI status")
        
        return False

def get_detailed_status():
    """Get detailed status of the OpenAI system"""
    status = get_quota_status()
    
    print("📊 DETAILED OPENAI STATUS")
    print("=" * 40)
    print(f"Daily usage: {status['daily_requests']}/{status['max_daily']} ({status['daily_usage_percent']:.1f}%)")
    print(f"Minute usage: {status['minute_requests']}/{status['max_per_minute']} ({status['minute_usage_percent']:.1f}%)")
    print(f"Time since last request: {status['time_since_last']:.1f} seconds")
    print(f"Can make request: {'✅ YES' if status['can_make_request'] else '❌ NO'}")
    
    if not status['can_make_request']:
        if status['daily_requests'] >= status['max_daily']:
            print("⚠️ Daily limit reached - wait until tomorrow")
        elif status['minute_requests'] >= status['max_per_minute']:
            print("⚠️ Minute limit reached - wait up to 60 seconds")
        elif status['time_since_last'] < min_request_interval:
            wait_time = min_request_interval - status['time_since_last']
            print(f"⚠️ Too soon since last request - wait {wait_time:.1f} seconds")
    
    return status

if __name__ == "__main__":
    print("🔧 ENHANCED OPENAI_LLM SYSTEM")
    print("=" * 50)
    
    # Test the connection
    connection_ok = test_openai_connection()
    
    if connection_ok:
        print("\n✅ OpenAI connection working!")
    
    # Show detailed status
    print()
    get_detailed_status()
    
    print(f"\n🚀 IMPROVEMENTS MADE:")
    print(f"✅ Increased daily limit: 50 → 800 requests")
    print(f"✅ Increased minute limit: 12 → 25 requests") 
    print(f"✅ Reduced interval: 2 → 1 second")
    print(f"✅ Better error handling and fallbacks")
    print(f"✅ Auto-reset when counters get stuck")
    print(f"✅ Detailed status monitoring")
    
    print(f"\n💡 KEY CHANGES:")
    print(f"• Much higher limits for normal usage")
    print(f"• Returns None on rate limits (triggers your comprehensive system)")
    print(f"• Better tracking and auto-reset capabilities")
    print(f"• Comprehensive system messages for better responses")
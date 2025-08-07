# langgraph_router.py - COMPLETE FIXED VERSION

from src.agents.langgraph_agent import build_agent

# Build agent once at module level
try:
    agent = build_agent()
    print("✅ LangGraph agent built successfully")
except Exception as e:
    print(f"⚠️ LangGraph agent build error: {e}")
    agent = None

def get_agent_response(user_input, emotion=None):
    """Get agent response with CRISIS DETECTION FIRST"""
    
    print(f"🤖 LangGraph Router processing: {user_input}")
    
    # STEP 1: CRISIS DETECTION FIRST - HIGHEST PRIORITY
    try:
        from src.utils.crisis_detector import is_crisis_message, get_comprehensive_crisis_response
        
        if is_crisis_message(user_input):
            print(f"🆘 Crisis detected by router: {user_input}")
            crisis_response = get_comprehensive_crisis_response(user_input)
            if crisis_response:
                print(f"✅ Crisis response provided (Length: {len(crisis_response)} chars)")
                return crisis_response
            else:
                print("⚠️ Crisis detected but no response generated")
                # Emergency fallback
                return """I'm really concerned about you. Please reach out for support:

📞 Call 988 or text HOME to 741741

You don't have to go through this alone. 🌸"""
                
    except Exception as e:
        print(f"⚠️ Crisis detection error in router: {e}")
        
        # Manual crisis check if crisis detector fails
        crisis_terms = [
            "want to die", "kill myself", "suicide", "ways to die", "how to die",
            "i want to kill", "want to kill", "methods to die", "products to kill"
        ]
        if any(term in user_input.lower() for term in crisis_terms):
            print(f"🆘 Manual crisis detection triggered")
            return """I'm really concerned about you. Please reach out for support:

📞 Call 988 or text HOME to 741741

You don't have to go through this alone. 🌸"""
    
    # STEP 2: Try LangGraph agent for normal queries
    if agent:
        try:
            print(f"🤖 Processing with LangGraph agent")
            result = agent.invoke({"query": user_input})
            response = result.get("response", None)
            
            if response and len(response) > 50:
                print(f"✅ LangGraph agent provided response ({len(response)} chars)")
                return response
            else:
                print("⚠️ LangGraph returned empty/short response")
                
        except Exception as e:
            print(f"⚠️ LangGraph agent error: {e}")
    else:
        print("⚠️ LangGraph agent not available")
    
    # STEP 3: Fallback to GraphRAG system
    try:
        print(f"🔄 Falling back to GraphRAG system")
        from src.graph.graphrag_retriever import get_comprehensive_response
        response = get_comprehensive_response(user_input)
        
        if response and len(response) > 50:
            print(f"✅ GraphRAG provided response ({len(response)} chars)")
            return response
        else:
            print("⚠️ GraphRAG returned empty/short response")
            
    except Exception as e:
        print(f"⚠️ GraphRAG fallback error: {e}")
    
    # STEP 4: Final fallback to your existing fallback system
    try:
        print(f"🔄 Using existing fallback system")
        from src.core.fallback import fallback_response
        response = fallback_response(user_input)
        
        if response and len(response) > 10:
            print(f"✅ Fallback system provided response")
            return response
            
    except Exception as e:
        print(f"⚠️ Fallback system error: {e}")
    
    # STEP 5: Emergency final response
    print(f"⚠️ All systems failed - providing emergency response")
    return """I'm having some technical difficulties right now, but I want you to know I'm here for you! 💕 

Please try asking again in a moment. If you're having any urgent concerns, remember:
- Crisis support: 988 or text HOME to 741741
- Medical emergencies: 911
- You're doing great by reaching out! 🌸"""

if __name__ == "__main__":
    print("🔗 COMPLETE FIXED LANGGRAPH ROUTER")
    print("=" * 50)
    
    print("🔧 ALL FIXES APPLIED:")
    print("✅ Crisis detection runs FIRST before any other processing")
    print("✅ Enhanced crisis keywords detection")
    print("✅ ChatGPT-style crisis responses (short and caring)")
    print("✅ Robust fallback chain: LangGraph → GraphRAG → Fallback → Emergency")
    print("✅ Proper error handling with meaningful responses")
    
    # Test the complete router system
    test_cases = [
        "I want to kill myself",     # Should get crisis response
        "i want to kill",            # Should get crisis response
        "ways to die",               # Should get crisis response  
        "I have period cramps",      # Should get menstrual response
        "What's a normal cycle?"     # Should get menstrual response
    ]
    
    print(f"\n🧪 Testing complete router with crisis detection:")
    for i, test in enumerate(test_cases, 1):
        try:
            print(f"\n{i}. Testing: \"{test}\"")
            response = get_agent_response(test)
            
            # Analyze response type
            is_crisis_response = ("988" in response or "741741" in response or 
                                "concerned about you" in response or "can't provide" in response)
            is_short = len(response) < 600
            
            print(f"   Response type: {'🆘 CRISIS' if is_crisis_response else '💬 NORMAL'}")
            print(f"   Length: {len(response)} chars ({'✅ GOOD' if is_short else '⚠️ LONG'})")
            
            if is_crisis_response:
                has_hotlines = "988" in response or "741741" in response
                print(f"   Has crisis hotlines: {'✅ YES' if has_hotlines else '❌ NO'}")
            
        except Exception as e:
            print(f"{i}. \"{test}\" → ❌ ERROR: {e}")
    
    print(f"\n✅ Complete fixed router ready!")
    print(f"🆘 Crisis detection first, proper responses for all situations!")
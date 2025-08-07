# debug_tracer.py - Track where answers come from in your Petal system

import sys
import os
from datetime import datetime

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

def trace_answer_source(query: str):
    """Trace exactly where your answer comes from"""
    
    print("🔍 PETAL ANSWER SOURCE TRACER")
    print("=" * 60)
    print(f"Query: '{query}'")
    print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 60)
    
    # Step 1: Test menstrual detection
    try:
        from src.graph.graphrag_retriever import is_menstrual_related
        is_menstrual = is_menstrual_related(query)
        print(f"🔍 STEP 1 - Menstrual Detection: {'✅ YES' if is_menstrual else '❌ NO'}")
        
        if not is_menstrual:
            print("📝 RESULT: Will get REDIRECT message")
            return "redirect"
    except Exception as e:
        print(f"❌ STEP 1 ERROR: {e}")
    
    # Step 2: Test input sanitizer
    try:
        from src.utils.input_sanitizer import sanitize_input
        clean_query = sanitize_input(query)
        if clean_query.startswith("[🚫"):
            print(f"🛡️ STEP 2 - Security: BLOCKED - {clean_query}")
            return "blocked"
        else:
            print(f"🛡️ STEP 2 - Security: ✅ PASSED")
    except Exception as e:
        print(f"❌ STEP 2 ERROR: {e}")
    
    # Step 3: Test crisis detection
    try:
        from src.utils.crisis_detector import is_crisis_message
        is_crisis = is_crisis_message(query)
        print(f"🆘 STEP 3 - Crisis Detection: {'⚠️ CRISIS' if is_crisis else '✅ NORMAL'}")
        
        if is_crisis:
            print("📝 RESULT: Will get CRISIS response")
            return "crisis"
    except Exception as e:
        print(f"❌ STEP 3 ERROR: {e}")
    
    # Step 4: Test emotion detection
    try:
        from src.core.emotion import detect_emotion
        emotion = detect_emotion(query)
        print(f"💭 STEP 4 - Emotion: {emotion}")
    except Exception as e:
        print(f"❌ STEP 4 ERROR: {e}")
    
    # Step 5: Test OpenAI availability
    try:
        from src.utils.openai_llm import openai_chat
        test_response = openai_chat("test")
        openai_available = test_response is not None
        print(f"🤖 STEP 5 - OpenAI: {'✅ AVAILABLE' if openai_available else '❌ UNAVAILABLE'}")
    except Exception as e:
        print(f"❌ STEP 5 ERROR: {e}")
        openai_available = False
    
    # Step 6: Test medical database content
    print(f"\n📚 STEP 6 - MEDICAL CONTENT SOURCES:")
    
    # Test FAISS database
    faiss_available = os.path.exists("src/graph/faiss_index")
    print(f"   FAISS Database: {'✅ EXISTS' if faiss_available else '❌ MISSING'}")
    
    # Test raw medical content
    raw_content_available = False
    if os.path.exists("src/graph/raw_medical_content"):
        files = [f for f in os.listdir("src/graph/raw_medical_content") if f.endswith('.txt')]
        raw_content_available = len(files) > 0
        print(f"   Raw Medical Files: {'✅ ' + str(len(files)) + ' files' if raw_content_available else '❌ NONE'}")
    else:
        print(f"   Raw Medical Files: ❌ DIRECTORY MISSING")
    
    # Test backup database
    backup_available = os.path.exists("src/graph/faiss_medical_backup")
    print(f"   Backup Database: {'✅ EXISTS' if backup_available else '❌ MISSING'}")
    
    # Step 7: Test actual content retrieval
    print(f"\n🔍 STEP 7 - CONTENT RETRIEVAL TEST:")
    
    try:
        from src.graph.graphrag_retriever import get_comprehensive_response
        print("   Calling get_comprehensive_response()...")
        
        # This will show us the actual path
        response = get_comprehensive_response(query)
        
        if response:
            response_length = len(response)
            print(f"   ✅ Got response: {response_length} characters")
            
            # Analyze response type
            if "I'm Petal, your menstrual health companion" in response:
                print("   📝 RESPONSE TYPE: REDIRECT (not menstrual health)")
                return "redirect"
            elif "🚨" in response or "crisis" in response.lower():
                print("   📝 RESPONSE TYPE: CRISIS SUPPORT")
                return "crisis"
            elif "Medical info from trusted sources" in response:
                print("   📝 RESPONSE TYPE: MEDICAL KNOWLEDGE")
                return "medical"
            elif "I want to help" in response:
                print("   📝 RESPONSE TYPE: FALLBACK")
                return "fallback"
            else:
                print("   📝 RESPONSE TYPE: DYNAMIC/OTHER")
                return "dynamic"
        else:
            print("   ❌ No response received")
            return "error"
            
    except Exception as e:
        print(f"   ❌ STEP 7 ERROR: {e}")
        return "error"

def test_langgraph_path(query: str):
    """Test the full LangGraph agent path"""
    
    print(f"\n🔗 LANGGRAPH AGENT PATH TEST:")
    print("-" * 40)
    
    try:
        from langgraph_router import get_agent_response
        print("   Calling LangGraph agent...")
        
        response = get_agent_response(query)
        
        if response:
            print(f"   ✅ LangGraph response: {len(response)} characters")
            return response
        else:
            print("   ❌ LangGraph returned no response")
            return None
            
    except Exception as e:
        print(f"   ❌ LangGraph error: {e}")
        return None

def full_system_trace(query: str):
    """Complete system trace"""
    
    print("🌸 PETAL SYSTEM FULL TRACE")
    print("=" * 60)
    
    # Trace GraphRAG path
    graphrag_result = trace_answer_source(query)
    
    # Trace LangGraph path
    langgraph_response = test_langgraph_path(query)
    
    # Summary
    print(f"\n📊 TRACE SUMMARY:")
    print(f"   GraphRAG Path: {graphrag_result}")
    print(f"   LangGraph Response: {'✅ SUCCESS' if langgraph_response else '❌ FAILED'}")
    
    # Show actual response preview
    if langgraph_response:
        preview = langgraph_response[:200] + "..." if len(langgraph_response) > 200 else langgraph_response
        print(f"\n📝 RESPONSE PREVIEW:")
        print(f"   {preview}")
    
    return graphrag_result, langgraph_response

def debug_specific_query():
    """Interactive debugging for specific queries"""
    
    print("🧪 INTERACTIVE QUERY DEBUGGER")
    print("=" * 40)
    print("Enter queries to trace (type 'quit' to exit)")
    
    while True:
        query = input("\n💬 Query: ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            break
        
        if not query:
            continue
        
        print()
        full_system_trace(query)
        print("-" * 60)

if __name__ == "__main__":
    
    # Test common queries
    test_queries = [
        "I want to punch something during my period",
        "Why is my vagina angry today?", 
        "I bled all over my jeans",
        "What's a normal cycle length?",
        "I'm scared about heavy bleeding"
    ]
    
    print("🧪 TESTING COMMON QUERIES:")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n🔍 TESTING: '{query}'")
        result = trace_answer_source(query)
        print(f"📝 SOURCE: {result}")
        print("-" * 40)
    
    # Interactive mode
    print(f"\n🎯 Want to test specific queries?")
    answer = input("Run interactive debugger? (y/n): ").strip().lower()
    
    if answer in ['y', 'yes']:
        debug_specific_query()
    
    print("\n🌸 Debug session complete!")
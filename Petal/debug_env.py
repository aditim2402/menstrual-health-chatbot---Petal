# debug_env.py - Run this to check your environment setup

import os
from dotenv import load_dotenv

def debug_environment():
    """Debug environment variable loading issues"""
    
    print("🔍 DEBUGGING ENVIRONMENT SETUP")
    print("=" * 40)
    
    # Check if .env file exists
    env_file_path = ".env"
    if os.path.exists(env_file_path):
        print("✅ .env file found")
        
        # Read .env file content
        try:
            with open(env_file_path, 'r') as f:
                env_content = f.read()
            print(f"📄 .env file content ({len(env_content)} characters):")
            
            # Show content but hide the actual key for security
            lines = env_content.split('\n')
            for line in lines:
                if line.strip():
                    if 'OPENAI_API_KEY' in line:
                        if '=' in line:
                            key_part = line.split('=')[1]
                            if key_part.strip():
                                print(f"   OPENAI_API_KEY=sk-...{key_part[-8:]} (key present)")
                            else:
                                print("   ❌ OPENAI_API_KEY= (empty value)")
                        else:
                            print("   ❌ OPENAI_API_KEY line malformed (no =)")
                    else:
                        print(f"   {line}")
        
        except Exception as e:
            print(f"❌ Error reading .env file: {e}")
    
    else:
        print("❌ .env file not found in current directory")
        print(f"   Current directory: {os.getcwd()}")
        print("   Expected location: .env")
    
    print("\n🔄 Testing dotenv loading...")
    
    # Test loading environment
    try:
        load_dotenv()
        print("✅ dotenv.load_dotenv() executed successfully")
    except Exception as e:
        print(f"❌ dotenv loading failed: {e}")
    
    # Check if key is available in environment
    print("\n🔑 API Key Environment Check:")
    api_key = os.getenv("OPENAI_API_KEY")
    
    if api_key:
        if api_key.startswith('sk-'):
            print(f"✅ OpenAI API key found: sk-...{api_key[-8:]}")
            print(f"   Key length: {len(api_key)} characters")
            
            # Test if key format looks correct
            if len(api_key) > 40:
                print("✅ Key length looks correct")
            else:
                print("⚠️ Key might be too short")
                
        else:
            print(f"❌ API key doesn't start with 'sk-': {api_key[:10]}...")
    else:
        print("❌ No OPENAI_API_KEY found in environment")
    
    # Check all environment variables
    print("\n📋 All Environment Variables:")
    all_env_vars = dict(os.environ)
    openai_vars = {k: v for k, v in all_env_vars.items() if 'OPENAI' in k.upper()}
    
    if openai_vars:
        for key, value in openai_vars.items():
            if 'API' in key:
                print(f"   {key}: {value[:8]}...{value[-4:] if len(value) > 12 else 'short'}")
            else:
                print(f"   {key}: {value}")
    else:
        print("   No OpenAI-related environment variables found")
    
    print("\n🧪 Test OpenAI Connection:")
    if api_key and api_key.startswith('sk-'):
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            
            # Simple test call
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            print("✅ OpenAI API connection successful!")
            
        except Exception as e:
            print(f"❌ OpenAI API connection failed: {str(e)[:100]}...")
    else:
        print("❌ Cannot test - no valid API key")
    
    print("\n🛠️ RECOMMENDATIONS:")
    
    if not os.path.exists(".env"):
        print("1. Create .env file in your project root directory")
        print("2. Add: OPENAI_API_KEY=your_key_here")
    elif not api_key:
        print("1. Check .env file format - should be: OPENAI_API_KEY=sk-...")
        print("2. No spaces around the = sign")
        print("3. No quotes around the key")
    elif not api_key.startswith('sk-'):
        print("1. Get a valid OpenAI API key from platform.openai.com")
        print("2. Make sure it starts with 'sk-'")
    else:
        print("✅ Environment looks good - the issue might be elsewhere")
    
    return api_key is not None and api_key.startswith('sk-')

if __name__ == "__main__":
    success = debug_environment()
    
    if success:
        print("\n🎉 Environment setup looks good!")
        print("💡 If still having issues, the problem might be in the database loading")
    else:
        print("\n❌ Environment issues found - fix the recommendations above")
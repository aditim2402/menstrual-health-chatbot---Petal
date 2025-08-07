import os
from datetime import datetime
import re

# Directory and log file setup
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

CRISIS_LOG_FILE = os.path.join(LOG_DIR, "crisis_events.log")
ERROR_LOG_FILE = os.path.join(LOG_DIR, "errors.txt")
FEEDBACK_LOG_FILE = os.path.join(LOG_DIR, "feedback.txt")

def anonymize(text):
    """Anonymize sensitive data in log messages"""
    text = re.sub(r"\b\d{10,16}\b", "[PHONE/ID REDACTED]", text)
    text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", "[EMAIL REDACTED]", text)
    return text

def log_event(filename: str, message: str) -> None:
    """
    Generic logger to append a message to a specified log file with improved error handling.

    Args:
        filename (str): Name of the file inside the logs directory.
        message (str): Message to log.
    """
    try:
        # Ensure logs directory exists
        os.makedirs(LOG_DIR, exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        filepath = os.path.join(LOG_DIR, filename)
        
        # Anonymize sensitive data
        safe_message = anonymize(message)

        # Create file if it doesn't exist with header
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(f"# {filename} - Created {timestamp}\n")
                f.write(f"# Petal App Logs\n\n")

        # Append the log entry
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {safe_message.strip()}\n")
        
        print(f"✅ Logged to {filepath}: {safe_message[:50]}...")
        
    except Exception as e:
        print(f"❌ Logging error for {filename}: {str(e)}")
        # Fallback - try to write to current directory
        try:
            fallback_file = f"fallback_{filename}"
            with open(fallback_file, "a", encoding="utf-8") as f:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"[{timestamp}] FALLBACK LOG: {safe_message.strip()}\n")
            print(f"✅ Fallback log created: {fallback_file}")
        except:
            print(f"❌ Complete logging failure for: {safe_message[:50]}")

def log_error(error_msg: str) -> None:
    """
    Log general errors to errors.txt.

    Args:
        error_msg (str): Error message to log.
    """
    try:
        log_event("errors.txt", f"ERROR: {error_msg}")
    except:
        print(f"Failed to log error: {error_msg}")

def log_crisis(user_id: str, message: str) -> None:
    """
    Log user crisis messages to crisis_events.log with enhanced security.

    Args:
        user_id (str): Identifier of the user.
        message (str): The crisis-related message.
    """
    try:
        # Anonymize the crisis message for privacy
        safe_message = anonymize(message)
        log_entry = f"UserID: {user_id} | CRISIS MESSAGE: {safe_message}"
        log_event("crisis_events.log", log_entry)
        
        # Also log to errors for immediate attention
        log_event("errors.txt", f"CRISIS DETECTED - UserID: {user_id}")
        
    except Exception as e:
        print(f"❌ Crisis logging failed: {str(e)}")
        # This is critical, so try direct file write
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("CRISIS_BACKUP.log", "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] CRISIS - UserID: {user_id} | Error: {str(e)}\n")
        except:
            print(f"❌ CRITICAL: Crisis logging completely failed")

def log_feedback(feedback_type: str, feedback_text: str, user_id: str = "anonymous") -> bool:
    """
    Log user feedback with improved error handling and privacy protection.
    
    Args:
        feedback_type (str): Type of feedback (e.g., "💡 Suggestion")
        feedback_text (str): Feedback content
        user_id (str): User identifier (optional)
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Anonymize feedback for privacy
        safe_feedback = anonymize(feedback_text.strip())
        
        # Create comprehensive log entry
        log_entry = f"UserID: {user_id} | Type: {feedback_type} | Feedback: {safe_feedback}"
        
        log_event("feedback.txt", log_entry)
        
        print(f"✅ Feedback logged successfully: {feedback_type}")
        return True
        
    except Exception as e:
        print(f"❌ Feedback logging failed: {str(e)}")
        
        # Emergency fallback for feedback
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("feedback_backup.txt", "a", encoding="utf-8") as f:
                f.write(f"[{timestamp}] BACKUP - Type: {feedback_type} | Text: {feedback_text[:100]}\n")
            print("✅ Feedback saved to backup file")
            return True
        except:
            print("❌ Complete feedback logging failure")
            return False

def log_mood(user_id: str, mood: str) -> None:
    """
    Log user mood tracking.
    
    Args:
        user_id (str): User identifier
        mood (str): Mood selection
    """
    try:
        log_entry = f"UserID: {user_id} | Mood: {mood}"
        log_event("mood_logs.txt", log_entry)
    except Exception as e:
        print(f"❌ Mood logging failed: {str(e)}")

def get_log_stats() -> dict:
    """
    Get statistics about log files for debugging.
    
    Returns:
        dict: Statistics about each log file
    """
    stats = {}
    
    for filename in ["feedback.txt", "mood_logs.txt", "errors.txt", "crisis_events.log"]:
        filepath = os.path.join(LOG_DIR, filename)
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                stats[filename] = {
                    'exists': True,
                    'lines': len(lines),
                    'size_kb': round(os.path.getsize(filepath) / 1024, 2)
                }
            except:
                stats[filename] = {'exists': True, 'lines': 'Error reading', 'size_kb': 0}
        else:
            stats[filename] = {'exists': False, 'lines': 0, 'size_kb': 0}
    
    return stats

# Test function to verify logging works
def test_logging():
    """Test function to verify all logging functions work"""
    print("🧪 Testing logging functions...")
    
    try:
        log_event("test.txt", "Test message")
        log_feedback("💡 Test", "This is a test feedback", "test_user")
        log_mood("test_user", "😊 Good")
        
        stats = get_log_stats()
        print("📊 Log statistics:")
        for filename, stat in stats.items():
            print(f"  {filename}: {stat}")
        
        print("✅ Logging test completed")
        
    except Exception as e:
        print(f"❌ Logging test failed: {str(e)}")

if __name__ == "__main__":
    test_logging()
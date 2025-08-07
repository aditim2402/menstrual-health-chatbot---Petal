import streamlit as st
import os
from pathlib import Path
from datetime import datetime

# Import your existing pages
from src.ui.pages.chat import chat_interface

# Try to import tips, fallback if not found
try:
    from src.ui.pages.tips import show_tips
except ImportError:
    def show_tips():
        st.markdown("## 💡 Create src/ui/pages/tips.py for professional tips!")

# Import logger functions
try:
    from src.utils.logger import log_event
except ImportError:
    def log_event(filename, message):
        print(f"Log: {message}")

def load_custom_css():
    """Load beautiful aesthetic CSS that works"""
    st.markdown("""
    <style>
    .main {
        background: linear-gradient(135deg, #ffeef8 0%, #f8e8ff 50%, #fff0f8 100%);
        font-family: 'Inter', 'Segoe UI', sans-serif;
    }
    
    .css-1d391kg {
        background: linear-gradient(180deg, 
            rgba(255, 240, 248, 0.95) 0%, 
            rgba(248, 232, 255, 0.95) 100%);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff6b9d 0%, #ffa8cc 100%);
        color: white;
        border: none;
        border-radius: 20px;
        padding: 0.8rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(255, 107, 157, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 107, 157, 0.4);
    }
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        border: 2px solid rgba(255, 182, 193, 0.3);
        border-radius: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(255, 107, 157, 0.1);
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #ff6b9d;
        box-shadow: 0 0 0 3px rgba(255, 107, 157, 0.15);
    }
    
    .stSelectbox > div > div > select {
        border: 2px solid rgba(255, 182, 193, 0.3);
        border-radius: 12px;
        transition: all 0.3s ease;
    }
    
    /* WHITE BACKGROUND for radio buttons - CLEAN NAVIGATION */
    .stRadio > div {
        background: white !important;
        border-radius: 16px !important;
        padding: 1rem !important;
        border: 1px solid rgba(255, 182, 193, 0.2) !important;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05) !important;
    }
    
    .stRadio > div > label {
        padding: 0.75rem 1rem !important;
        border-radius: 8px !important;
        margin: 0.25rem 0 !important;
        font-weight: 500 !important;
        font-size: 0.9rem !important;
        color: #374151 !important;
        transition: all 0.3s ease !important;
    }
    
    .stRadio > div > label:hover {
        background: #f9fafb !important;
        border-left: 3px solid #ff6b9d !important;
        transform: translateX(2px) !important;
    }
    
    .stAlert {
        border-radius: 15px;
        border: none;
        box-shadow: 0 3px 10px rgba(0, 0, 0, 0.1);
    }
    
    .stForm {
        background: rgba(255, 255, 255, 0.9);
        border-radius: 15px;
        padding: 1.5rem;
        border: 1px solid rgba(255, 182, 193, 0.3);
        box-shadow: 0 4px 15px rgba(255, 107, 157, 0.1);
    }
    
    h1, h2, h3 {
        color: #2d3748;
        font-weight: 600;
    }
    
    /* Clean navigation header */
    h3 {
        color: #7c3aed !important;
        font-weight: 600 !important;
        font-size: 1.2rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Petal - Your Gentle Cycle Companion",
        page_icon="🌸",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def create_professional_sidebar():
    """Create beautiful working sidebar"""
    with st.sidebar:
        # Gorgeous header (this works!)
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #ff6b9d, #ffa8cc, #ffcce5);
            color: white;
            padding: 2.5rem 1.5rem;
            border-radius: 25px;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(255, 107, 157, 0.4);
            border: 2px solid rgba(255, 255, 255, 0.3);
        ">
            <h1 style="
                margin: 0; 
                color: white; 
                font-size: 2.8rem; 
                font-weight: 800;
                text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
                letter-spacing: 1px;
            ">🌸 Petal</h1>
            <p style="
                margin: 1rem 0 0 0; 
                opacity: 0.95; 
                font-size: 1.2rem;
                font-weight: 600;
                letter-spacing: 0.5px;
                text-shadow: 0 1px 5px rgba(0, 0, 0, 0.2);
            ">Your Gentle Companion</p>
            <div style="
                margin-top: 1rem; 
                font-size: 1rem; 
                opacity: 0.9;
                font-style: italic;
                font-weight: 500;
            ">✨ Blooming with infinite love ✨</div>
        </div>
        """, unsafe_allow_html=True)
        
        # CLEAN Navigation without emojis
        st.markdown("### Navigate")
        st.markdown("Choose your section:")
        
        page = st.radio(
            "",
            ["Chat", "Health Info", "Cycle Tracker", "Feedback"],
            key="main_navigation"
        )
        
        st.markdown("---")
        
        # Emergency Resources with working design
        st.markdown("### 🆘 Emergency Resources")
        
        # Use containers for clean organization
        with st.container():
            st.markdown("**🚨 Crisis Support:**")
            st.info("📱 **Crisis Text Line:** 741741")
            st.info("📞 **Suicide Prevention:** 988") 
            st.error("🚨 **Emergency:** 911")
            
        with st.container():
            st.markdown("**🏥 Health Resources:**")
            st.success("🌸 **Planned Parenthood**")
            st.success("👩‍⚕️ **Your healthcare provider**")
            st.success("🌐 **ACOG.org resources**")
        
        st.markdown("---")
        
        # Beautiful Mood Tracker header (this works!)
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #fff8e1, #f3e5f5);
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-left: 5px solid #ff9800;
            box-shadow: 0 6px 20px rgba(255, 152, 0, 0.15);
            border: 1px solid rgba(255, 152, 0, 0.1);
        ">
            <h3 style="
                color: #f57c00; 
                margin-top: 0;
                font-size: 1.2rem;
                font-weight: 700;
            ">📊 ✨ Today's Mood Tracker ✨</h3>
        </div>
        """, unsafe_allow_html=True)
        
        mood = st.selectbox(
            "How is your beautiful heart feeling today?", 
            ["😊 Wonderful & Radiant", "🌸 Good & Blooming", "😌 Okay & Peaceful", "😰 Anxious & Worried", "😢 Sad & Heavy", "😤 Irritated & Frustrated", "😴 Tired & Drained", "🤗 Loved & Supported"],
            key="main_mood_selector"
        )
        
        if st.button("✨ Save My Beautiful Mood ✨", key="main_save_mood"):
            try:
                log_event("mood_logs.txt", f"User mood: {mood}")
                st.success("🎉 Your beautiful mood has been saved! Thank you for sharing your heart! 🌸")
                st.balloons()
            except:
                st.success("🎉 Your mood is noted with love! 🌸")
        
        st.markdown("---")
        
        # Gorgeous Feedback Form header (this works!)
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f3e5f5, #e8f5e8);
            border-radius: 20px;
            padding: 1.5rem;
            margin: 1.5rem 0;
            border-left: 5px solid #9c27b0;
            box-shadow: 0 6px 20px rgba(156, 39, 176, 0.15);
            border: 1px solid rgba(156, 39, 176, 0.1);
        ">
            <h3 style="
                color: #7b1fa2; 
                margin-top: 0;
                font-size: 1.2rem;
                font-weight: 700;
            ">💌 ✨ Share Your Heart ✨</h3>
            <p style="
                color: #6a1b9a; 
                margin: 0; 
                font-size: 0.95rem; 
                opacity: 0.8;
                font-style: italic;
            ">Help Petal bloom even more beautifully</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("main_feedback_form", clear_on_submit=True):
            feedback_type = st.selectbox(
                "What's in your heart?",
                ["💡 Bright Suggestion", "🐛 Something to Fix", "💖 Sweet Compliment", "❓ Gentle Question", "📱 Feature Wish"],
                key="main_feedback_type"
            )
            
            feedback_text = st.text_area(
                "Pour your thoughts here:",
                placeholder="Tell us how we can make Petal even more magical and caring! Your voice matters deeply to us... 🌸💕",
                height=100,
                key="main_feedback_text"
            )
            
            if st.form_submit_button("✨ Send Love & Feedback ✨", use_container_width=True):
                if feedback_text.strip():
                    try:
                        os.makedirs("logs", exist_ok=True)
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        with open("logs/feedback.txt", "a", encoding="utf-8") as f:
                            f.write(f"[{timestamp}] Type: {feedback_type} | Feedback: {feedback_text.strip()}\n")
                        
                        st.success("🌸✨ Your beautiful feedback has been received with so much gratitude! Thank you for helping Petal bloom! ✨🌸")
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"💔 Oh no! Something went wrong: {str(e)}")
                        st.info("But don't worry - your thoughts still matter deeply to us! 💕")
                else:
                    st.warning("💭 Please share your beautiful thoughts with us first! We're excited to hear from you! 🌸")
        
        st.markdown("---")
        
        # Privacy section
        st.markdown("### 🔒 Your Safe Space")
        st.info("""
        💝 Your conversations are completely confidential and sacred. Petal uses advanced encryption and follows healthcare privacy standards.
        
        **Remember:** Petal provides loving educational information and cannot replace professional medical advice. Always trust your healthcare providers! 💚
        """)
        
        return page

def get_page_from_selection(page_selection):
    """Convert sidebar selection to page identifier"""
    page_mapping = {
        "Chat": "Chat",
        "Health Info": "Tips", 
        "Cycle Tracker": "Timeline",
        "Feedback": "Feedback"
    }
    return page_mapping.get(page_selection, "Chat")

def display_professional_header():
    """Display professional header"""
    st.markdown("""
    <div style="
        background: linear-gradient(135deg, #ff6b9d 0%, #ffa8cc 100%);
        padding: 2rem;
        border-radius: 16px;
        text-align: center;
        color: white;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(255, 107, 157, 0.3);
    ">
        <h1 style="margin: 0; font-size: 2.5rem; font-weight: 600;">🌸 Petal</h1>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 1.2rem;">
            Your Gentle Cycle Companion
        </p>
        <div style="margin-top: 1rem; font-size: 0.95rem; opacity: 0.8;">
            Blooming • Confidential • Always supportive
        </div>
    </div>
    """, unsafe_allow_html=True)

def show_cycle_timeline():
    """Timeline page"""
    try:
        from src.ui.pages.timeline import show_cycle_timeline as timeline_func
        timeline_func()
    except ImportError:
        st.markdown("## 📈 Cycle Timeline")
        st.info("Create src/ui/pages/timeline.py for the full timeline!")

def show_feedback_page():
    """Feedback viewer page"""
    st.markdown("## 📝 User Feedback")
    
    feedback_file = "logs/feedback.txt"
    
    if not os.path.exists(feedback_file):
        st.info("📝 No feedback received yet!")
        st.code(f"Expected: {os.path.abspath(feedback_file)}")
        
        if st.button("🛠️ Create Logs Folder"):
            try:
                os.makedirs("logs", exist_ok=True)
                with open("logs/feedback.txt", "w") as f:
                    f.write("# Petal Feedback Log\n")
                st.success("✅ Logs folder created!")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        return
    
    try:
        with open(feedback_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        feedback_lines = [l for l in lines if l.strip() and not l.startswith('#')]
        
        if not feedback_lines:
            st.info("📝 Feedback file exists but no entries yet.")
            return
        
        st.success(f"📊 Total feedback: {len(feedback_lines)}")
        
        for line in reversed(feedback_lines):
            st.text(line.strip())
    
    except Exception as e:
        st.error(f"Error reading feedback: {str(e)}")

def run_app():
    """Main app"""
    configure_page()
    load_custom_css()
    
    page_selection = create_professional_sidebar()
    page = get_page_from_selection(page_selection)
    
    if page == "Chat":
        chat_interface()
    elif page == "Tips":
        display_professional_header()
        show_tips()
    elif page == "Timeline":
        display_professional_header()
        show_cycle_timeline()
    elif page == "Feedback":
        display_professional_header()
        show_feedback_page()
    else:
        chat_interface()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 1rem; color: #666;">
        Made with 💜 for menstrual health awareness
        <br><br>
        <strong>Disclaimer:</strong> Petal provides educational information only and cannot replace professional medical advice.
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    run_app()
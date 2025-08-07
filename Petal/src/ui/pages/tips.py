import streamlit as st
from datetime import datetime

def show_tips():
    """Professional menstrual health tips that actually work"""
    
    # Professional styling that works in Streamlit
    st.markdown("""
    <style>
    .tip-header {
        background: linear-gradient(135deg, #ff6b9d, #ffa8cc);
        color: white;
        padding: 20px;
        border-radius: 15px;
        text-align: center;
        margin-bottom: 20px;
    }
    
    .tip-section {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #e91e63;
    }
    
    .fact-box {
        background: linear-gradient(135deg, #e8f5e8, #f0f8ff);
        border-radius: 8px;
        padding: 12px;
        margin: 12px 0;
        border-left: 3px solid #4caf50;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
        border-radius: 8px;
        padding: 12px;
        margin: 12px 0;
        border-left: 3px solid #ffc107;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="tip-header">
        <h1>🌸 Comprehensive Menstrual Health Guide</h1>
        <p>Evidence-based information for your wellness journey</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Quick Navigation with working session state
    st.markdown("### 📍 Quick Navigation")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("🩸 Cycle Basics", use_container_width=True):
            st.session_state.show_section = "cycle_basics"
            st.rerun()
    with col2:
        if st.button("💊 Pain Management", use_container_width=True):
            st.session_state.show_section = "pain_management"
            st.rerun()
    with col3:
        if st.button("🧠 Mental Health", use_container_width=True):
            st.session_state.show_section = "mental_health"
            st.rerun()
    with col4:
        if st.button("🚨 When to See Doctor", use_container_width=True):
            st.session_state.show_section = "doctor"
            st.rerun()
    
    # Show all sections or specific section
    show_all = not hasattr(st.session_state, 'show_section')
    
    if st.button("📚 Show All Sections", use_container_width=True):
        if hasattr(st.session_state, 'show_section'):
            del st.session_state.show_section
        st.rerun()
    
    st.markdown("---")
    
    # Cycle Basics Section
    if show_all or getattr(st.session_state, 'show_section', '') == 'cycle_basics':
        st.markdown("""
        <div class="tip-section">
            <h2>🩸 Understanding Your Menstrual Cycle</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 📊 Normal Cycle Ranges
            - **Cycle length**: 21-35 days (average 28)
            - **Period duration**: 2-7 days (average 3-5)
            - **Blood loss**: 30-40ml total (2-3 tablespoons)
            - **Age of onset**: 10-15 years typically
            
            #### 🔄 Cycle Phases
            **1. Menstrual Phase (Days 1-5)**
            - Uterine lining sheds
            - Hormone levels lowest
            - May experience fatigue
            
            **2. Follicular Phase (Days 1-13)**
            - Egg development begins
            - Estrogen rises gradually
            - Energy levels increase
            """)
        
        with col2:
            st.markdown("""
            **3. Ovulation (Around Day 14)**
            - Egg released from ovary
            - Peak fertility window
            - Slight temperature rise
            - Some may feel mild pain
            
            **4. Luteal Phase (Days 15-28)**
            - Progesterone peaks then drops
            - PMS symptoms possible
            - Breast tenderness common
            """)
            
            st.info("💡 **Medical Fact**: Your cycle is controlled by estrogen, progesterone, FSH, and LH. Irregular cycles in the first 2-3 years are completely normal.")
    
    # Pain Management Section
    if show_all or getattr(st.session_state, 'show_section', '') == 'pain_management':
        st.markdown("""
        <div class="tip-section">
            <h2>💊 Evidence-Based Pain Management</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 🌡️ Heat Therapy
            **How it works**: Heat increases blood flow and relaxes uterine muscles
            
            **Methods**:
            - Heating pad (15-20 minutes)
            - Warm bath (38-40°C)
            - Hot water bottle
            - Heat patches
            
            **Effectiveness**: 70-80% report relief
            """)
        
        with col2:
            st.markdown("""
            #### 💊 Medications
            **NSAIDs (Most Effective)**:
            - Ibuprofen: 400-600mg every 6-8 hours
            - Naproxen: 220mg every 8-12 hours
            - Start 1-2 days before period
            
            **How they work**: Block prostaglandin production
            
            **Alternative**: Acetaminophen (less effective but safe)
            """)
        
        with col3:
            st.markdown("""
            #### 🧘 Natural Methods
            **Exercise**:
            - Light cardio releases endorphins
            - Yoga poses: child's pose, cat-cow
            - Walking 20-30 minutes daily
            
            **Other Methods**:
            - Massage therapy
            - Magnesium supplements (240-360mg)
            - Acupuncture
            """)
        
        st.success("🔬 **Research Insight**: Regular aerobic exercise can reduce menstrual pain by up to 40%. NSAIDs work best when started before severe pain.")
    
    # Mental Health Section
    if show_all or getattr(st.session_state, 'show_section', '') == 'mental_health':
        st.markdown("""
        <div class="tip-section">
            <h2>🧠 Mental Health & Emotional Wellness</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 😔 Understanding PMS
            **Common Symptoms**:
            - Mood swings (affects 80% of people)
            - Irritability and anxiety
            - Food cravings
            - Bloating and breast tenderness
            - Sleep disturbances
            
            **Timeline**: 1-2 weeks before period
            
            #### 🌱 Coping Strategies
            - **Mindfulness**: 10-15 minutes daily
            - **Sleep**: 7-9 hours nightly
            - **Limit caffeine**: During luteal phase
            - **Complex carbs**: Stabilize mood
            """)
        
        with col2:
            st.markdown("""
            #### 🚨 When PMS Becomes PMDD
            **Premenstrual Dysphoric Disorder** affects 3-8% of people
            
            **Severe Symptoms**:
            - Marked mood changes
            - Severe depression or anxiety
            - Daily functioning impairment
            - Anger or conflict
            
            **Treatment Available**: 
            - Cognitive behavioral therapy
            - SSRIs (antidepressants)
            - Lifestyle modifications
            - Birth control options
            """)
        
        st.warning("⚠️ **Important**: If mood symptoms severely impact your life, please consult a healthcare provider. Effective treatments are available.")
    
    # Doctor Consultation Section
    if show_all or getattr(st.session_state, 'show_section', '') == 'doctor':
        st.markdown("""
        <div class="tip-section">
            <h2>🏥 When to Seek Medical Care</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🚨 Immediate Medical Attention
            **Seek emergency care for**:
            - Severe pain unresponsive to medication
            - Bleeding through pad/tampon every hour for 2+ hours
            - Fever >101°F with tampon use
            - Sudden, severe pelvic pain
            - Signs of severe anemia (dizziness, fainting)
            
            #### ⚠️ Schedule Appointment For
            - Periods lasting >7 days consistently
            - Cycles <21 or >35 days
            - Missing periods for 3+ months
            - Pain interfering with daily activities
            - Severe mood symptoms
            """)
        
        with col2:
            st.markdown("""
            #### 🩺 What to Track
            **For Your Doctor Visit**:
            - Period start/end dates
            - Flow heaviness (light/medium/heavy)
            - Pain levels (1-10 scale)
            - Mood changes and timing
            - Associated symptoms
            - Medication effectiveness
            
            #### ❓ Questions to Ask
            - "Are my symptoms normal for my age?"
            - "What treatment options are available?"
            - "Could this indicate a condition?"
            - "When should I follow up?"
            """)
        
        st.error("🆘 **Crisis Resources**: Crisis Text Line: 741741 | Suicide Prevention: 988 | Emergency: 911")
    
    # Additional sections for comprehensive view
    if show_all:
        # Nutrition Section
        st.markdown("""
        <div class="tip-section">
            <h2>🥗 Nutrition for Menstrual Health</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
            #### 🍎 Foods to Include
            **Iron-Rich Foods**:
            - Lean red meat, poultry
            - Spinach, kale, broccoli
            - Lentils, chickpeas
            - Fortified cereals
            
            **Calcium Sources**:
            - Dairy products
            - Leafy greens
            - Sardines, salmon
            - Almonds
            """)
        
        with col2:
            st.markdown("""
            #### 🚫 Foods to Limit
            **During Your Period**:
            - Excessive caffeine (>200mg/day)
            - High sodium foods
            - Refined sugars
            - Alcohol
            - Trans fats
            
            **Why**: Can worsen bloating, mood swings, and cramps
            """)
        
        with col3:
            st.markdown("""
            #### 💊 Helpful Supplements
            **Evidence-Based**:
            - **Magnesium**: 200-400mg for cramps
            - **Omega-3**: 1-2g for inflammation
            - **Vitamin D**: If deficient
            - **Iron**: For heavy periods
            
            *Consult healthcare provider first*
            """)
        
        # Products Section
        st.markdown("""
        <div class="tip-section">
            <h2>🧴 Products & Hygiene</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            #### 🩸 Product Options
            **Disposable Products**:
            - **Pads**: Change every 4-6 hours
            - **Tampons**: Change every 4-8 hours (TSS risk)
            
            **Reusable Products**:
            - **Menstrual cups**: 12-hour wear, 10-year lifespan
            - **Period underwear**: 12-hour protection
            - **Reusable pads**: Eco-friendly
            
            **Choosing Products**:
            - Light days: Regular protection
            - Heavy days: Super/overnight
            - Sensitive skin: Organic, fragrance-free
            """)
        
        with col2:
            st.markdown("""
            #### 🚿 Hygiene Best Practices
            **Daily Care**:
            - Gentle, unscented soap externally only
            - Change products every 4-8 hours
            - Wash hands before/after changes
            - Cotton underwear for breathability
            
            **Avoid**:
            - Douching (disrupts natural pH)
            - Scented products near vaginal area
            - Tampons >8 hours
            - Internal cleaning
            """)
        
        st.info("🔬 **Medical Note**: The vagina is self-cleaning. Only external washing needed. Internal cleaning disrupts healthy bacteria.")
        
        # Common Conditions
        st.markdown("""
        <div class="tip-section">
            <h2>🔍 Common Menstrual Conditions</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Use Streamlit's native expanders for better functionality
        with st.expander("🔴 Heavy Menstrual Bleeding (Menorrhagia)"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **Definition**: Bleeding >7 days or changing protection every hour
                
                **Common Causes**:
                - Hormonal imbalances
                - Uterine fibroids
                - Polyps
                - Blood clotting disorders
                
                **Impact**: Can lead to iron deficiency anemia
                """)
            with col2:
                st.markdown("""
                **Treatment Options**:
                - Hormonal birth control
                - Tranexamic acid
                - Iron supplements
                - IUD with progestin
                - Surgical options (severe cases)
                
                **When to See Doctor**: Immediately if bleeding severe or feeling dizzy/faint
                """)
        
        with st.expander("😣 Dysmenorrhea (Painful Periods)"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **Primary Dysmenorrhea**: 
                - Common cramping without underlying condition
                - Caused by prostaglandins
                - Usually improves with age
                
                **Secondary Dysmenorrhea**:
                - Pain from underlying condition
                - Endometriosis, fibroids, etc.
                - May worsen over time
                """)
            with col2:
                st.markdown("""
                **Treatment Approach**:
                1. NSAIDs (first-line treatment)
                2. Hormonal contraceptives
                3. Heat therapy
                4. Exercise and stress management
                5. Specialist referral (severe cases)
                
                **Red Flags**: Pain unresponsive to treatment or worsening
                """)
        
        with st.expander("🌙 Irregular Periods"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("""
                **Common Causes**:
                - PCOS (Polycystic Ovary Syndrome)
                - Thyroid disorders
                - Stress and weight changes
                - Excessive exercise
                - Eating disorders
                - Certain medications
                """)
            with col2:
                st.markdown("""
                **When It's Normal**:
                - First 2-3 years after first period
                - During perimenopause
                - While breastfeeding
                - After stopping birth control
                
                **When to Worry**: Missing periods 3+ months without pregnancy
                """)
        
        # Myth Busting
        st.markdown("""
        <div class="tip-section">
            <h2>🚫 Myth Busting: Evidence vs Fiction</h2>
        </div>
        """, unsafe_allow_html=True)
        
        myths = [
            ("You can't swim during your period", "Water pressure prevents flow while swimming. Use tampons or cups."),
            ("PMS isn't real", "PMS affects 85% of people. PMDD is a serious medical condition."),
            ("You lose a lot of blood", "Average loss is only 30-40ml (2-3 tablespoons) total."),
            ("Exercise makes cramps worse", "Regular exercise reduces menstrual pain and improves mood."),
            ("All cycles are 28 days", "Normal cycles range 21-35 days. Your normal may differ."),
            ("Can't get pregnant during period", "Less likely but possible, especially with shorter cycles.")
        ]
        
        for i, (myth, fact) in enumerate(myths):
            col1, col2 = st.columns(2)
            if i % 2 == 0:
                with col1:
                    st.error(f"❌ **Myth**: {myth}")
                    st.success(f"✅ **Fact**: {fact}")
            else:
                with col2:
                    st.error(f"❌ **Myth**: {myth}")
                    st.success(f"✅ **Fact**: {fact}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    ### 📚 Trusted Medical Resources
    
    **🏥 ACOG** - American College of Obstetricians and Gynecologists  
    **🩺 Mayo Clinic** - Comprehensive health information  
    **🔬 NIH** - National Institutes of Health  
    **👩‍⚕️ Planned Parenthood** - Reproductive health resources  
    """)
    
    st.info("⚠️ **Medical Disclaimer**: This information is for educational purposes only and does not replace professional medical advice. Always consult healthcare providers for medical concerns.")

if __name__ == "__main__":
    show_tips()
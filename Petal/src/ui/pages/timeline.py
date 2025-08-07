import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

def calculate_next_periods(last_period_date, cycle_length, num_predictions=6):
    """Calculate next periods based on cycle length"""
    predictions = []
    current_date = datetime.strptime(last_period_date, '%Y-%m-%d')
    
    for i in range(1, num_predictions + 1):
        next_period = current_date + timedelta(days=cycle_length * i)
        predictions.append({
            'start_date': next_period.strftime('%Y-%m-%d'),
            'month': next_period.strftime('%B %Y')
        })
    
    return predictions

def get_cycle_info(date, periods_data, cycle_length):
    """Get cycle information for a specific date"""
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    
    for period in periods_data:
        period_start = datetime.strptime(period['start_date'], '%Y-%m-%d')
        period_end = period_start + timedelta(days=period.get('period_length', 5) - 1)
        
        # Check if it's a period day
        if period_start <= date_obj <= period_end:
            return {
                'type': 'period',
                'predicted': period.get('type') == 'predicted'
            }
        
        # Check cycle day for ovulation
        cycle_start = period_start
        days_since_start = (date_obj - cycle_start).days
        cycle_day = (days_since_start % cycle_length) + 1
        
        if 13 <= cycle_day <= 15 and days_since_start >= 0:
            return {
                'type': 'ovulation',
                'predicted': False
            }
        
        # Check fertile window (days 10-17)
        if 10 <= cycle_day <= 17 and days_since_start >= 0:
            return {
                'type': 'fertile',
                'predicted': False
            }
    
    return {'type': 'normal', 'predicted': False}

def create_simple_calendar(year, month, periods_data, cycle_length):
    """Create simple calendar using basic Streamlit components"""
    
    # Get calendar for the month
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    today = datetime.now().date()
    
    # Calendar header with navigation
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col1:
        if st.button("◀ Previous", key="prev_btn", help="Previous Month"):
            if st.session_state.current_month == 1:
                st.session_state.current_month = 12
                st.session_state.current_year -= 1
            else:
                st.session_state.current_month -= 1
            st.rerun()
    
    with col2:
        st.markdown(f"### 🌸 {month_name} {year}")
    
    with col3:
        if st.button("Next ▶", key="next_btn", help="Next Month"):
            if st.session_state.current_month == 12:
                st.session_state.current_month = 1
                st.session_state.current_year += 1
            else:
                st.session_state.current_month += 1
            st.rerun()
    
    st.markdown("---")
    
    # Day headers
    header_cols = st.columns(7)
    days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    for i, day in enumerate(days):
        header_cols[i].markdown(f"**{day}**")
    
    # Calendar grid
    for week in cal:
        week_cols = st.columns(7)
        for i, day in enumerate(week):
            with week_cols[i]:
                if day == 0:
                    # Empty cell
                    st.write("")
                else:
                    # Get date info
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                    is_today = date_obj == today
                    
                    # Get cycle info
                    info = get_cycle_info(date_str, periods_data, cycle_length)
                    
                    # Create display for each day with colored circles around dates
                    if info['type'] == 'period':
                        if info['predicted']:
                            # Expected period - cute dashed circle
                            st.markdown(f"""
                            <div style="
                                width: 50px;
                                height: 50px;
                                border: 3px dashed #ff69b4;
                                border-radius: 50%;
                                background: linear-gradient(135deg, #fff0f5, #fce4ec);
                                color: #d63384;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                font-weight: 600;
                                font-size: 16px;
                                margin: 0 auto;
                                cursor: pointer;
                                transition: all 0.3s ease;
                                box-shadow: 0 2px 8px rgba(255, 105, 180, 0.2);
                                font-family: 'Quicksand', sans-serif;
                            " title="Expected Period ✨">
                                {day}
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            # Actual period - cute solid circle
                            st.markdown(f"""
                            <div style="
                                width: 50px;
                                height: 50px;
                                border: 2px solid #ff1493;
                                border-radius: 50%;
                                background: linear-gradient(135deg, #ff69b4, #ff1493);
                                color: white;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                font-weight: 600;
                                font-size: 16px;
                                margin: 0 auto;
                                cursor: pointer;
                                transition: all 0.3s ease;
                                box-shadow: 0 4px 12px rgba(255, 20, 147, 0.4);
                                font-family: 'Quicksand', sans-serif;
                            " title="Period Day 🌸" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
                                {day}
                            </div>
                            """, unsafe_allow_html=True)
                    elif info['type'] == 'ovulation':
                        # Ovulation - cute blue circle
                        st.markdown(f"""
                        <div style="
                            width: 50px;
                            height: 50px;
                            border: 2px solid #1976d2;
                            border-radius: 50%;
                            background: linear-gradient(135deg, #42a5f5, #1976d2);
                            color: white;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-weight: 600;
                            font-size: 16px;
                            margin: 0 auto;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            box-shadow: 0 4px 12px rgba(25, 118, 210, 0.4);
                            font-family: 'Quicksand', sans-serif;
                        " title="Ovulation Day 💙" onmouseover="this.style.transform='scale(1.1)'" onmouseout="this.style.transform='scale(1)'">
                            {day}
                        </div>
                        """, unsafe_allow_html=True)
                    elif info['type'] == 'fertile':
                        # Fertile window - cute light blue circle
                        st.markdown(f"""
                        <div style="
                            width: 50px;
                            height: 50px;
                            border: 2px solid #81d4fa;
                            border-radius: 50%;
                            background: linear-gradient(135deg, #e1f5fe, #b3e5fc);
                            color: #0277bd;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-weight: 600;
                            font-size: 16px;
                            margin: 0 auto;
                            cursor: pointer;
                            transition: all 0.3s ease;
                            box-shadow: 0 2px 8px rgba(129, 212, 250, 0.3);
                            font-family: 'Quicksand', sans-serif;
                        " title="Fertile Window 💫" onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                            {day}
                        </div>
                        """, unsafe_allow_html=True)
                    else:
                        # Normal day or today - cute styling
                        if is_today:
                            st.markdown(f"""
                            <div style="
                                width: 55px;
                                height: 55px;
                                border: 3px solid #ffc107;
                                border-radius: 50%;
                                background: linear-gradient(135deg, #fff8e1, #ffecb3);
                                color: #f57c00;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                font-weight: 700;
                                font-size: 18px;
                                margin: 0 auto;
                                cursor: pointer;
                                transition: all 0.3s ease;
                                box-shadow: 0 0 0 3px rgba(255, 193, 7, 0.3), 0 4px 15px rgba(255, 193, 7, 0.4);
                                font-family: 'Quicksand', sans-serif;
                                animation: pulse 2s infinite;
                            " title="Today! ✨" onmouseover="this.style.transform='scale(1.15)'" onmouseout="this.style.transform='scale(1)'">
                                {day}
                            </div>
                            <style>
                            @keyframes pulse {{
                                0%, 100% {{ box-shadow: 0 0 0 3px rgba(255, 193, 7, 0.3), 0 4px 15px rgba(255, 193, 7, 0.4); }}
                                50% {{ box-shadow: 0 0 0 6px rgba(255, 193, 7, 0.2), 0 6px 20px rgba(255, 193, 7, 0.3); }}
                            }}
                            </style>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown(f"""
                            <div style="
                                width: 45px;
                                height: 45px;
                                border: 1px solid #e0e0e0;
                                border-radius: 50%;
                                background: rgba(255, 255, 255, 0.7);
                                color: #757575;
                                display: flex;
                                align-items: center;
                                justify-content: center;
                                font-weight: 500;
                                font-size: 16px;
                                margin: 0 auto;
                                cursor: pointer;
                                transition: all 0.3s ease;
                                font-family: 'Quicksand', sans-serif;
                            " title="{date_str}" onmouseover="this.style.backgroundColor='rgba(255, 182, 193, 0.1)'; this.style.borderColor='#ffb6c1'" onmouseout="this.style.backgroundColor='rgba(255, 255, 255, 0.7)'; this.style.borderColor='#e0e0e0'">
                                {day}
                            </div>
                            """, unsafe_allow_html=True)

def show_cycle_timeline():
    """Simple Period Tracker"""
    
    st.markdown("# 🌸 Period Tracker")
    
    # Initialize session state
    if 'period_data' not in st.session_state:
        st.session_state.period_data = []
    if 'current_month' not in st.session_state:
        st.session_state.current_month = datetime.now().month
    if 'current_year' not in st.session_state:
        st.session_state.current_year = datetime.now().year
    
    # Sidebar with cute styling
    with st.sidebar:
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #ffb3d9, #ffc0e3);
            padding: 15px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 20px;
        ">
            <h3 style="color: white; margin: 0; font-family: 'Quicksand', sans-serif;">
                🌸 ✨ Track Your Cycle ✨ 🌸
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        # Cute input form
        with st.form("add_period"):
            st.markdown("""
            <div style="
                background: rgba(255, 182, 193, 0.1);
                padding: 15px;
                border-radius: 15px;
                border: 2px dashed #ffb6c1;
                margin: 10px 0;
            ">
                <h4 style="color: #d63384; text-align: center; margin-top: 0;">
                    🌺 Add Your Period Data 🌺
                </h4>
            </div>
            """, unsafe_allow_html=True)
            
            start_date = st.date_input(
                "Period Start Date",
                value=datetime.now().date(),
                help="When did your period start?"
            )
            
            period_length = st.slider(
                "Period Length (days)",
                min_value=1,
                max_value=10,
                value=5,
                help="How many days did your period last?"
            )
            
            cycle_length = st.slider(
                "Cycle Length (days)",
                min_value=21,
                max_value=45,
                value=28,
                help="How many days between periods?"
            )
            
            submitted = st.form_submit_button("✨ Add Period ✨")
            
            if submitted:
                new_period = {
                    'start_date': start_date.strftime('%Y-%m-%d'),
                    'period_length': period_length,
                    'cycle_length': cycle_length,
                    'type': 'actual'
                }
                st.session_state.period_data.append(new_period)
                st.success("🎉 Period added successfully! 🌸")
                st.balloons()  # Cute celebration!
                st.rerun()
        
        # Show recent periods with cute styling
        if st.session_state.period_data:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #e1f5fe, #f3e5f5);
                padding: 15px;
                border-radius: 15px;
                margin: 15px 0;
                border: 1px solid #ffb3d9;
            ">
                <h4 style="color: #d63384; text-align: center; margin-top: 0;">
                    📊 ✨ Recent Periods ✨
                </h4>
            </div>
            """, unsafe_allow_html=True)
            
            for period in st.session_state.period_data[-3:]:
                date = datetime.strptime(period['start_date'], '%Y-%m-%d')
                cycle_len = period.get('cycle_length', 28)
                st.markdown(f"""
                <div style="
                    background: rgba(255, 182, 193, 0.1);
                    padding: 8px 12px;
                    border-radius: 10px;
                    margin: 5px 0;
                    border-left: 3px solid #ff69b4;
                ">
                    🌸 <strong>{date.strftime('%b %d')}</strong> - {cycle_len} day cycle
                </div>
                """, unsafe_allow_html=True)
        
        # Cute clear data button
        if st.session_state.period_data:
            if st.button("🗑️ ✨ Clear All Data ✨"):
                st.session_state.period_data = []
                st.success("✨ Data cleared! Ready for fresh tracking! 🌸")
                st.rerun()
    
    # Main calendar area with cute container
    st.markdown('<div class="cute-container">', unsafe_allow_html=True)
    
    if not st.session_state.period_data:
        # Cute instructions when no data
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #fff9c4, #ffe0b3);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            margin: 20px 0;
            border: 2px dashed #ffc107;
        ">
            <h3 style="color: #e65100; margin-top: 0;">
                ✨ 🌸 Welcome to Your Cute Period Tracker! 🌸 ✨
            </h3>
            <p style="color: #f57600; font-size: 16px;">
                👈 Add your period data in the sidebar to see your adorable calendar!
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #e8f5e8, #d4edda);
                padding: 15px;
                border-radius: 15px;
                border: 1px solid #c3e6cb;
            ">
                <h4 style="color: #155724; margin-top: 0;">🌸 ✨ Cute Features ✨</h4>
                <ul style="color: #155724;">
                    <li><strong>🔴 Soft pink circles</strong> for period days</li>
                    <li><strong>🔵 Pretty blue circles</strong> for ovulation</li>
                    <li><strong>💙 Light blue</strong> for fertile window</li>
                    <li><strong>⭕ Dashed circles</strong> for predictions</li>
                    <li><strong>🟡 Golden glow</strong> for today</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div style="
                background: linear-gradient(135deg, #e3f2fd, #f3e5f5);
                padding: 15px;
                border-radius: 15px;
                border: 1px solid #bbdefb;
            ">
                <h4 style="color: #0d47a1; margin-top: 0;">📅 ✨ How to Use ✨</h4>
                <ul style="color: #0d47a1;">
                    <li><strong>◀ Previous</strong> and <strong>Next ▶</strong> to navigate</li>
                    <li><strong>Click arrows</strong> to scroll months</li>
                    <li><strong>Add cute data</strong> to see predictions</li>
                    <li><strong>Track patterns</strong> with love</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Show sample calendar
        st.markdown("---")
        sample_periods = [{
            'start_date': (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'),
            'period_length': 5,
            'cycle_length': 28,
            'type': 'actual'
        }]
        
        create_simple_calendar(
            datetime.now().year,
            datetime.now().month,
            sample_periods,
            28
        )
        
    else:
        # Get current cycle length from latest entry
        latest_cycle_length = st.session_state.period_data[-1].get('cycle_length', 28)
        
        # Add predictions to the data
        predictions = calculate_next_periods(
            st.session_state.period_data[-1]['start_date'],
            latest_cycle_length,
            12
        )
        
        all_periods = st.session_state.period_data.copy()
        for pred in predictions:
            all_periods.append({
                'start_date': pred['start_date'],
                'period_length': 5,
                'cycle_length': latest_cycle_length,
                'type': 'predicted'
            })
        
        # Calculate next period info
        next_period_date = datetime.strptime(predictions[0]['start_date'], '%Y-%m-%d')
        days_until = (next_period_date - datetime.now()).days
        
        # Next period info with extra cuteness
        if days_until > 0:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #ffebee, #fce4ec);
                padding: 15px;
                border-radius: 20px;
                text-align: center;
                margin: 20px 0;
                border: 2px solid #f8bbd9;
                box-shadow: 0 4px 15px rgba(248, 187, 217, 0.3);
            ">
                <h3 style="color: #d63384; margin: 0;">
                    🌸 ✨ Next Period in {days_until} days ✨ 🌸
                </h3>
                <p style="color: #ad1457; font-size: 18px; margin: 5px 0 0 0;">
                    ({next_period_date.strftime('%B %d')}) 💖
                </p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div style="
                background: linear-gradient(135deg, #ffcdd2, #f8bbd9);
                padding: 15px;
                border-radius: 20px;
                text-align: center;
                margin: 20px 0;
                border: 2px solid #f48fb1;
                box-shadow: 0 4px 15px rgba(244, 143, 177, 0.3);
            ">
                <h3 style="color: #c2185b; margin: 0;">
                    🌸 ✨ Period Today ✨ 🌸
                </h3>
                <p style="color: #ad1457; font-size: 18px; margin: 5px 0 0 0;">
                    ({next_period_date.strftime('%B %d')}) 💝
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        # Create calendar
        create_simple_calendar(
            st.session_state.current_year,
            st.session_state.current_month,
            all_periods,
            latest_cycle_length
        )
        
        # Cute legend
        st.markdown("---")
        st.markdown("""
        <div style="
            background: linear-gradient(135deg, #f3e5f5, #e8f5e8);
            padding: 20px;
            border-radius: 20px;
            margin: 20px 0;
            border: 2px solid #e1bee7;
        ">
            <h3 style="text-align: center; color: #7b1fa2; margin-top: 0;">
                ✨ 🌸 Legend 🌸 ✨
            </h3>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.markdown("""
            <div style="text-align: center; padding: 10px;">
                <div style="width: 30px; height: 30px; background: linear-gradient(135deg, #ff69b4, #ff1493); border-radius: 50%; margin: 0 auto 8px;"></div>
                <strong style="color: #d63384;">Period</strong>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 10px;">
                <div style="width: 30px; height: 30px; background: linear-gradient(135deg, #e1f5fe, #b3e5fc); border-radius: 50%; margin: 0 auto 8px; border: 2px solid #81d4fa;"></div>
                <strong style="color: #0277bd;">Fertile</strong>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown("""
            <div style="text-align: center; padding: 10px;">
                <div style="width: 30px; height: 30px; background: linear-gradient(135deg, #42a5f5, #1976d2); border-radius: 50%; margin: 0 auto 8px;"></div>
                <strong style="color: #1976d2;">Ovulation</strong>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown("""
            <div style="text-align: center; padding: 10px;">
                <div style="width: 30px; height: 30px; background: linear-gradient(135deg, #fff0f5, #fce4ec); border: 3px dashed #ff69b4; border-radius: 50%; margin: 0 auto 8px;"></div>
                <strong style="color: #d63384;">Expected</strong>
            </div>
            """, unsafe_allow_html=True)
        with col5:
            st.markdown("""
            <div style="text-align: center; padding: 10px;">
                <div style="width: 30px; height: 30px; background: linear-gradient(135deg, #fff8e1, #ffecb3); border: 3px solid #ffc107; border-radius: 50%; margin: 0 auto 8px;"></div>
                <strong style="color: #f57c00;">Today</strong>
            </div>
            """, unsafe_allow_html=True)
        
        # Quick stats
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🔄 Cycle Length", f"{latest_cycle_length} days")
        
        with col2:
            avg_period_length = sum(p.get('period_length', 5) for p in st.session_state.period_data) / len(st.session_state.period_data)
            st.metric("🌸 Period Length", f"{avg_period_length:.0f} days")
        
        with col3:
            st.metric("📊 Cycles Tracked", len(st.session_state.period_data))
        
        # Today button
        current_date = datetime.now()
        if (st.session_state.current_month != current_date.month or 
            st.session_state.current_year != current_date.year):
            if st.button("📍 Go to Current Month"):
                st.session_state.current_month = current_date.month
                st.session_state.current_year = current_date.year
                st.rerun()

if __name__ == "__main__":
    show_cycle_timeline()
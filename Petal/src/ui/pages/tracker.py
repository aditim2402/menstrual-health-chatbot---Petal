import streamlit as st
from src.ui.charts.cycle_timeline import plot_cycle_timeline

def tracker_interface():
    st.subheader("📅 Cycle Timeline (Like iOS Health)")

    st.markdown("""
    - 🔴 **Dark Red**: Logged period days  
    - 🩸 **Light Red**: Predicted period days  
    - 🟣 **Purple Dot**: Logged ovulation/symptoms  
    - ⚪️ **White**: No entry  
    """)

    fig = plot_cycle_timeline(
        period_start_day=1,
        period_length=4,
        cycle_length=28,
        predicted_start=30,
        predicted_length=4,
        purple_logs=[13, 15]
    )
    st.pyplot(fig)

    with st.expander("ℹ️ What is Ovulation?"):
        st.info("""
        Ovulation occurs roughly 14 days before the next expected period.
        It's your most fertile time and may include symptoms like increased discharge,
        slight cramps, or breast tenderness.
        """)


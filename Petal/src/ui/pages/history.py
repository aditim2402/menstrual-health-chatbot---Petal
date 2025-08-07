import streamlit as st
import pandas as pd
from src.core.user_memory import get_user_symptoms

def show_history():
    st.title("🕓 Chat History")
    st.write("This feature is under development. Stay tuned!")
    
def history_page():
    st.title("📖 Symptom & Mood History")
    data = get_user_symptoms()
    if not data.empty:
        st.dataframe(data)
        chart = data.groupby("symptom").size().plot(kind="bar", title="Symptom Frequency")
        st.pyplot(chart.get_figure())
    else:
        st.info("No symptoms logged yet.")

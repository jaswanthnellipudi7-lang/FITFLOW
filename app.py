import streamlit as st
import pandas as pd
import json
from pathlib import Path
from datetime import date

st.set_page_config(
    page_title="FITFLOW",
    page_icon="💪",
    layout="wide"
)

FILE = Path("fitness_data.json")

def load_data():
    if FILE.exists():
        return json.loads(FILE.read_text())
    return []

def save_data(data):
    FILE.write_text(json.dumps(data, indent=4))

data = load_data()

st.markdown("""
<style>
.stApp {
    background-color: #101827;
    color: white;
}
h1, h2, h3 {
    color: #38D9A9;
}
</style>
""", unsafe_allow_html=True)

st.title("💪 FITFLOW")
st.caption("Your Personal Fitness Tracker")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Log Workout", "History"]
)

if page == "Dashboard":
    st.header("Fitness Dashboard")

    today_data = [
        x for x in data if x["date"] == str(date.today())
    ]

    total = sum(x["minutes"] for x in today_data)

    col1, col2 = st.columns(2)

    col1.metric("Today's Activities", len(today_data))
    col2.metric("Active Minutes", total)

    st.subheader("Recent Workouts")

    if today_data:
        st.dataframe(pd.DataFrame(today_data))
    else:
        st.info("No workouts logged today.")

elif page == "Log Workout":
    st.header("Add New Workout")

    with st.form("workout_form"):
        activity = st.selectbox(
            "Choose Activity",
            ["Walking", "Running", "Cycling", "Yoga", "Gym"]
        )

        minutes = st.number_input(
            "Duration (minutes)",
            min_value=1,
            max_value=300,
            value=30
        )

        submitted = st.form_submit_button("Save Workout")

        if submitted:
            data.append({
                "date": str(date.today()),
                "activity": activity,
                "minutes": int(minutes)
            })

            save_data(data)
            st.success("Workout saved successfully!")

elif page == "History":
    st.header("Workout History")

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

        st.subheader("Activity Chart")
        chart = df.groupby("activity")["minutes"].sum()
        st.bar_chart(chart)
    else:
        st.info("No workout history available.")



st.sidebar.caption("FITFLOW | Stay Active 💚")

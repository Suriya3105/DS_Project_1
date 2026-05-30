import streamlit as st
import pandas as pd
import mysql.connector
from queries import queries

# -----------------------------------
# MYSQL CONNECTION
# -----------------------------------

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1222",
    database="earthquake_db",
    port="3307"
)

# -----------------------------------
# PAGE SETTINGS
# -----------------------------------

st.set_page_config(
    page_title="Global Seismic Trends",
    layout="wide"
)

st.title("🌍 Global Seismic Trends Dashboard")

# -----------------------------------
# SIDEBAR MAIN HEADINGS
# -----------------------------------

category = st.sidebar.radio(
    "Select Category",
    [
        "Magnitude & Depth",
        "Time Analysis",
        "Casualties & Economic Loss",
        "Event Type & Quality Metrics",
        "Tsunamis & Alerts",
        "Seismic Pattern & Trends",
        "Depth & Location Analysis"
    ]
)

# -----------------------------------
# CATEGORY QUESTIONS
# -----------------------------------

category_questions = {

    "Magnitude & Depth": [
        "1. Top 10 strongest earthquakes",
        "2. Top 10 deepest earthquakes",
        "3. Shallow earthquakes <50km & mag >7.5",
        "4. Average depth per continent",
        "5. Average magnitude per magType"
    ],

    "Time Analysis": [
        "6. Year with most earthquakes",
        "7. Month with highest earthquakes",
        "8. Day of week with most earthquakes",
        "9. Earthquakes per hour",
        "10. Most active reporting network"
    ],

    "Casualties & Economic Loss": [
        "11. Top 5 significant earthquakes",
        "12. Total significance per country",
        "13. Average significance by alert level"
    ],

    "Event Type & Quality Metrics": [
        "14. Reviewed vs automatic earthquakes",
        "15. Count by earthquake type",
        "16. Number by data type",
        "17. Average RMS & GAP per continent",
        "18. High station coverage events"
    ],

    "Tsunamis & Alerts": [
        "19. Tsunami events per year",
        "20. Earthquakes by alert level"
    ],

    "Seismic Pattern & Trends": [
        "21. Top 5 countries by avg magnitude",
        "22. Countries with shallow & deep earthquakes",
        "23. Year-over-year growth rate",
        "24. Top 3 seismically active regions"
    ],

    "Depth & Location Analysis": [
        "25. Avg depth near equator",
        "26. Highest shallow/deep ratio",
        "27. Avg magnitude tsunami vs non-tsunami",
        "28. Lowest reliability events",
        "29. Consecutive earthquakes",
        "30. Deep-focus earthquake regions"
    ]
}

# -----------------------------------
# QUESTION SELECTION
# -----------------------------------

selected_question = st.sidebar.selectbox(
    "Select Question",
    category_questions[category]
)

# -----------------------------------
# RUN QUERY
# -----------------------------------

query = queries[selected_question]

df = pd.read_sql(query, conn)

# -----------------------------------
# DISPLAY RESULTS
# -----------------------------------

st.subheader(selected_question)

st.dataframe(df, use_container_width=True)

# -----------------------------------
# DOWNLOAD BUTTON
# -----------------------------------

csv = df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="📥 Download CSV",
    data=csv,
    file_name="earthquake_analysis.csv",
    mime="text/csv"
)
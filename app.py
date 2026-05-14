import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv

from agent.sql_generator import generate_sql
from db.sql_executor import run_query


# ---------------------------------------------------
# 🔐 Load environment (LOCAL + CLOUD SAFE)
# ---------------------------------------------------
load_dotenv()

def get_secret(key):
    """
    Priority:
    1. Streamlit Cloud Secrets
    2. Local .env file
    """
    return st.secrets.get(key, os.getenv(key))


GROQ_API_KEY = get_secret("GROQ_API_KEY")
DB_URL = get_secret("DB_URL")


# Safety check
if not GROQ_API_KEY:
    st.error("❌ GROQ_API_KEY not found (check .env or Streamlit secrets)")
    st.stop()

if not DB_URL:
    st.error("❌ DB_URL not found (check .env or Streamlit secrets)")
    st.stop()


# ---------------------------------------------------
# 🎨 Page Config
# ---------------------------------------------------
st.set_page_config(
    page_title="AI SQL Agent Dashboard",
    layout="wide"
)

st.title("🤖 AI SQL Analytics Dashboard")
st.write("Ask questions in natural language and get SQL + insights + charts")


# ---------------------------------------------------
# 🧾 Input
# ---------------------------------------------------
question = st.text_input("💬 Enter your question")
run_btn = st.button("🚀 Run Analysis")


# ---------------------------------------------------
# 🚀 Main Flow
# ---------------------------------------------------
if run_btn and question:

    with st.spinner("Generating SQL..."):
        sql_query = generate_sql(question)

    st.subheader("🧠 Generated SQL")
    st.code(sql_query, language="sql")

    with st.spinner("Executing Query..."):
        result = run_query(sql_query)

    # Convert to DataFrame
    df = pd.DataFrame(result) if not isinstance(result, pd.DataFrame) else result

    st.subheader("📊 Query Result")
    st.dataframe(df)


    # ---------------------------------------------------
    # 📈 Visualization
    # ---------------------------------------------------
    st.subheader("📈 Visualization")

    if df is not None and not df.empty and df.shape[1] >= 2:

        numeric_cols = df.select_dtypes(include="number").columns
        categorical_cols = df.select_dtypes(exclude="number").columns

        if len(numeric_cols) > 0 and len(categorical_cols) > 0:

            fig = px.bar(
                df,
                x=categorical_cols[0],
                y=numeric_cols[0],
                title="AI Generated Bar Chart"
            )
            st.plotly_chart(fig, use_container_width=True)

        elif len(numeric_cols) >= 2:

            fig = px.scatter(
                df,
                x=numeric_cols[0],
                y=numeric_cols[1],
                title="AI Generated Scatter Plot"
            )
            st.plotly_chart(fig, use_container_width=True)

        else:
            st.info("⚠️ Not enough numeric data for chart")

    else:
        st.warning("No data returned from query")
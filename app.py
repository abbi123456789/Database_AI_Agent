import streamlit as st
import pandas as pd
import plotly.express as px

from agent.sql_generator import generate_sql
from db.sql_executor import run_query


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
# 🧾 User Input
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

    # Convert to DataFrame if needed
    if isinstance(result, pd.DataFrame):
        df = result
    else:
        df = pd.DataFrame(result)

    st.subheader("📊 Query Result")
    st.dataframe(df)


    # ---------------------------------------------------
    # 📈 Automatic Chart Generation
    # ---------------------------------------------------
    st.subheader("📈 Visualization")

    if df.shape[1] >= 2:

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
import plotly.express as px
import pandas as pd
import logging

# ---------------------------------------------------
# 🪵 Logging
# ---------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ---------------------------------------------------
# 🎨 Dynamic AI Chart Generator
# ---------------------------------------------------
def generate_chart(df: pd.DataFrame, question: str):

    try:

        if df.empty:
            logger.warning("⚠️ Empty dataframe received")
            return

        columns = df.columns.tolist()

        # ---------------------------------------------------
        # Auto detect chart type
        # ---------------------------------------------------
        numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
        categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

        chart = None

        # ---------------------------------------------------
        # KPI Card Style (Single Value)
        # ---------------------------------------------------
        if len(df.columns) == 1 and len(df) == 1:

            value = df.iloc[0, 0]

            fig = px.bar(
                x=["Result"],
                y=[value],
                text=[value],
                title="📌 KPI Result"
            )

            fig.update_traces(textposition="outside")

            fig.update_layout(
                template="plotly_dark",
                height=500
            )

            fig.show()
            return

        # ---------------------------------------------------
        # Bar Chart
        # ---------------------------------------------------
        if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:

            x = categorical_cols[0]
            y = numeric_cols[0]

            chart = px.bar(
                df,
                x=x,
                y=y,
                text=y,
                title=f"📊 {question}",
                barmode="group"
            )

        # ---------------------------------------------------
        # Line Chart
        # ---------------------------------------------------
        elif len(numeric_cols) >= 2:

            chart = px.line(
                df,
                x=numeric_cols[0],
                y=numeric_cols[1],
                title=f"📈 {question}",
                markers=True
            )

        # ---------------------------------------------------
        # Scatter Plot
        # ---------------------------------------------------
        elif len(numeric_cols) >= 2:

            chart = px.scatter(
                df,
                x=numeric_cols[0],
                y=numeric_cols[1],
                size=numeric_cols[1],
                title=f"📍 {question}"
            )

        # ---------------------------------------------------
        # Pie Chart
        # ---------------------------------------------------
        if len(categorical_cols) >= 1 and len(numeric_cols) >= 1:

            pie = px.pie(
                df,
                names=categorical_cols[0],
                values=numeric_cols[0],
                title=f"🥧 Distribution - {question}",
                hole=0.4
            )

            pie.update_layout(template="plotly_dark")
            pie.show()

        # ---------------------------------------------------
        # Final Styling
        # ---------------------------------------------------
        if chart:

            chart.update_layout(
                template="plotly_dark",
                height=600,
                title_x=0.5,
                font=dict(size=14),
                hovermode="x unified"
            )

            chart.update_traces(
                textposition="outside"
            )

            chart.show()

            logger.info("✅ Chart generated successfully")

    except Exception as e:
        logger.error(f"❌ Chart generation failed: {e}")
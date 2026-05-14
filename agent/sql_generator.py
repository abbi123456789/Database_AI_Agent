import logging
from dotenv import load_dotenv

from langchain_groq import ChatGroq

from db.schema_loader import load_schema
from db.sql_executor import run_query
from agent.chart_generator import generate_chart

# ---------------------------------------------------
# 🔐 Load ENV
# ---------------------------------------------------
load_dotenv()

# ---------------------------------------------------
# 🪵 Logging
# ---------------------------------------------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ---------------------------------------------------
# 🤖 Initialize LLM (Groq)
# ---------------------------------------------------
llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

# ---------------------------------------------------
# 📚 Load Schema
# ---------------------------------------------------
schema = load_schema()

# ---------------------------------------------------
# 🧠 Prompt Template
# ---------------------------------------------------
PROMPT_TEMPLATE = """
You are an expert SQL generator.

Database Schema:
{schema}

Rules:
1. Return ONLY SQL query
2. No explanations
3. Use SQLite syntax
4. Use only available tables and columns
5. Never hallucinate columns
6. Use proper JOINs when needed
7. Use aliases for readability
8. Ensure query is executable

User Question:
{question}
"""

# ---------------------------------------------------
# 🚀 SQL Generator
# ---------------------------------------------------
def generate_sql(question: str):

    try:
        prompt = PROMPT_TEMPLATE.format(
            schema=schema,
            question=question
        )

        logger.info("🧠 Generating SQL query...")

        response = llm.invoke(prompt)

        sql_query = response.content.strip()

        # Clean markdown if any
        sql_query = sql_query.replace("```sql", "")
        sql_query = sql_query.replace("```", "")
        sql_query = sql_query.strip()

        logger.info(f"✅ SQL Generated: {sql_query}")

        return sql_query

    except Exception as e:
        logger.error(f"❌ SQL generation failed: {e}")
        raise


# ---------------------------------------------------
# 🚀 Full Pipeline (Main Function)
# ---------------------------------------------------
def ask_database(question: str):

    try:
        # 1. Generate SQL
        sql_query = generate_sql(question)

        print("\n🧠 Generated SQL:")
        print(sql_query)

        # 2. Execute SQL
        result = run_query(sql_query)

        print("\n📊 Query Result:")
        print(result)

        # 3. Generate Chart
        generate_chart(result, question)

        return result

    except Exception as e:
        logger.error(f"❌ Pipeline failed: {e}")
        raise


# ---------------------------------------------------
# 🧪 Test Execution
# ---------------------------------------------------
if __name__ == "__main__":

    questions = [
        "Show all employees",
        "Show employees with salary greater than 60000",
        "Show top 2 employees by salary",
        "Show department wise average salary",
        "Show total sales by employee"
    ]

    for q in questions:

        print("\n" + "=" * 60)
        print(f"❓ Question: {q}")

        try:
            ask_database(q)

        except Exception as e:
            print(f"❌ Error: {e}")
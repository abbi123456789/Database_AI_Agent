# 🤖 AI SQL Agent Dashboard

An intelligent Streamlit-based application that allows users to ask questions in natural language and automatically converts them into SQL queries, executes them on a database, and displays results with visualizations.

---

## 🚀 Features

- Convert natural language questions into SQL queries using LLM
- Connect to SQLite or PostgreSQL databases
- Execute generated SQL queries automatically
- Display query results in tabular format
- Generate charts automatically based on result set
- Works both locally and on Streamlit Cloud
- Secure deployment using environment variables / Streamlit secrets

---

## 🛠 Tech Stack

- Python
- Streamlit
- LangChain
- Groq LLM
- SQLAlchemy
- Pandas
- Plotly
- SQLite / PostgreSQL

---

## 📂 Project Structure

```bash
AI_SQL_Agent/
│
├── app.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── agent/
│   ├── __init__.py
│   ├── sql_generator.py
│   └── chart_generator.py
│
├── db/
│   ├── __init__.py
│   ├── connection.py
│   ├── schema_loader.py
│   └── sql_executor.py
│
└── test.db
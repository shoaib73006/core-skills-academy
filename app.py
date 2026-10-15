
import streamlit as st
import pandas as pd

from database import (
    initialize_database,
    save_progress,
    load_progress,
    save_quiz_result,
    load_quiz_results,
    load_topic_performance,
)

st.set_page_config(
    page_title="Core Skills Academy",
    page_icon="🎯",
    layout="wide",
)

initialize_database()

modules = {
    "Python Fundamentals": [
        "Variables and Data Types",
        "Loops and Conditions",
        "Functions",
        "Lists and Dictionaries",
        "OOP and Exception Handling",
    ],
    "SQL and Databases": [
        "SELECT and Filtering",
        "Joins",
        "Aggregate Functions",
        "Subqueries",
    ],
    "APIs and Backend": [
        "HTTP and JSON",
        "REST API Concepts",
        "FastAPI Basics",
    ],
    "Code Quality": [
        "Git and GitHub",
        "Debugging",
        "Unit Testing",
    ],
}

questions = [
    {
        "question": "Which data type stores True or False?",
        "options": ["int", "str", "bool", "list"],
        "answer": "bool",
        "topic": "Variables and Data Types",
    },
    {
        "question": "Which keyword defines a function?",
        "options": ["func", "define", "def", "function"],
        "answer": "def",
        "topic": "Functions",
    },
    {
        "question": "What does len([10, 20, 30]) return?",
        "options": ["2", "3", "30", "10"],
        "answer": "3",
        "topic": "Lists and Dictionaries",
    },
    {
        "question": "Which collection stores unique values?",
        "options": ["list", "tuple", "set", "string"],
        "answer": "set",
        "topic": "Lists and Dictionaries",
    },
    {
        "question": "Which keyword handles exceptions?",
        "options": ["catch", "except", "error", "final"],
        "answer": "except",
        "topic": "OOP and Exception Handling",
    },
    {
        "question": "Which SQL keyword filters rows?",
        "options": ["ORDER BY", "WHERE", "GROUP BY", "JOIN"],
        "answer": "WHERE",
        "topic": "SELECT and Filtering",
    },
    {
        "question": "Which SQL JOIN returns matching rows?",
        "options": ["INNER JOIN", "CROSS JOIN", "FULL JOIN", "No JOIN"],
        "answer": "INNER JOIN",
        "topic": "Joins",
    },
    {
        "question": "Which format is commonly used by REST APIs?",
        "options": ["JSON", "MP3", "EXE", "PNG"],
        "answer": "JSON",
        "topic": "HTTP and JSON",
    },
    {
        "question": "Which HTTP method commonly retrieves data?",
        "options": ["POST", "GET", "PATCH", "DELETE"],
        "answer": "GET",
        "topic": "REST API Concepts",
    },
    {
        "question": "Which tool tracks source code changes?",
        "options": ["Git", "Pandas", "SQLite", "Streamlit"],
        "answer": "Git",
        "topic": "Git and GitHub",
    },
]

st.title("🎯 Core Skills Academy")
st.caption("Learn • Practice • Assess • Improve")

# Load saved progress
if "completed" not in st.session_state:
    st.session_state.completed = load_progress()

# Dashboard
st.header("📊 Learning Dashboard")

total_topics = sum(len(topics) for topics in modules.values())
completed_count = len(st.session_state.completed)

col1, col2, col3 = st.columns(3)
col1.metric("Total Topics", total_topics)
col2.metric("Completed Topics", completed_count)
col3.metric(
    "Learning Progress",
    f"{completed_count / total_topics * 100:.1f}%"
)

st.progress(completed_count / total_topics)

# Learning modules
st.divider()
st.header("📚 Learning Modules")

for module, topics in modules.items():
    with st.expander(module):
        for topic in topics:
            key = f"{module}:{topic}"

            if key not in st.session_state:
                st.session_state[key] = (
                    key in st.session_state.completed
                )

            def update_progress(topic_key=key):
                checked = st.session_state[topic_key]
                save_progress(topic_key, checked)

                if checked:
                    st.session_state.completed.add(topic_key)
                else:
                    st.session_state.completed.discard(topic_key)

            st.checkbox(
                topic,
                key=key,
                on_change=update_progress,
            )

# Quiz
st.divider()
st.header("📝 Skills Assessment")

with st.form("skills_quiz"):
    answers = {}

    for i, q in enumerate(questions):
        answers[i] = st.radio(
            f"Q{i + 1}. {q['question']}",
            q["options"],
            index=None,
            key=f"assessment_{i}",
        )

    submitted = st.form_submit_button("Submit Assessment")

if submitted:
    attempt_answers = [
        {
            "topic": q["topic"],
            "is_correct": answers[i] == q["answer"],
        }
        for i, q in enumerate(questions)
    ]

    score, total, percentage = save_quiz_result(
        "Core Skills Assessment",
        attempt_answers,
    )

    st.session_state.latest_result = {
        "score": score,
        "total": total,
        "percentage": percentage,
        "answers": answers.copy(),
    }

if "latest_result" in st.session_state:
    result = st.session_state.latest_result

    st.metric(
        "Latest Score",
        f"{result['score']}/{result['total']}",
    )
    st.progress(result["percentage"] / 100)

    with st.expander("Review answers"):
        for i, q in enumerate(questions):
            st.write(f"**{i + 1}. {q['question']}**")
            st.write(f"Your answer: {result['answers'][i] or 'Not answered'}")
            st.write(f"Correct answer: {q['answer']}")

# Weak topic analysis
st.divider()
st.header("🧠 Weak Topic Analysis")

topic_results = load_topic_performance()

if topic_results:
    df_topics = pd.DataFrame(
        topic_results,
        columns=[
            "Topic",
            "Questions Attempted",
            "Correct Answers",
            "Accuracy (%)",
        ],
    )

    st.subheader("Topic-wise Performance")
    st.dataframe(df_topics, use_container_width=True, hide_index=True)

    weak_topics = [
        row for row in topic_results
        if row[1] >= 1 and row[3] < 70
    ]

    if weak_topics:
        st.warning("These topics need more practice.")

        for topic, attempts, correct, accuracy in weak_topics:
            st.markdown(f"**{topic} — {accuracy}% accuracy**")

            if accuracy < 40:
                st.write(
                    "Recommendation: Revise the fundamentals, "
                    "then solve 5 beginner-level questions."
                )
            else:
                st.write(
                    "Recommendation: Review mistakes and solve "
                    "3–5 targeted practice questions."
                )
    else:
        st.success(
            "No weak topics identified yet. Keep practicing "
            "to build a more reliable performance history."
        )

    st.subheader("Topic Accuracy Chart")
    st.bar_chart(df_topics.set_index("Topic")["Accuracy (%)"])

else:
    st.info(
        "Attempt the assessment to unlock personalized "
        "topic analysis and revision suggestions."
    )

# Quiz history
st.divider()
st.header("📈 Quiz Performance History")

results = load_quiz_results()

if results:
    df_history = pd.DataFrame(
        results,
        columns=[
            "ID",
            "Quiz",
            "Score",
            "Total Questions",
            "Percentage",
            "Attempted At",
        ],
    )

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Attempts", len(df_history))
    col2.metric(
        "Average Score",
        f"{df_history['Percentage'].mean():.1f}%",
    )
    col3.metric(
        "Best Score",
        f"{df_history['Percentage'].max():.1f}%",
    )

    st.dataframe(
        df_history.drop(columns=["ID"]),
        use_container_width=True,
        hide_index=True,
    )

    chart = df_history.iloc[::-1].reset_index(drop=True)
    chart.index = range(1, len(chart) + 1)
    chart.index.name = "Attempt"

    st.line_chart(chart["Percentage"])

else:
    st.info("Your quiz attempts will appear here.")

st.divider()
st.caption("Core Skills Academy | Python • Streamlit • SQLite")

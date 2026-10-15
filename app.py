
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
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

initialize_database()

# -------------------- DATA --------------------

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

# -------------------- SESSION STATE --------------------

if "completed" not in st.session_state:
    st.session_state.completed = load_progress()

if "latest_result" not in st.session_state:
    st.session_state.latest_result = None

# -------------------- DESIGN --------------------

st.markdown("""
<style>
    .stApp {
        background: #f5f7fc;
        color: #172033;
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #10162b 0%, #171d38 100%);
    }

    [data-testid="stSidebar"] * {
        color: #f4f5ff;
    }

    .brand {
        font-size: 25px;
        font-weight: 800;
        line-height: 1.25;
        padding: 12px 0 4px;
        color: #ffffff;
    }

    .brand span {
        color: #a78bfa;
    }

    .muted {
        color: #66718a;
        font-size: 14px;
    }

    .hero {
        background: linear-gradient(120deg, #191d46, #5635a9);
        padding: 28px;
        border-radius: 20px;
        color: white;
        margin: 8px 0 22px;
        box-shadow: 0 10px 28px rgba(57, 43, 120, 0.13);
    }

    .hero h1 {
        color: white;
        font-size: 30px;
        margin: 0 0 8px;
    }

    .hero p {
        color: #e1e4ff;
        margin: 0;
        font-size: 15px;
    }

    .metric-card {
        background: #ffffff;
        padding: 20px;
        border: 1px solid #e7eaf3;
        border-radius: 16px;
        min-height: 126px;
        box-shadow: 0 4px 14px rgba(31, 41, 70, 0.035);
    }

    .metric-label {
        font-size: 13px;
        color: #69748c;
        margin-bottom: 12px;
    }

    .metric-value {
        font-size: 29px;
        font-weight: 800;
        color: #171d36;
        line-height: 1.2;
    }

    .metric-note {
        color: #778199;
        font-size: 12px;
        margin-top: 8px;
    }

    .section-title {
        font-size: 21px;
        font-weight: 750;
        color: #1b2340;
        margin: 12px 0 4px;
    }

    .panel {
        background: white;
        border: 1px solid #e7eaf3;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 14px;
    }

    .topic-name {
        font-weight: 650;
        color: #27314c;
    }

    .stButton > button {
        border-radius: 10px;
        font-weight: 650;
        min-height: 42px;
        border: 1px solid #ddd7fc;
    }

    .stButton > button[kind="primary"] {
        background: linear-gradient(100deg, #6546ed, #9144e8);
        border: none;
        color: white;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e7eaf3;
        border-radius: 14px;
        padding: 15px;
    }

    div[data-testid="stProgressBar"] > div {
        border-radius: 20px;
    }

    h1, h2, h3 {
        letter-spacing: -0.4px;
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    @media (max-width: 700px) {
        .hero { padding: 20px; }
        .hero h1 { font-size: 24px; }
        .metric-card { padding: 15px; }
    }
</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------

with st.sidebar:
    st.markdown(
        '<div class="brand">🎓 Core Skills<br>'
        '<span>Academy</span></div>',
        unsafe_allow_html=True,
    )
    st.caption("LEARN · PRACTICE · GROW")
    st.divider()

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "📚 Learning Modules",
            "📝 Skills Assessment",
            "🧠 Weak Topic Analysis",
            "📈 Quiz History",
        ],
        label_visibility="visible",
    )

    st.divider()

    total_topics = sum(len(items) for items in modules.values())
    completed_count = sum(
        1
        for module, topics in modules.items()
        for topic in topics
        if f"{module}:{topic}" in st.session_state.completed
    )

    progress = completed_count / total_topics if total_topics else 0

    st.markdown("**🚀 Your learning journey**")
    st.progress(progress)
    st.caption(
        f"{completed_count} of {total_topics} topics completed"
    )

    st.divider()
    st.caption("Built with Python & Streamlit")

# -------------------- DASHBOARD --------------------

if page == "🏠 Dashboard":
    st.markdown("""
    <div class="hero">
        <h1>Welcome back, Shoaib! 👋</h1>
        <p>Small steps every day. Big progress over time.</p>
    </div>
    """, unsafe_allow_html=True)

    total_topics = sum(len(items) for items in modules.values())
    completed_count = sum(
        1
        for module, topics in modules.items()
        for topic in topics
        if f"{module}:{topic}" in st.session_state.completed
    )
    progress = completed_count / total_topics if total_topics else 0

    history = load_quiz_results()
    attempts = len(history)
    average_score = (
        sum(row[4] for row in history) / attempts
        if attempts else 0
    )

    c1, c2, c3, c4 = st.columns(4)

    cards = [
        ("📚", "Total Topics", total_topics, "Across all modules"),
        ("✅", "Completed", completed_count, "Topics checked off"),
        ("🎯", "Overall Progress", f"{progress:.0%}", "Keep it going!"),
        ("🏆", "Quizzes Attempted", attempts, f"Average score: {average_score:.1f}%"),
    ]

    for col, (emoji, label, value, note) in zip(
        [c1, c2, c3, c4], cards
    ):
        with col:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-label">{emoji} {label}</div>
                    <div class="metric-value">{value}</div>
                    <div class="metric-note">{note}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.write("")
    left, right = st.columns([1.4, 1])

    with left:
        st.markdown(
            '<div class="section-title">📘 Learning Progress</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            for module, topics in modules.items():
                done = sum(
                    f"{module}:{topic}" in st.session_state.completed
                    for topic in topics
                )
                module_progress = done / len(topics) if topics else 0

                st.markdown(f"**{module}**")
                st.progress(
                    module_progress,
                    text=f"{done}/{len(topics)} topics · {module_progress:.0%}",
                )

            st.caption(
                "Mark topics complete in Learning Modules to update progress."
            )

    with right:
        st.markdown(
            '<div class="section-title">⚡ Quick Actions</div>',
            unsafe_allow_html=True,
        )

        with st.container(border=True):
            st.write("**Ready to improve your skills?**")
            st.caption("Practice concepts and review your performance.")

            if st.button("📝 Start Skills Assessment", type="primary", use_container_width=True):
                st.session_state.navigate_to = "📝 Skills Assessment"
                st.rerun()

            if st.button("📚 Continue Learning", use_container_width=True):
                st.session_state.navigate_to = "📚 Learning Modules"
                st.rerun()

            if st.button("🧠 Review Weak Topics", use_container_width=True):
                st.session_state.navigate_to = "🧠 Weak Topic Analysis"
                st.rerun()

    if st.session_state.get("navigate_to"):
        st.info(
            f"Use the sidebar to open {st.session_state.navigate_to}."
        )
        st.session_state.navigate_to = None

    st.markdown(
        '<div class="section-title">📈 Recent Quiz Performance</div>',
        unsafe_allow_html=True,
    )

    if history:
        df_history = pd.DataFrame(
            history,
            columns=[
                "ID", "Quiz", "Score", "Total",
                "Percentage", "Attempted At"
            ],
        )
        chart_data = df_history.iloc[::-1].reset_index(drop=True)
        chart_data.index = range(1, len(chart_data) + 1)
        chart_data.index.name = "Attempt"

        st.line_chart(chart_data["Percentage"], y_label="Score (%)")
    else:
        st.info("Your quiz scores will appear here after your first assessment.")

# -------------------- LEARNING MODULES --------------------

elif page == "📚 Learning Modules":
    st.markdown(
        '<div class="section-title">📚 Learning Modules</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        "Track your learning journey. Your progress is saved in the database."
    )

    for module, topics in modules.items():
        done = sum(
            f"{module}:{topic}" in st.session_state.completed
            for topic in topics
        )

        with st.expander(
            f"{module} · {done}/{len(topics)} completed",
            expanded=False,
        ):
            st.progress(done / len(topics) if topics else 0)

            for topic in topics:
                key = f"{module}:{topic}"

                # Keep the existing database key format.
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

# -------------------- QUIZ --------------------

elif page == "📝 Skills Assessment":
    st.markdown(
        '<div class="section-title">📝 Skills Assessment</div>',
        unsafe_allow_html=True,
    )
    st.caption("10 questions · Python, SQL, APIs and development fundamentals")

    with st.form("skills_quiz"):
        answers = {}

        for i, q in enumerate(questions):
            st.markdown(f"**Question {i + 1} of {len(questions)}**")
            answers[i] = st.radio(
                q["question"],
                q["options"],
                index=None,
                key=f"assessment_{i}",
            )
            st.divider()

        submitted = st.form_submit_button(
            "Submit Assessment",
            type="primary",
            use_container_width=True,
        )

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

    result = st.session_state.latest_result

    if result:
        st.markdown("### Your latest result")

        c1, c2, c3 = st.columns(3)
        c1.metric("Score", f"{result['score']}/{result['total']}")
        c2.metric("Accuracy", f"{result['percentage']:.1f}%")
        c3.metric(
            "Result",
            "Excellent" if result["percentage"] >= 80
            else "Keep Practising" if result["percentage"] < 60
            else "Good Work",
        )

        st.progress(result["percentage"] / 100)

        with st.expander("Review answers"):
            for i, q in enumerate(questions):
                user_answer = result["answers"].get(i)
                correct = user_answer == q["answer"]

                st.markdown(f"**{i + 1}. {q['question']}**")
                st.write(f"Your answer: {user_answer or 'Not answered'}")
                st.write(f"Correct answer: {q['answer']}")

                if correct:
                    st.success("Correct")
                else:
                    st.error("Review this concept")

# -------------------- WEAK TOPIC ANALYSIS --------------------

elif page == "🧠 Weak Topic Analysis":
    st.markdown(
        '<div class="section-title">🧠 Weak Topic Analysis</div>',
        unsafe_allow_html=True,
    )
    st.caption("Use your quiz performance to decide what to revise next.")

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

        weak_topics = [
            row for row in topic_results
            if row[1] >= 1 and row[3] < 70
        ]

        c1, c2 = st.columns(2)
        c1.metric("Topics Analysed", len(topic_results))
        c2.metric("Topics Below 70%", len(weak_topics))

        st.markdown("### Topic accuracy")
        st.bar_chart(
            df_topics.set_index("Topic")["Accuracy (%)"],
            y_label="Accuracy (%)",
        )

        st.markdown("### Recommended revision")

        if weak_topics:
            for topic, attempts, correct, accuracy in weak_topics:
                with st.container(border=True):
                    st.markdown(f"**{topic}**")
                    st.progress(
                        max(0.0, min(1.0, accuracy / 100)),
                        text=f"{accuracy:.1f}% accuracy · {attempts} attempts",
                    )

                    if accuracy < 40:
                        st.write(
                            "Start with the fundamentals, then solve "
                            "five beginner-level questions."
                        )
                    else:
                        st.write(
                            "Review mistakes and solve three to five "
                            "targeted practice questions."
                        )
        else:
            st.success(
                "No topics below 70% accuracy in your recorded attempts."
            )

        st.dataframe(
            df_topics,
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.info(
            "Complete the skills assessment to unlock topic-wise "
            "performance insights."
        )

# -------------------- QUIZ HISTORY --------------------

elif page == "📈 Quiz History":
    st.markdown(
        '<div class="section-title">📈 Quiz History</div>',
        unsafe_allow_html=True,
    )
    st.caption("Review past attempts and track your improvement.")

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

        c1, c2, c3 = st.columns(3)
        c1.metric("Total Attempts", len(df_history))
        c2.metric(
            "Average Score",
            f"{df_history['Percentage'].mean():.1f}%",
        )
        c3.metric(
            "Best Score",
            f"{df_history['Percentage'].max():.1f}%",
        )

        chart = df_history.iloc[::-1].reset_index(drop=True)
        chart.index = range(1, len(chart) + 1)
        chart.index.name = "Attempt"

        st.markdown("### Performance over time")
        st.line_chart(chart["Percentage"], y_label="Score (%)")

        st.markdown("### All attempts")
        st.dataframe(
            df_history.drop(columns=["ID"]),
            use_container_width=True,
            hide_index=True,
        )

        csv_data = df_history.drop(columns=["ID"]).to_csv(index=False)

        st.download_button(
            "⬇️ Download quiz history (CSV)",
            data=csv_data,
            file_name="core_skills_quiz_history.csv",
            mime="text/csv",
        )
    else:
        st.info("No quiz attempts yet. Complete the assessment to start your history.")

# -------------------- FOOTER --------------------

st.divider()
st.caption(
    "🎓 Core Skills Academy · Learn • Practice • Assess • Improve"
)

import streamlit as st
import time
import matplotlib.pyplot as plt
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from extract import extract_text_from_pdf
from llm_engine import generate_questions
from quiz_engine_file import init_quiz_state, evaluate_quiz

# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------
st.set_page_config(
    page_title="SmartQuizzer Pro",
    layout="wide",
    initial_sidebar_state="expanded"
)

init_quiz_state(st)

# --------------------------------------------------
# SESSION STATE DEFAULTS
# --------------------------------------------------
defaults = {
    "quiz_started": False,
    "quiz_submitted": False,
    "show_review": False,
    "questions": [],
    "answers": {},
    "current_question": 0,
    "score": 0,
    "username": "",
    "quiz_start_time": None,
    "time_limit": 0
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --------------------------------------------------
# STYLES
# --------------------------------------------------
st.markdown("""
<style>
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
}

/* MAIN HEADER CARD */
.header-card {
    background: linear-gradient(135deg,#6366f1,#22c55e);
    padding: 2rem;
    border-radius: 22px;
    color: white;
    text-align: center;
    box-shadow: 0 14px 30px rgba(0,0,0,0.25);
    margin-bottom: 25px;
}

.header-title {
    font-size: 2.6rem;
    font-weight: 900;
}

.header-sub {
    font-size: 1.05rem;
    opacity: 0.95;
    margin-top: 6px;
}

/* Welcome card */
.name-card {
    background: linear-gradient(135deg,#6366f1,#22c55e);
    padding: 1rem 1.4rem;
    border-radius: 16px;
    color: white;
    font-size: 1.1rem;
    font-weight: 700;
    box-shadow: 0 10px 25px rgba(0,0,0,0.25);
    margin-bottom: 20px;
}

/* Instruction card */
.instruction-card {
    background: linear-gradient(135deg,#f97316,#facc15);
    padding: 1.2rem 1.5rem;
    border-radius: 16px;
    color: white;
    font-size: 1rem;
    font-weight: 600;
    box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    margin-bottom: 20px;
    transition: all 0.5s ease;
}

/* Question card */
.question-card {
    background: linear-gradient(135deg,#ffffff,#f8faff);
    padding: 1.8rem;
    border-radius: 18px;
    box-shadow: 0 8px 22px rgba(0,0,0,0.12);
    margin-bottom: 28px;
}

/* Options */
.option-btn {
    width: 100%;
    padding: 0.9rem 1rem;
    margin: 10px 0;
    border-radius: 14px;
    border: 2px solid #e5e7eb;
    background: #ffffff;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.25s ease;
}

.option-btn:hover {
    background: #eef2ff;
    transform: translateY(-2px);
}

.option-selected {
    background: linear-gradient(135deg,#6366f1,#22c55e) !important;
    color: white !important;
    border-color: transparent !important;
}

/* Score card */
.score-card {
    background: linear-gradient(135deg,#22c55e,#3b82f6);
    color: white;
    padding: 2.2rem;
    border-radius: 22px;
    text-align: center;
    box-shadow: 0 14px 30px rgba(0,0,0,0.25);
    margin: 30px 0;
}

.score-big {
    font-size: 3.2rem;
    font-weight: 900;
}

/* Report */
.report-card {
    background: white;
    border-radius: 16px;
    padding: 1.2rem;
    margin-bottom: 18px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.1);
}

/* Timer */
.timer-box {
    background: #111827;
    color: #22c55e;
    padding: 10px 16px;
    border-radius: 12px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 14px;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------
with st.sidebar:
    st.markdown("## 🧠 SmartQuizzer Pro")

    st.session_state.username = st.text_input(
        "👤 Your Name",
        value=st.session_state.username,
        placeholder="Enter your name"
    )

    uploaded_file = st.file_uploader("📄 Upload PDF / TXT", type=["pdf", "txt"])
    topic_input = st.text_input("✍️ Or enter a topic", placeholder="Machine Learning")

    st.markdown("---")

    difficulty = st.selectbox("🎯 Difficulty", ["easy", "medium", "hard"])

    n_questions = st.slider("📊 Number of Questions", 3, 30, 10)

    # Timer per quiz (minutes)
    timer_minutes = st.slider("⏱ Quiz Time (minutes)", 1, 60, 10)

    generate_clicked = st.button("🚀 Generate Quiz", use_container_width=True)

# --------------------------------------------------
# HEADER CARD
# --------------------------------------------------
st.markdown("""
<div class="header-card">
    <div class="header-title">🧠 SmartQuizzer Pro</div>
    <div class="header-sub">
        AI-powered quiz generator with smart evaluation & downloadable report
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# NAME CARD
# --------------------------------------------------
if st.session_state.username:
    st.markdown(
        f"<div class='name-card'>👋 Welcome, {st.session_state.username}</div>",
        unsafe_allow_html=True
    )

# --------------------------------------------------
# INSTRUCTION CARD
# --------------------------------------------------
if not st.session_state.quiz_started:
    st.markdown("""
    <div class='instruction-card'>
        <h3>📌 Instructions to Attempt Quiz</h3>
        <ul>
            <li>Enter your name above.</li>
            <li>Upload a PDF or enter a topic of your choice.</li>
            <li>Select difficulty and number of questions.</li>
            <li>Click <strong>Generate Quiz</strong> to start.</li>
            <li>You can use the timer to manage your time.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# GENERATE QUIZ
# --------------------------------------------------
if generate_clicked:
    source_text = ""

    if uploaded_file:
        source_text = extract_text_from_pdf(uploaded_file)
    elif topic_input.strip():
        source_text = topic_input.strip()

    if not source_text:
        st.warning("Please upload a file or enter a topic.")
    else:
        with st.spinner("Generating intelligent quiz..."):
            st.session_state.questions = generate_questions(
                source_text,
                n_questions,
                True,
                difficulty
            )

            st.session_state.answers = {}
            st.session_state.current_question = 0
            st.session_state.quiz_started = True
            st.session_state.quiz_submitted = False
            st.session_state.show_review = False

            # TIMER INIT
            st.session_state.quiz_start_time = time.time()
            st.session_state.time_limit = timer_minutes * 60

        st.success("Quiz generated successfully!")
        time.sleep(0.5)
        st.rerun()

# --------------------------------------------------
# TIMER DISPLAY
# --------------------------------------------------
def render_timer():
    elapsed = int(time.time() - st.session_state.quiz_start_time)
    remaining = max(0, st.session_state.time_limit - elapsed)

    mins = remaining // 60
    secs = remaining % 60

    st.markdown(
        f"<div class='timer-box'>⏱ Time Left: {mins:02d}:{secs:02d}</div>",
        unsafe_allow_html=True
    )

    # AUTO SUBMIT WHEN TIME ENDS
    if remaining <= 0:
        if st.session_state.score == 0:
            st.session_state.score = evaluate_quiz(
                st.session_state.questions,
                st.session_state.answers
            )

        st.session_state.quiz_started = False
        st.session_state.quiz_submitted = True
        st.rerun()

# --------------------------------------------------
# QUIZ VIEW
# --------------------------------------------------
if st.session_state.quiz_started and not st.session_state.quiz_submitted:
    render_timer()

    q_idx = st.session_state.current_question
    q = st.session_state.questions[q_idx]

    st.markdown("<div class='question-card'>", unsafe_allow_html=True)

    st.markdown(f"### Question {q_idx + 1} / {len(st.session_state.questions)}")
    st.markdown(f"**{q['question']}**")

    labels = ["A", "B", "C", "D"]

    # ensure exactly 4 options
    distractors = q.get("distractors", [])[:3]   # max 3
    options = [q["answer"]] + distractors

    # pad if less than 4
    while len(options) < 4:
        options.append("Not Available")

    for i in range(4):
        opt = options[i]
        selected = st.session_state.answers.get(q_idx) == opt
        cls = "option-btn option-selected" if selected else "option-btn"

        if st.button(f"{labels[i]}. {opt}", key=f"opt_{q_idx}_{i}"):
            st.session_state.answers[q_idx] = opt
            st.rerun()


    col1, col2, col3 = st.columns(3)

    with col1:
        if q_idx > 0 and st.button("⬅ Previous"):
            st.session_state.current_question -= 1
            st.rerun()

    with col2:
        if st.button("✅ Submit Quiz"):
            st.session_state.score = evaluate_quiz(
                st.session_state.questions,
                st.session_state.answers
            )
            st.session_state.quiz_started = False
            st.session_state.quiz_submitted = True
            st.rerun()

    with col3:
        if q_idx < len(st.session_state.questions) - 1:
            if st.button("Next ➡"):
                st.session_state.current_question += 1
                st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# --------------------------------------------------
# RESULTS
# --------------------------------------------------
if st.session_state.quiz_submitted:
    score = st.session_state.score or 0
    total = len(st.session_state.questions)
    wrong = total - score
    percentage = (score / total) * 100

    st.markdown(f"""
    <div class="score-card">
        <div class="score-big">{score}/{total}</div>
        <div>{percentage:.1f}% Accuracy</div>
        <div style="margin-top:8px;">👤 {st.session_state.username or "Student"}</div>
    </div>
    """, unsafe_allow_html=True)

    fig, ax = plt.subplots()
    ax.bar(["Correct", "Wrong"], [score, wrong])
    ax.set_title("Performance Overview")
    st.pyplot(fig)

    if percentage >= 80:
        st.success("🌟 Excellent! You have strong command over this topic.")
    elif percentage >= 60:
        st.info("👍 Good job! Keep practicing.")
    else:
        st.warning("📘 Revise fundamentals and try again.")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("📋 View Detailed Report"):
            st.session_state.show_review = True
            st.rerun()

    with col2:
        if st.button("🔄 Start New Quiz"):
            for k in list(st.session_state.keys()):
                del st.session_state[k]
            st.rerun()

# --------------------------------------------------
# PDF REPORT
# --------------------------------------------------
def generate_pdf():
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    w, h = A4

    y = h - 40
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, y, "SmartQuizzer Report")

    y -= 30
    c.setFont("Helvetica", 11)
    c.drawString(40, y, f"Name: {st.session_state.username or 'Student'}")
    y -= 18
    c.drawString(40, y, f"Score: {st.session_state.score}/{len(st.session_state.questions)}")

    y -= 30

    for i, q in enumerate(st.session_state.questions):
        if y < 100:
            c.showPage()
            y = h - 40

        c.setFont("Helvetica-Bold", 11)
        c.drawString(40, y, f"Q{i+1}. {q['question']}")
        y -= 16

        c.setFont("Helvetica", 10)
        c.drawString(50, y, f"Your Answer: {st.session_state.answers.get(i,'Not answered')}")
        y -= 14
        c.drawString(50, y, f"Correct Answer: {q['answer']}")
        y -= 16

        if q.get("explanation"):
            c.drawString(50, y, f"Explanation: {q['explanation']}")
            y -= 18

    c.save()
    buffer.seek(0)
    return buffer

# --------------------------------------------------
# DETAILED REPORT
# --------------------------------------------------
if st.session_state.show_review:
    st.markdown("## 📋 Detailed Report")

    for i, q in enumerate(st.session_state.questions):
        st.markdown("<div class='report-card'>", unsafe_allow_html=True)
        st.markdown(f"**Q{i+1}. {q['question']}**")
        st.markdown(f"👉 Your answer: **{st.session_state.answers.get(i)}**")
        st.markdown(f"✅ Correct answer: **{q['answer']}**")

        if q.get("explanation"):
            st.markdown(f"💡 **Explanation:** {q['explanation']}")

        st.markdown("</div>", unsafe_allow_html=True)

    pdf_file = generate_pdf()
    st.download_button(
        "⬇️ Download Report (PDF)",
        pdf_file,
        file_name="SmartQuizzer_Report.pdf",
        mime="application/pdf"
    )

    if st.button("🔄 Start New Quiz", key="restart_bottom"):
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

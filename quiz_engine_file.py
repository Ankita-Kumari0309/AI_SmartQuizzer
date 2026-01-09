def init_quiz_state(st):
    if "answers" not in st.session_state:
        st.session_state.answers = {}
    if "current_question" not in st.session_state:
        st.session_state.current_question = 0
    if "score" not in st.session_state:
        st.session_state.score = None

def evaluate_quiz(questions, answers):
    score = 0
    for i, q in enumerate(questions):
        if answers.get(i) == q["answer"]:
            score += 1
    return score

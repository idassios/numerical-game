import random
import streamlit as st

st.set_page_config(
    page_title="Numerical Analysis Challenge",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Styling ----------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 950px;
}
.quiz-card {
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    padding: 1.4rem;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 10px 30px rgba(0,0,0,0.22);
    color: white;
    margin-bottom: 1rem;
}
.big-title {
    font-size: 2.1rem;
    font-weight: 800;
    margin-bottom: 0.2rem;
}
.subtitle {
    font-size: 1rem;
    opacity: 0.85;
    margin-bottom: 0.5rem;
}
.question-box {
    background: white;
    color: #111827;
    padding: 1.2rem;
    border-radius: 16px;
    border: 1px solid #e5e7eb;
    box-shadow: 0 8px 20px rgba(0,0,0,0.06);
    margin-top: 1rem;
    margin-bottom: 1rem;
}
.option-label {
    font-size: 1rem;
    font-weight: 500;
}
.score-box {
    background: #111827;
    color: white;
    padding: 1rem;
    border-radius: 16px;
    text-align: center;
}
.small-note {
    color: #6b7280;
    font-size: 0.95rem;
}
</style>
""", unsafe_allow_html=True)

# ---------- Questions ----------
QUESTIONS = [
    {
        "question": "For a continuous function f, the bisection method can be applied if:",
        "options": [
            "f'(x) exists",
            "f(a)f(b) < 0",
            "f(a) = f(b)",
            "f''(x) > 0"
        ],
        "answer": 1,
        "explanation": "Bisection needs a sign change at the endpoints of the interval."
    },
    {
        "question": r"""At iteration x_n, Newton’s method for a system is
x_(n+1) = x_n - J(x_n)^(-1)F(x_n).
Assume J(x_n)^(-1) has very large entries. Which statement is correct?""",
        "options": [
            "The update is always large",
            "The update may be large unless F(x_n) is very small",
            "The update is always small",
            "The method always converges"
        ],
        "answer": 1,
        "explanation": "A large inverse may amplify the correction term, unless F(x_n) is already very small."
    },
    {
        "question": r"""Consider the system
4x + y = 5
x + 3y = 5
Starting from (x0,y0)=(0,0), after one Gauss–Seidel iteration, the value of y1 is:""",
        "options": [
            "5/3",
            "15/12",
            "(5 - 5/4)/3",
            "5/4"
        ],
        "answer": 2,
        "explanation": "First x1 = 5/4, then y1 = (5 - x1)/3 = (5 - 5/4)/3."
    },
    {
        "question": "The trapezoidal rule approximates the function using:",
        "options": [
            "Constant segments",
            "Straight lines between points",
            "Quadratic curves",
            "Cubic curves"
        ],
        "answer": 1,
        "explanation": "It uses a linear approximation on each subinterval."
    },
    {
        "question": "A polynomial of degree n interpolates exactly:",
        "options": [
            "n points",
            "n+1 points",
            "Any number of points",
            "Only equally spaced points"
        ],
        "answer": 1,
        "explanation": "A degree-n interpolating polynomial is determined by n+1 data points."
    },
    {
        "question": "Simpson’s rule is based on approximating the function by:",
        "options": [
            "A constant function",
            "A linear function",
            "A quadratic polynomial",
            "A cubic polynomial"
        ],
        "answer": 2,
        "explanation": "Simpson’s rule uses quadratic interpolation."
    },
    {
        "question": "If a function is exactly linear, the trapezoidal rule:",
        "options": [
            "Has error",
            "Is exact",
            "Diverges",
            "Needs many intervals"
        ],
        "answer": 1,
        "explanation": "The trapezoidal rule is exact for linear functions."
    },
    {
        "question": "For the trapezoidal rule, if the step size h is halved, the error is:",
        "options": [
            "Doubled",
            "Unchanged",
            "Halved",
            "Reduced by a factor of 4"
        ],
        "answer": 3,
        "explanation": "The trapezoidal error is proportional to h^2."
    },
    {
        "question": "Interpolation means:",
        "options": [
            "Approximating data without passing through the points",
            "Finding a function that passes exactly through the given points",
            "Minimizing squared error",
            "Ignoring noisy data"
        ],
        "answer": 1,
        "explanation": "Interpolation matches all given data points exactly."
    },
    {
        "question": "In least squares, we:",
        "options": [
            "Force zero error",
            "Minimize the sum of squared residuals",
            "Use only two data points",
            "Solve a nonlinear system"
        ],
        "answer": 1,
        "explanation": "Least squares minimizes the sum of squared residuals."
    },
    {
        "question": "For the data points (0,1) and (1,3), the least-squares line y=ax+b is:",
        "options": [
            "y = 2x + 1",
            "y = x + 1",
            "y = 3x",
            "y = 2x"
        ],
        "answer": 0,
        "explanation": "The exact line through the two points is y = 2x + 1."
    }
]

# ---------- State ----------
if "started" not in st.session_state:
    st.session_state.started = False
if "questions" not in st.session_state:
    st.session_state.questions = QUESTIONS.copy()
if "current" not in st.session_state:
    st.session_state.current = 0
if "score" not in st.session_state:
    st.session_state.score = 0
if "answered" not in st.session_state:
    st.session_state.answered = False
if "selected" not in st.session_state:
    st.session_state.selected = None
if "player_name" not in st.session_state:
    st.session_state.player_name = ""

# ---------- Helper ----------
def reset_game():
    st.session_state.questions = QUESTIONS.copy()
    random.shuffle(st.session_state.questions)
    st.session_state.current = 0
    st.session_state.score = 0
    st.session_state.answered = False
    st.session_state.selected = None
    st.session_state.started = True

# ---------- Landing ----------
if not st.session_state.started:
    st.markdown("""
    <div class="quiz-card">
        <div class="big-title">🎯 Numerical Analysis Challenge</div>
        <div class="subtitle">A quiz game for Civil Engineering students</div>
        <div>Topics: Bisection, Newton, Gauss–Seidel, Interpolation, Simpson, Trapezoidal Rule, Least Squares</div>
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([2, 1])
    with left:
        name = st.text_input("Student name or team name")
        st.session_state.player_name = name
    with right:
        st.write("")
        st.write("")
        if st.button("Start Game", use_container_width=True):
            reset_game()
            st.rerun()

    st.info("This version looks much better on phone and laptop, and the questions appear one by one.")
    st.stop()

# ---------- Quiz View ----------
total = len(st.session_state.questions)
idx = st.session_state.current
q = st.session_state.questions[idx]
progress = (idx + 1) / total

top1, top2, top3 = st.columns([1.3, 1, 1])
with top1:
    st.markdown(f"""
    <div class="score-box">
        <div style="font-size:0.9rem;opacity:0.85;">Player</div>
        <div style="font-size:1.2rem;font-weight:700;">{st.session_state.player_name or "Anonymous"}</div>
    </div>
    """, unsafe_allow_html=True)
with top2:
    st.markdown(f"""
    <div class="score-box">
        <div style="font-size:0.9rem;opacity:0.85;">Question</div>
        <div style="font-size:1.3rem;font-weight:800;">{idx + 1} / {total}</div>
    </div>
    """, unsafe_allow_html=True)
with top3:
    st.markdown(f"""
    <div class="score-box">
        <div style="font-size:0.9rem;opacity:0.85;">Score</div>
        <div style="font-size:1.3rem;font-weight:800;">{st.session_state.score}</div>
    </div>
    """, unsafe_allow_html=True)

st.progress(progress)

st.markdown('<div class="question-box">', unsafe_allow_html=True)
st.subheader("Question")
st.write(q["question"])
choice = st.radio(
    "Choose one answer:",
    range(len(q["options"])),
    format_func=lambda i: f"{chr(65+i)}. {q['options'][i]}",
    key=f"q_{idx}"
)
st.markdown("</div>", unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)

with c1:
    if st.button("Submit Answer", use_container_width=True, disabled=st.session_state.answered):
        st.session_state.selected = choice
        st.session_state.answered = True
        if choice == q["answer"]:
            st.session_state.score += 1

if st.session_state.answered:
    if st.session_state.selected == q["answer"]:
        st.success("Correct.")
    else:
        st.error(f"Wrong. Correct answer: {chr(65 + q['answer'])}.")
    st.info(q["explanation"])

with c2:
    if st.button("Next", use_container_width=True):
        if idx < total - 1:
            st.session_state.current += 1
            st.session_state.answered = False
            st.session_state.selected = None
            st.rerun()
        else:
            st.session_state.current += 1
            st.rerun()

with c3:
    if st.button("Restart", use_container_width=True):
        reset_game()
        st.rerun()

# ---------- Final Screen ----------
if st.session_state.current >= total:
    st.balloons()
    st.markdown("""
    <div class="quiz-card">
        <div class="big-title">🏁 Game Finished</div>
        <div class="subtitle">Well done.</div>
    </div>
    """, unsafe_allow_html=True)

    percent = round(100 * st.session_state.score / total)
    st.metric("Final Score", f"{st.session_state.score} / {total}")
    st.metric("Success Rate", f"{percent}%")

    if percent >= 80:
        st.success("Excellent result.")
    elif percent >= 50:
        st.warning("Good effort — with a little revision this can become excellent.")
    else:
        st.error("Needs more practice.")

    if st.button("Play Again", use_container_width=True):
        reset_game()
        st.rerun()
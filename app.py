import streamlit as st

st.title("🎯 Numerical Analysis Game")

questions = [
    {
        "q": "Bisection requires:",
        "options": ["f'(x) exists", "f(a)f(b)<0", "f(a)=f(b)", "f''(x)>0"],
        "answer": 1
    },
    {
        "q": "Newton: if J^{-1} is large, then:",
        "options": [
            "update always small",
            "update may be large unless F is small",
            "method always converges",
            "no effect"
        ],
        "answer": 1
    },
    {
        "q": "Trapezoidal rule uses:",
        "options": ["constants", "straight lines", "quadratics", "cubics"],
        "answer": 1
    },
    {
        "q": "Least squares minimizes:",
        "options": ["error", "squared error", "points", "matrix size"],
        "answer": 1
    }
]

if "i" not in st.session_state:
    st.session_state.i = 0
    st.session_state.score = 0

q = questions[st.session_state.i]

st.subheader(q["q"])

choice = st.radio("Choose:", q["options"])

if st.button("Submit"):
    if q["options"].index(choice) == q["answer"]:
        st.success("Correct!")
        st.session_state.score += 1
    else:
        st.error("Wrong!")

if st.button("Next"):
    st.session_state.i += 1
    if st.session_state.i >= len(questions):
        st.write(f"Final score: {st.session_state.score}")
        st.session_state.i = 0
        st.session_state.score = 0

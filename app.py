import streamlit as st

from question_bank import get_questions
from evaluator import evaluate_answer


# -----------------------------
# PAGE CONFIGURATION
# -----------------------------

st.set_page_config(
    page_title="AI Interview Generator",
    page_icon="🎯",
    layout="centered"
)


# -----------------------------
# TITLE
# -----------------------------

st.title("🎯 AI Interview Question Generator")

st.write(
    "Practice interview questions based on your job role "
    "and experience level."
)


# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("Interview Settings")

role = st.sidebar.selectbox(
    "Select Job Role",
    [
        "Data Scientist"
    ]
)

experience = st.sidebar.selectbox(
    "Experience Level",
    [
        "Fresher"
    ]
)

category = st.sidebar.selectbox(
    "Interview Category",
    [
        "Technical",
        "HR",
        "Situation-based"
    ]
)

number_of_questions = st.sidebar.slider(
    "Number of Questions",
    min_value=1,
    max_value=5,
    value=3
)


# -----------------------------
# SESSION STATE
# -----------------------------

if "questions" not in st.session_state:
    st.session_state.questions = []

if "current_question" not in st.session_state:
    st.session_state.current_question = 0

if "scores" not in st.session_state:
    st.session_state.scores = []

if "started" not in st.session_state:
    st.session_state.started = False

if "results" not in st.session_state:
    st.session_state.results = []


# -----------------------------
# START INTERVIEW
# -----------------------------

if not st.session_state.started:

    st.subheader("Start Your Mock Interview")

    st.write("Your selected settings:")

    st.write(f"**Role:** {role}")
    st.write(f"**Experience:** {experience}")
    st.write(f"**Category:** {category}")
    st.write(f"**Questions:** {number_of_questions}")

    if st.button("🚀 Start Interview"):

        questions = get_questions(
            role,
            experience,
            category,
            number_of_questions
        )

        if len(questions) == 0:

            st.error(
                "No questions available for this selection."
            )

        else:

            st.session_state.questions = questions
            st.session_state.current_question = 0
            st.session_state.scores = []
            st.session_state.results = []
            st.session_state.started = True

            st.rerun()


# -----------------------------
# INTERVIEW
# -----------------------------

else:

    questions = st.session_state.questions

    current = st.session_state.current_question

    # Interview completed
    if current >= len(questions):

        st.success("🎉 Interview Completed!")

        st.subheader("📊 Interview Performance")

        scores = st.session_state.scores

        if scores:

            average_score = sum(scores) / len(scores)

            st.metric(
                "Overall Score",
                f"{average_score:.1f} / 10"
            )

            percentage = (average_score / 10) * 100

            st.progress(
                int(percentage)
            )

            st.write(
                f"Overall Performance: **{percentage:.0f}%**"
            )

            if average_score >= 8:

                st.success(
                    "Excellent performance!"
                )

            elif average_score >= 6:

                st.info(
                    "Good performance. Keep improving."
                )

            else:

                st.warning(
                    "More practice is recommended."
                )

        st.subheader("Question-wise Results")

        for i, result in enumerate(
            st.session_state.results
        ):

            st.write(
                f"### Question {i + 1}"
            )

            st.write(
                f"**Score:** {result['score']} / 10"
            )

            st.write(
                f"**Feedback:** {result['feedback']}"
            )

        if st.button("🔄 Start New Interview"):

            st.session_state.started = False
            st.session_state.current_question = 0
            st.session_state.scores = []
            st.session_state.results = []

            st.rerun()

    else:

        question_data = questions[current]

        st.progress(
            (current + 1) / len(questions)
        )

        st.write(
            f"Question {current + 1} of {len(questions)}"
        )

        st.subheader(
            question_data["question"]
        )

        answer = st.text_area(
            "Your Answer",
            height=180,
            key=f"answer_{current}"
        )

        if st.button("Submit Answer"):

            if not answer.strip():

                st.warning(
                    "Please enter your answer first."
                )

            else:

                result = evaluate_answer(
                    answer,
                    question_data
                )

                st.session_state.scores.append(
                    result["score"]
                )

                st.session_state.results.append(
                    result
                )

                st.session_state.current_question += 1

                st.session_state.last_result = result

                st.rerun()


# -----------------------------
# SHOW LAST RESULT
# -----------------------------

if (
    "last_result" in st.session_state
    and st.session_state.current_question > 0
):

    result = st.session_state.last_result

    st.divider()

    st.subheader("📋 Answer Evaluation")

    st.metric(
        "Score",
        f"{result['score']} / 10"
    )

    st.write(
        f"**Feedback:** {result['feedback']}"
    )

    st.write("### Concepts Identified")

    if result["matched_keywords"]:

        for keyword in result["matched_keywords"]:

            st.write(
                f"✅ {keyword}"
            )

    else:

        st.write(
            "No important concepts detected."
        )

    st.write("### Concepts to Improve")

    if result["missing_keywords"]:

        for keyword in result["missing_keywords"]:

            st.write(
                f"⚠️ {keyword}"
            )

    else:

        st.write(
            "Great! You covered the major concepts."
        )

    with st.expander("💡 Suggested Answer"):

        st.write(
            result["ideal_answer"]
        )
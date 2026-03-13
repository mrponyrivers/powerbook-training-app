import random
import streamlit as st


# -----------------------------------
# Page config
# -----------------------------------
st.set_page_config(
    page_title="Powerbook Training App",
    page_icon="📘",
    layout="wide",
)


# -----------------------------------
# Problem generators
# -----------------------------------
def generate_implied_probability_problem():
    odds_options = [1.50, 1.67, 1.80, 1.83, 1.91, 2.00, 2.20, 2.50, 2.75, 3.00]
    odds = random.choice(odds_options)
    correct_probability = 100 / odds
    return {
        "odds": odds,
        "correct_probability": correct_probability,
    }


def generate_ev_problem():
    odds_options = [1.50, 1.67, 1.80, 1.83, 1.91, 2.00, 2.20, 2.50, 2.75, 3.00]
    probability_options = [35, 40, 45, 50, 52, 55, 57, 60, 62, 65, 70]

    odds = random.choice(odds_options)
    model_probability = random.choice(probability_options)
    correct_ev = ((model_probability / 100) * odds - 1) * 100

    return {
        "odds": odds,
        "model_probability": model_probability,
        "correct_ev": correct_ev,
    }


def generate_no_vig_problem():
    market_pairs = [
        (1.91, 1.91),
        (1.83, 1.91),
        (1.80, 2.00),
        (1.67, 2.20),
        (1.57, 2.40),
        (2.10, 1.73),
        (2.30, 1.62),
        (2.50, 1.53),
    ]

    home_odds, away_odds = random.choice(market_pairs)

    home_implied = 1 / home_odds
    away_implied = 1 / away_odds
    total_implied = home_implied + away_implied

    home_no_vig = (home_implied / total_implied) * 100

    return {
        "home_odds": home_odds,
        "away_odds": away_odds,
        "home_implied": home_implied,
        "away_implied": away_implied,
        "total_implied": total_implied,
        "home_no_vig": home_no_vig,
    }


# -----------------------------------
# Session state setup
# -----------------------------------
def init_state():
    if "total_answered" not in st.session_state:
        st.session_state.total_answered = 0

    if "total_correct" not in st.session_state:
        st.session_state.total_correct = 0

    if "ip_problem" not in st.session_state:
        st.session_state.ip_problem = generate_implied_probability_problem()

    if "ev_problem" not in st.session_state:
        st.session_state.ev_problem = generate_ev_problem()

    if "nv_problem" not in st.session_state:
        st.session_state.nv_problem = generate_no_vig_problem()

    if "ip_answer" not in st.session_state:
        st.session_state.ip_answer = ""

    if "ev_answer" not in st.session_state:
        st.session_state.ev_answer = ""

    if "nv_answer" not in st.session_state:
        st.session_state.nv_answer = ""

    if "ip_feedback" not in st.session_state:
        st.session_state.ip_feedback = ""

    if "ev_feedback" not in st.session_state:
        st.session_state.ev_feedback = ""

    if "nv_feedback" not in st.session_state:
        st.session_state.nv_feedback = ""

    if "ip_checked" not in st.session_state:
        st.session_state.ip_checked = False

    if "ev_checked" not in st.session_state:
        st.session_state.ev_checked = False

    if "nv_checked" not in st.session_state:
        st.session_state.nv_checked = False


init_state()


# -----------------------------------
# Helpers
# -----------------------------------
def reset_ip_problem():
    st.session_state.ip_problem = generate_implied_probability_problem()
    st.session_state.ip_answer = ""
    st.session_state.ip_feedback = ""
    st.session_state.ip_checked = False


def reset_ev_problem():
    st.session_state.ev_problem = generate_ev_problem()
    st.session_state.ev_answer = ""
    st.session_state.ev_feedback = ""
    st.session_state.ev_checked = False


def reset_nv_problem():
    st.session_state.nv_problem = generate_no_vig_problem()
    st.session_state.nv_answer = ""
    st.session_state.nv_feedback = ""
    st.session_state.nv_checked = False


def reset_score():
    st.session_state.total_answered = 0
    st.session_state.total_correct = 0
    reset_ip_problem()
    reset_ev_problem()
    reset_nv_problem()


def check_ip_answer():
    if st.session_state.ip_checked:
        return

    answer_text = st.session_state.ip_answer.strip()

    try:
        user_answer = float(answer_text)
    except ValueError:
        st.session_state.ip_feedback = "Please enter a number like 52.38"
        return

    correct = st.session_state.ip_problem["correct_probability"]
    odds = st.session_state.ip_problem["odds"]

    st.session_state.total_answered += 1
    st.session_state.ip_checked = True

    if abs(user_answer - correct) <= 0.25:
        st.session_state.total_correct += 1
        st.session_state.ip_feedback = (
            f"✅ Correct!\n\n"
            f"Decimal odds = {odds:.2f}\n\n"
            f"Implied probability = 1 / {odds:.2f} = {1 / odds:.4f}\n\n"
            f"As a percentage: {(1 / odds) * 100:.2f}%"
        )
    else:
        st.session_state.ip_feedback = (
            f"❌ Not quite.\n\n"
            f"Correct answer: {correct:.2f}%\n\n"
            f"Work:\n"
            f"Implied probability = 1 / decimal odds\n\n"
            f"= 1 / {odds:.2f}\n\n"
            f"= {1 / odds:.4f}\n\n"
            f"= {correct:.2f}%"
        )


def check_ev_answer():
    if st.session_state.ev_checked:
        return

    answer_text = st.session_state.ev_answer.strip()

    try:
        user_answer = float(answer_text)
    except ValueError:
        st.session_state.ev_feedback = "Please enter a number like 5.00 or -3.50"
        return

    odds = st.session_state.ev_problem["odds"]
    model_probability = st.session_state.ev_problem["model_probability"]
    correct = st.session_state.ev_problem["correct_ev"]

    st.session_state.total_answered += 1
    st.session_state.ev_checked = True

    if abs(user_answer - correct) <= 0.5:
        st.session_state.total_correct += 1
        st.session_state.ev_feedback = (
            f"✅ Correct!\n\n"
            f"EV = p × odds − 1\n\n"
            f"= ({model_probability / 100:.2f}) × {odds:.2f} − 1\n\n"
            f"= {(model_probability / 100) * odds:.4f} − 1\n\n"
            f"= {((model_probability / 100) * odds - 1):.4f}\n\n"
            f"As a percentage: {correct:.2f}%"
        )
    else:
        st.session_state.ev_feedback = (
            f"❌ Not quite.\n\n"
            f"Correct answer: {correct:.2f}%\n\n"
            f"Work:\n"
            f"EV = p × odds − 1\n\n"
            f"= ({model_probability / 100:.2f}) × {odds:.2f} − 1\n\n"
            f"= {(model_probability / 100) * odds:.4f} − 1\n\n"
            f"= {((model_probability / 100) * odds - 1):.4f}\n\n"
            f"= {correct:.2f}%"
        )


def check_nv_answer():
    if st.session_state.nv_checked:
        return

    answer_text = st.session_state.nv_answer.strip()

    try:
        user_answer = float(answer_text)
    except ValueError:
        st.session_state.nv_feedback = "Please enter a number like 51.20"
        return

    problem = st.session_state.nv_problem
    correct = problem["home_no_vig"]

    st.session_state.total_answered += 1
    st.session_state.nv_checked = True

    if abs(user_answer - correct) <= 0.35:
        st.session_state.total_correct += 1
        st.session_state.nv_feedback = (
            f"✅ Correct!\n\n"
            f"Step 1: Convert both sides to implied probability\n\n"
            f"Home = 1 / {problem['home_odds']:.2f} = {problem['home_implied']:.4f}\n\n"
            f"Away = 1 / {problem['away_odds']:.2f} = {problem['away_implied']:.4f}\n\n"
            f"Step 2: Add them together\n\n"
            f"Total = {problem['home_implied']:.4f} + {problem['away_implied']:.4f} = {problem['total_implied']:.4f}\n\n"
            f"Step 3: Remove the vig from the home side\n\n"
            f"Home no-vig = {problem['home_implied']:.4f} / {problem['total_implied']:.4f} = "
            f"{problem['home_implied'] / problem['total_implied']:.4f}\n\n"
            f"As a percentage: {correct:.2f}%"
        )
    else:
        st.session_state.nv_feedback = (
            f"❌ Not quite.\n\n"
            f"Correct answer: {correct:.2f}%\n\n"
            f"Step 1: Convert both sides to implied probability\n\n"
            f"Home = 1 / {problem['home_odds']:.2f} = {problem['home_implied']:.4f}\n\n"
            f"Away = 1 / {problem['away_odds']:.2f} = {problem['away_implied']:.4f}\n\n"
            f"Step 2: Add them together\n\n"
            f"Total = {problem['home_implied']:.4f} + {problem['away_implied']:.4f} = {problem['total_implied']:.4f}\n\n"
            f"Step 3: Remove the vig from the home side\n\n"
            f"Home no-vig = {problem['home_implied']:.4f} / {problem['total_implied']:.4f} = "
            f"{problem['home_implied'] / problem['total_implied']:.4f}\n\n"
            f"= {correct:.2f}%"
        )


# -----------------------------------
# Sidebar
# -----------------------------------
st.sidebar.title("📘 Powerbook Training App")
page = st.sidebar.radio(
    "Choose section",
    ["Home", "Implied Probability Drill", "EV Drill", "No-Vig Drill", "Score Summary"],
)

st.sidebar.markdown("---")
st.sidebar.button("Reset All Scores", on_click=reset_score)


# -----------------------------------
# Header
# -----------------------------------
st.title("📘 Powerbook Training App")
st.subheader("Train your betting math like a real decision engine.")
st.caption(
    "Practice implied probability, EV, and core Powerbook concepts through interactive drills."
)


# -----------------------------------
# Pages
# -----------------------------------
if page == "Home":
    st.subheader("Welcome")
    st.write(
        """
This app is designed to help you practice the core betting math behind the **Powerbook system**.

Use it to build speed, confidence, and accuracy with the formulas that matter most when reading markets and evaluating bets.

### Version 1 includes:
- Implied Probability drills
- Expected Value (EV) drills
- No-Vig Probability drills
- Instant answer checking
- Running score tracking
- Step-by-step explanations
"""
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(
            """
**Implied Probability**

Implied Probability = 1 / Decimal Odds
"""
        )

    with col2:
        st.info(
            """
**Expected Value**

EV = p × odds − 1
"""
        )

    with col3:
        st.info(
            """
**No-Vig Probability**

No-Vig = Side Implied Probability / Total Implied Probability
"""
        )

elif page == "Implied Probability Drill":
    st.subheader("Implied Probability Drill")

    odds = st.session_state.ip_problem["odds"]

    st.write(f"### Decimal Odds: **{odds:.2f}**")
    st.write("Enter the implied probability as a percentage.")

    st.text_input(
        "Your answer (%)",
        key="ip_answer",
        placeholder="Example: 52.38",
    )

    col1, col2 = st.columns(2)

    with col1:
        st.button("Check Answer", on_click=check_ip_answer)

    with col2:
        st.button("Next Problem", on_click=reset_ip_problem)

    if st.session_state.ip_feedback:
        if st.session_state.ip_checked and "✅" in st.session_state.ip_feedback:
            st.success(st.session_state.ip_feedback)
        elif st.session_state.ip_checked and "❌" in st.session_state.ip_feedback:
            st.error(st.session_state.ip_feedback)
        else:
            st.warning(st.session_state.ip_feedback)

elif page == "EV Drill":
    st.subheader("EV Drill")

    odds = st.session_state.ev_problem["odds"]
    model_probability = st.session_state.ev_problem["model_probability"]

    st.write(f"### Decimal Odds: **{odds:.2f}**")
    st.write(f"### Model Probability: **{model_probability}%**")
    st.write("Enter EV as a percentage.")

    st.text_input(
        "Your answer (%)",
        key="ev_answer",
        placeholder="Example: 5.00 or -3.50",
    )

    col1, col2 = st.columns(2)

    with col1:
        st.button("Check EV Answer", on_click=check_ev_answer)

    with col2:
        st.button("Next EV Problem", on_click=reset_ev_problem)

    if st.session_state.ev_feedback:
        if st.session_state.ev_checked and "✅" in st.session_state.ev_feedback:
            st.success(st.session_state.ev_feedback)
        elif st.session_state.ev_checked and "❌" in st.session_state.ev_feedback:
            st.error(st.session_state.ev_feedback)
        else:
            st.warning(st.session_state.ev_feedback)

elif page == "No-Vig Drill":
    st.subheader("No-Vig Drill")

    home_odds = st.session_state.nv_problem["home_odds"]
    away_odds = st.session_state.nv_problem["away_odds"]

    st.write(f"### Home Odds: **{home_odds:.2f}**")
    st.write(f"### Away Odds: **{away_odds:.2f}**")
    st.write("Enter the **home team's no-vig probability** as a percentage.")

    st.text_input(
        "Your answer (%)",
        key="nv_answer",
        placeholder="Example: 51.20",
    )

    col1, col2 = st.columns(2)

    with col1:
        st.button("Check No-Vig Answer", on_click=check_nv_answer)

    with col2:
        st.button("Next No-Vig Problem", on_click=reset_nv_problem)

    if st.session_state.nv_feedback:
        if st.session_state.nv_checked and "✅" in st.session_state.nv_feedback:
            st.success(st.session_state.nv_feedback)
        elif st.session_state.nv_checked and "❌" in st.session_state.nv_feedback:
            st.error(st.session_state.nv_feedback)
        else:
            st.warning(st.session_state.nv_feedback)

elif page == "Score Summary":
    st.subheader("Score Summary")

    total_answered = st.session_state.total_answered
    total_correct = st.session_state.total_correct
    accuracy = (total_correct / total_answered * 100) if total_answered > 0 else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Questions Answered", total_answered)

    with col2:
        st.metric("Correct Answers", total_correct)

    with col3:
        st.metric("Accuracy", f"{accuracy:.1f}%")

    st.markdown("---")
    st.write(
        "Keep practicing until implied probability, no-vig, and EV calculations start to feel automatic."
    )
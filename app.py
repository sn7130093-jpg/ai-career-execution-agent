import streamlit as st
import pandas as pd
from supabase import create_client

st.set_page_config(
    page_title="AI Career Execution Agent",
    page_icon="🎯",
    layout="wide"
)

# Connect securely using Streamlit Secrets
try:
    supabase = create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )
except Exception:
    st.error(
        "Supabase is not configured yet. "
        "Please add SUPABASE_URL and SUPABASE_KEY "
        "in Streamlit Settings > Secrets."
    )
    st.stop()

CAREERS = {
    "Data Analyst": {
        "skills": ["Python", "SQL", "Excel", "Statistics", "Power BI"],
        "roadmap": [
            ("Excel", "Practice formulas, sorting, and pivot tables."),
            ("SQL", "Learn SELECT, WHERE, GROUP BY, and JOIN."),
            ("Python", "Practice Python basics and Pandas."),
            ("Statistics", "Study averages, distributions, and correlation."),
            ("Power BI", "Build an interactive dashboard.")
        ]
    },
    "AI/ML Engineer": {
        "skills": ["Python", "Statistics", "Machine Learning", "Pandas", "SQL"],
        "roadmap": [
            ("Python", "Practice functions, lists, dictionaries, and files."),
            ("Pandas", "Load, clean, and analyze datasets."),
            ("Statistics", "Learn probability, averages, and distributions."),
            ("Machine Learning", "Study regression, classification, and evaluation."),
            ("SQL", "Practice queries and database basics.")
        ]
    },
    "Web Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "Python", "SQL"],
        "roadmap": [
            ("HTML", "Create a webpage using headings, forms, and links."),
            ("CSS", "Practice layouts, colors, and responsive design."),
            ("JavaScript", "Learn variables, functions, and events."),
            ("Python", "Understand programming basics."),
            ("SQL", "Create tables and practice queries.")
        ]
    },
    "Python Developer": {
        "skills": ["Python", "SQL", "Git", "Problem Solving", "APIs"],
        "roadmap": [
            ("Python", "Practice functions, loops, and data structures."),
            ("Problem Solving", "Solve beginner programming exercises."),
            ("SQL", "Learn database queries and CRUD operations."),
            ("Git", "Practice commits and version control."),
            ("APIs", "Learn how to call and use REST APIs.")
        ]
    }
}

# Authentication
if "user_email" not in st.session_state:
    st.session_state.user_email = None

if not st.session_state.user_email:
    st.title("🎯 AI Career Execution Agent")
    st.write("Sign in to create your personalized career roadmap.")

    login_tab, register_tab = st.tabs(["Login", "Register"])

    with login_tab:
        with st.form("login_form"):
            email = st.text_input("Email address", key="login_email")
            password = st.text_input(
                "Password", type="password", key="login_password"
            )
            login_clicked = st.form_submit_button(
                "Login", type="primary"
            )

        if login_clicked:
            try:
                result = supabase.auth.sign_in_with_password({
                    "email": email.strip(),
                    "password": password
                })
                st.session_state.user_email = result.user.email
                st.rerun()
            except Exception:
                st.error(
                    "Login failed. Check your email and password. "
                    "If you just registered, confirm your email first."
                )

    with register_tab:
        with st.form("register_form"):
            new_email = st.text_input("Email address", key="register_email")
            new_password = st.text_input(
                "Create password (at least 6 characters)",
                type="password",
                key="register_password"
            )
            confirm_password = st.text_input(
                "Confirm password",
                type="password",
                key="confirm_password"
            )
            register_clicked = st.form_submit_button(
                "Create account", type="primary"
            )

        if register_clicked:
            if not new_email.strip() or not new_password:
                st.error("Enter an email address and password.")
            elif new_password != confirm_password:
                st.error("The passwords do not match.")
            elif len(new_password) < 6:
                st.error("Use a password with at least 6 characters.")
            else:
                try:
                    result = supabase.auth.sign_up({
                        "email": new_email.strip(),
                        "password": new_password
                    })
                    if result.session:
                        st.session_state.user_email = result.user.email
                        st.success("Account created!")
                        st.rerun()
                    else:
                        st.success(
                            "Registration submitted. Check your email "
                            "for a confirmation link, then log in."
                        )
                except Exception:
                    st.error(
                        "Registration failed. The email may already be "
                        "registered, or Supabase may require another step."
                    )

    st.stop()

# Main application, available after login
st.sidebar.success(f"Signed in as {st.session_state.user_email}")

if st.sidebar.button("Logout"):
    try:
        supabase.auth.sign_out()
    except Exception:
        pass
    st.session_state.user_email = None
    st.session_state.pop("analyzed", None)
    st.rerun()

st.title("🎯 AI Career Execution Agent")
st.write(
    "Discover suitable career paths, identify skill gaps, "
    "and create a personalized learning roadmap."
)

st.sidebar.header("Your Career Profile")
name = st.sidebar.text_input("Your name (optional)")
career = st.sidebar.selectbox(
    "Choose your target career",
    list(CAREERS.keys())
)

all_skills = sorted({
    skill
    for details in CAREERS.values()
    for skill in details["skills"]
})

current_skills = st.sidebar.multiselect(
    "Select skills you already know",
    all_skills
)

st.sidebar.caption(
    "Select only skills you have some knowledge of."
)

if st.sidebar.button("Analyze My Career", type="primary"):
    st.session_state["analyzed"] = True

if st.session_state.get("analyzed", False):
    required = CAREERS[career]["skills"]
    missing = [s for s in required if s not in current_skills]
    matched = [s for s in required if s in current_skills]

    st.subheader(f"Hello {name.strip() or 'Future Professional'}!")
    st.write(f"### Recommended preparation: {career}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Required skills", len(required))
    col2.metric("Skills you know", len(matched))
    col3.metric("Skills to develop", len(missing))

    progress = len(matched) / len(required)
    st.write("Current skill coverage")
    st.progress(progress, text=f"{progress:.0%} skill coverage")

    st.subheader("📊 Skill Gap Analysis")
    results = pd.DataFrame({
        "Skill": required,
        "Status": [
            "Known" if skill in current_skills else "Needs learning"
            for skill in required
        ]
    })
    st.dataframe(results, use_container_width=True, hide_index=True)

    st.subheader("🗺️ Your Personalized Learning Roadmap")
    for number, (skill, task) in enumerate(
        CAREERS[career]["roadmap"], start=1
    ):
        if skill in missing:
            st.checkbox(
                f"Step {number}: {skill} — {task}",
                key=f"{career}_{skill}_completed"
            )
        else:
            st.markdown(
                f"- ✅ **{skill}:** {task} "
                "(already selected as known)"
            )

    completed = sum(
        st.session_state.get(f"{career}_{skill}_completed", False)
        for skill in missing
    )
    total = len(missing)

    if total:
        st.write("Roadmap completion")
        st.progress(
            completed / total,
            text=f"{completed} of {total} learning steps completed"
        )
    else:
        st.success("You selected all required skills!")

    st.subheader("💡 Career Preparation Advice")
    if missing:
        st.write(
            "Start with the first missing skill in your roadmap. "
            "Practice it with a small project, then move to the next skill."
        )

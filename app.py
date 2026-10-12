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
# Authentication - Email and Password

APP_URL = "https://ai-career-execution-agent-tzhqzd27gmfgqb7dtnbqzj.streamlit.app"

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "recovery_mode" not in st.session_state:
    st.session_state.recovery_mode = False

# Handle the recovery code returned by Supabase
recovery_code = st.query_params.get("code")

if recovery_code and not st.session_state.recovery_mode:
    try:
        supabase.auth.exchange_code_for_session(recovery_code)
        st.session_state.recovery_mode = True
        st.query_params.clear()
        st.rerun()
    except Exception:
        st.error(
            "This reset link is invalid or expired. "
            "Request a new password reset email."
        )
        st.stop()

# Show the new-password form
if st.session_state.recovery_mode:
    st.subheader("🔐 Set a New Password")

    new_password = st.text_input(
        "New password",
        type="password",
        key="new_password"
    )
    confirm_password = st.text_input(
        "Confirm new password",
        type="password",
        key="confirm_new_password"
    )

    if st.button("Update Password", type="primary"):
        if len(new_password) < 8:
            st.error("Password must be at least 8 characters.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            try:
                supabase.auth.update_user({"password": new_password})
                st.session_state.recovery_mode = False
                st.session_state.user_email = None
                supabase.auth.sign_out()
                st.success(
                    "Password updated successfully. Please log in "
                    "using your new password."
                )
            except Exception:
                st.error(
                    "Password update failed. Request a fresh reset link "
                    "and try again."
                )

    st.stop()

# Normal login and signup
if not st.session_state.user_email:
    st.subheader("🔐 AI Career Execution Agent")
    st.write("Sign in or create an account to continue.")

    auth_mode = st.radio(
        "Choose an option",
        ["Log In", "Create Account"],
        horizontal=True
    )

    email = st.text_input("Email address").strip()
    password = st.text_input("Password", type="password")

    if st.button("Reset Password"):
        if not email or "@" not in email:
            st.error("Enter your registered email address first.")
        else:
            try:
                supabase.auth.reset_password_for_email(
                    email,
                    options={"redirect_to": APP_URL}
                )
                st.success(
                    "Check your inbox and spam folder for the reset link."
                )
            except Exception:
                st.error(
                    "Could not send reset email. Check Supabase settings."
                )

    if st.button(auth_mode, type="primary"):
        if not email or not password:
            st.error("Please enter your email and password.")
        else:
            try:
                if auth_mode == "Create Account":
                    result = supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })

                    if result.session and result.user:
                        st.session_state.user_email = result.user.email
                        st.rerun()
                    else:
                        st.info(
                            "Check your email to confirm your account, "
                            "then log in."
                        )
                else:
                    result = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    if result.user and result.session:
                        st.session_state.user_email = result.user.email
                        st.rerun()
                    else:
                        st.error("Login unsuccessful. Please try again.")

            except Exception as e:
                st.error(f"Authentication failed: {e}")

    st.stop()# Authentication - Email and Password

APP_URL = "https://ai-career-execution-agent-tzhqzd27gmfgqb7dtnbqzj.streamlit.app"

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "recovery_mode" not in st.session_state:
    st.session_state.recovery_mode = False

# Handle the recovery code returned by Supabase
recovery_code = st.query_params.get("code")

if recovery_code and not st.session_state.recovery_mode:
    try:
        supabase.auth.exchange_code_for_session(recovery_code)
        st.session_state.recovery_mode = True
        st.query_params.clear()
        st.rerun()
    except Exception:
        st.error(
            "This reset link is invalid or expired. "
            "Request a new password reset email."
        )
        st.stop()

# Show the new-password form
if st.session_state.recovery_mode:
    st.subheader("🔐 Set a New Password")

    new_password = st.text_input(
        "New password",
        type="password",
        key="new_password"
    )
    confirm_password = st.text_input(
        "Confirm new password",
        type="password",
        key="confirm_new_password"
    )

    if st.button("Update Password", type="primary"):
        if len(new_password) < 8:
            st.error("Password must be at least 8 characters.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            try:
                supabase.auth.update_user({"password": new_password})
                st.session_state.recovery_mode = False
                st.session_state.user_email = None
                supabase.auth.sign_out()
                st.success(
                    "Password updated successfully. Please log in "
                    "using your new password."
                )
            except Exception:
                st.error(
                    "Password update failed. Request a fresh reset link "
                    "and try again."
                )

    st.stop()

# Normal login and signup
if not st.session_state.user_email:
    st.subheader("🔐 AI Career Execution Agent")
    st.write("Sign in or create an account to continue.")

    auth_mode = st.radio(
        "Choose an option",
        ["Log In", "Create Account"],
        horizontal=True
    )

    email = st.text_input("Email address").strip()
    password = st.text_input("Password", type="password")

    if st.button("Reset Password"):
        if not email or "@" not in email:
            st.error("Enter your registered email address first.")
        else:
            try:
                supabase.auth.reset_password_for_email(
                    email,
                    options={"redirect_to": APP_URL}
                )
                st.success(
                    "Check your inbox and spam folder for the reset link."
                )

    if st.button(auth_mode, type="primary"):
        if not email or not password:
            st.error("Please enter your email and password.")
        else:
            except Exception as e:
                 st.error(f"Password reset error: {e}")
                    try:
                if auth_mode == "Create Account":
                    result = supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })

                    if result.session and result.user:
                        st.session_state.user_email = result.user.email
                        st.rerun()
                    else:
                        st.info(
                            "Check your email to confirm your account, "
                            "then log in."
                        )
                else:
                    result = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    if result.user and result.session:
                        st.session_state.user_email = result.user.email
                        st.rerun()
                    else:
                        st.error("Login unsuccessful. Please try again.")

            except Exception as e:
                st.error(f"Authentication failed: {e}")

    st.stop()
# Authentication - Email and Password

APP_URL = "https://ai-career-execution-agent-tzhqzd27gmfgqb7dtnbqzj.streamlit.app"

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "recovery_mode" not in st.session_state:
    st.session_state.recovery_mode = False

# Handle the recovery code returned by Supabase
recovery_code = st.query_params.get("code")

if recovery_code and not st.session_state.recovery_mode:
    try:
        supabase.auth.exchange_code_for_session(recovery_code)
        st.session_state.recovery_mode = True
        st.query_params.clear()
        st.rerun()
    except Exception:
        st.error(
            "This reset link is invalid or expired. "
            "Request a new password reset email."
        )
        st.stop()

# Show the new-password form
if st.session_state.recovery_mode:
    st.subheader("🔐 Set a New Password")

    new_password = st.text_input(
        "New password",
        type="password",
        key="new_password"
    )
    confirm_password = st.text_input(
        "Confirm new password",
        type="password",
        key="confirm_new_password"
    )

    if st.button("Update Password", type="primary"):
        if len(new_password) < 8:
            st.error("Password must be at least 8 characters.")
        elif new_password != confirm_password:
            st.error("Passwords do not match.")
        else:
            try:
                supabase.auth.update_user({"password": new_password})
                st.session_state.recovery_mode = False
                st.session_state.user_email = None
                supabase.auth.sign_out()
                st.success(
                    "Password updated successfully. Please log in "
                    "using your new password."
                )
            except Exception:
                st.error(
                    "Password update failed. Request a fresh reset link "
                    "and try again."
                )

    st.stop()

# Normal login and signup
if not st.session_state.user_email:
    st.subheader("🔐 AI Career Execution Agent")
    st.write("Sign in or create an account to continue.")

    auth_mode = st.radio(
        "Choose an option",
        ["Log In", "Create Account"],
        horizontal=True
    )

    email = st.text_input("Email address").strip()
    password = st.text_input("Password", type="password")

    if st.button("Reset Password"):
        if not email or "@" not in email:
            st.error("Enter your registered email address first.")
        else:
            try:
                supabase.auth.reset_password_for_email(
                    email,
                    options={"redirect_to": APP_URL}
                )
                st.success(
                    "Check your inbox and spam folder for the reset link."
                )
            except Exception:
                st.error(
                    "Could not send reset email. Check Supabase settings."
                )

    if st.button(auth_mode, type="primary"):
        if not email or not password:
            st.error("Please enter your email and password.")
        else:
            try:
                if auth_mode == "Create Account":
                    result = supabase.auth.sign_up({
                        "email": email,
                        "password": password
                    })

                    if result.session and result.user:
                        st.session_state.user_email = result.user.email
                        st.rerun()
                    else:
                        st.info(
                            "Check your email to confirm your account, "
                            "then log in."
                        )
                else:
                    result = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": password
                    })

                    if result.user and result.session:
                        st.session_state.user_email = result.user.email
                        st.rerun()
                    else:
                        st.error("Login unsuccessful. Please try again.")

            except Exception as e:
                st.error(f"Authentication failed: {e}")

    st.stop()
# ==============================
# AUTHENTICATION: SUPABASE
# ==============================

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "reset_mode" not in st.session_state:
    st.session_state.reset_mode = False

if not st.session_state.user_email:

    st.subheader("🔐 AI Career Execution Agent")

    # PASSWORD RESET FORM
    if st.session_state.reset_mode:

        st.write("Reset your password")

        reset_email = st.text_input(
            "Registered email address",
            key="reset_email"
        )

        if st.button("Send Reset Link"):
            if not reset_email or "@" not in reset_email:
                st.error("Enter a valid email address.")
            else:
                try:
                    supabase.auth.reset_password_for_email(
                        reset_email,
                        {
                            "redirect_to":
                            "https://ai-career-execution-agent-tzhqzd27gmfgqb7dtnbqzj.streamlit.app/"
                        }
                    )
                    st.success(
                        "If the email is registered, check your inbox "
                        "and spam folder for the reset link."
                    )
                except Exception:
                    st.error(
                        "Could not send reset email. Check Supabase "
                        "email settings and redirect URLs."
                    )

        if st.button("Back to Login"):
            st.session_state.reset_mode = False
            st.rerun()

    # NEW PASSWORD FORM
    elif st.query_params.get("type") == "recovery":

        st.write("Choose a new password")

        new_password = st.text_input(
            "New password",
            type="password",
            key="new_password"
        )

        confirm_password = st.text_input(
            "Confirm new password",
            type="password",
            key="confirm_password"
        )

        if st.button("Update Password"):
            if len(new_password) < 8:
                st.error("Use at least 8 characters.")
            elif new_password != confirm_password:
                st.error("Passwords do not match.")
            else:
                try:
                    supabase.auth.update_user({
                        "password": new_password
                    })
                    st.success(
                        "Password updated. Return to login."
                    )
                    st.session_state.reset_mode = False
                except Exception:
                    st.error(
                        "Password update failed. Open the reset link "
                        "again and try once more."
                    )

    # LOGIN AND ACCOUNT CREATION
    else:

        auth_mode = st.radio(
            "Choose an option",
            ["Log In", "Create Account"],
            horizontal=True
        )

        email = st.text_input(
            "Email address",
            key="auth_email"
        ).strip()

        password = st.text_input(
            "Password",
            type="password",
            key="auth_password"
        )

        if st.button("Forgot Password?"):
            st.session_state.reset_mode = True
            st.rerun()

        if st.button(auth_mode, type="primary"):

            if not email or not password:
                st.error("Enter your email and password.")
            else:
                try:
                    if auth_mode == "Create Account":

                        result = supabase.auth.sign_up({
                            "email": email,
                            "password": password
                        })

                        if result.session and result.user:
                            st.session_state.user_email = (
                                result.user.email
                            )
                            st.rerun()
                        else:
                            st.success(
                                "Check your email to confirm your "
                                "account, then log in."
                            )

                    else:

                        result = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })

                        if result.user and result.session:
                            st.session_state.user_email = (
                                result.user.email
                            )
                            st.rerun()
                        else:
                            st.error("Login failed. Try again.")

                except Exception as e:
                    st.error(f"Authentication failed: {e}")

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

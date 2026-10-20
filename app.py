import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from supabase import create_client
from streamlit_url_fragments import get_fragments
from urllib.parse import parse_qs

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
except Exception as e:
    st.error(f"Login failed: {e}")
    st.stop()
def recommend_careers(student_skills, student_interests, careers, top_n=3):
    """Rank careers by similarity to the student's current skills."""

    if not careers:
        return []

    career_names = list(careers.keys())

    documents = [
    " ".join(student_skills + student_interests).lower()
]
    documents.extend(
        " ".join(details["skills"]).lower()
        for details in careers.values()
    )

    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(documents)

    scores = cosine_similarity(
        matrix[0:1],
        matrix[1:]
    ).flatten()

    results = []

    for index, name in enumerate(career_names):
        required_skills = careers[name]["skills"]
        known = [
            skill for skill in required_skills
            if skill.lower() in {
                item.lower() for item in student_skills
            }
        ]
        missing = [
            skill for skill in required_skills
            if skill.lower() not in {
                item.lower() for item in student_skills
            }
        ]

        results.append({
            "Career": name,
            "Similarity (%)": round(float(scores[index]) * 100, 1),
            "Matched Skills": ", ".join(known) or "None yet",
            "Skills to Learn": ", ".join(missing) or "None"
        })

    results.sort(
        key=lambda item: item["Similarity (%)"],
        reverse=True
    )

    return results[:top_n]
CAREERS = {
    "Engineering & Technology": {
        "skills": ["Python", "SQL", "Git", "Problem Solving", "APIs"],
        "roadmap": [
            ("Python", "Learn variables, loops, functions, and data structures."),
            ("SQL", "Practice database queries."),
            ("Git", "Learn version control and commits."),
            ("Problem Solving", "Solve beginner programming exercises."),
            ("APIs", "Build a small application using an API.")
        ]
    },
    "Data Analyst": {
        "skills": ["Excel", "SQL", "Python", "Statistics", "Power BI"],
        "roadmap": [
            ("Excel", "Practice formulas and pivot tables."),
            ("SQL", "Learn SELECT, WHERE, GROUP BY, and JOIN."),
            ("Python", "Practice data analysis with Pandas."),
            ("Statistics", "Learn averages and distributions."),
            ("Power BI", "Create an interactive dashboard.")
        ]
    },
    "AI/ML Engineer": {
        "skills": ["Python", "Statistics", "Machine Learning", "Pandas", "SQL"],
        "roadmap": [
            ("Python", "Practice Python programming."),
            ("Statistics", "Learn probability and averages."),
            ("Pandas", "Clean and analyze datasets."),
            ("Machine Learning", "Study regression and classification."),
            ("SQL", "Practice database queries.")
        ]
    },
    "Web Developer": {
        "skills": ["HTML", "CSS", "JavaScript", "Git", "APIs"],
        "roadmap": [
            ("HTML", "Create webpages with headings, forms, and links."),
            ("CSS", "Practice layouts and responsive design."),
            ("JavaScript", "Learn variables, functions, and events."),
            ("Git", "Save projects using version control."),
            ("APIs", "Connect a webpage to an API.")
        ]
    },
    "Commerce & Accounting": {
        "skills": ["Excel", "Accounting", "Communication", "Business Maths", "Tax Basics"],
        "roadmap": [
            ("Excel", "Practice spreadsheets and formulas."),
            ("Accounting", "Learn basic accounting entries."),
            ("Communication", "Practice professional emails."),
            ("Business Maths", "Learn percentages and financial calculations."),
            ("Tax Basics", "Study introductory tax concepts.")
        ]
    },
    "Banking & Finance": {
        "skills": ["Numerical Ability", "Reasoning", "English", "Excel", "Financial Awareness"],
        "roadmap": [
            ("Numerical Ability", "Practice percentages, ratios, and averages."),
            ("Reasoning", "Solve logical reasoning questions."),
            ("English", "Practice grammar and comprehension."),
            ("Excel", "Learn formulas and tables."),
            ("Financial Awareness", "Study banking and finance basics.")
        ]
    },
    "Business & Management": {
        "skills": ["Communication", "Leadership", "Excel", "Planning", "Problem Solving"],
        "roadmap": [
            ("Communication", "Practice presentations and emails."),
            ("Leadership", "Learn teamwork and delegation."),
            ("Excel", "Track tasks and business data."),
            ("Planning", "Create a simple project plan."),
            ("Problem Solving", "Practice real-world case studies.")
        ]
    },
    "Arts & Humanities": {
        "skills": ["Writing", "Research", "Communication", "Critical Thinking", "Presentation"],
        "roadmap": [
            ("Writing", "Write short articles and summaries."),
            ("Research", "Find and compare reliable sources."),
            ("Communication", "Practice clear spoken communication."),
            ("Critical Thinking", "Evaluate arguments and evidence."),
            ("Presentation", "Prepare a short presentation.")
        ]
    },
    "Teaching & Education": {
        "skills": ["Communication", "Subject Knowledge", "Presentation", "Planning", "Digital Skills"],
        "roadmap": [
            ("Subject Knowledge", "Strengthen your chosen subject."),
            ("Communication", "Explain concepts in simple language."),
            ("Presentation", "Prepare a sample lesson."),
            ("Planning", "Create a lesson plan."),
            ("Digital Skills", "Practice online teaching tools.")
        ]
    },
    "Science & Research": {
        "skills": ["Research", "Statistics", "Excel", "Scientific Writing", "Data Analysis"],
        "roadmap": [
            ("Research", "Learn how to frame a research question."),
            ("Statistics", "Study basic statistical concepts."),
            ("Excel", "Organize and analyze data."),
            ("Scientific Writing", "Write a short research summary."),
            ("Data Analysis", "Interpret a small dataset.")
        ]
    },
    "Healthcare & Life Sciences": {
        "skills": ["Biology", "Communication", "Research", "Data Analysis", "Digital Skills"],
        "roadmap": [
            ("Biology", "Revise foundational biology concepts."),
            ("Communication", "Practice clear and respectful communication."),
            ("Research", "Learn to read reliable scientific sources."),
            ("Data Analysis", "Practice interpreting simple data."),
            ("Digital Skills", "Learn common digital documentation tools.")
        ]
    },
    "Digital Marketing": {
        "skills": ["Writing", "Social Media", "SEO", "Analytics", "Design Basics"],
        "roadmap": [
            ("Writing", "Create sample promotional content."),
            ("Social Media", "Plan a weekly content calendar."),
            ("SEO", "Learn keywords and search basics."),
            ("Analytics", "Understand engagement metrics."),
            ("Design Basics", "Create simple promotional graphics.")
        ]
    },
    "Graphic Designer": {
        "skills": ["Design Basics", "Typography", "Color Theory", "Creativity", "Portfolio"],
        "roadmap": [
            ("Design Basics", "Learn layout and visual hierarchy."),
            ("Typography", "Practice font pairing."),
            ("Color Theory", "Create balanced color palettes."),
            ("Creativity", "Redesign a simple poster."),
            ("Portfolio", "Collect your best design samples.")
        ]
    },
    "Content Writer": {
        "skills": ["Writing", "Grammar", "Research", "SEO", "Editing"],
        "roadmap": [
            ("Writing", "Write a short article."),
            ("Grammar", "Practice sentence clarity."),
            ("Research", "Verify facts using reliable sources."),
            ("SEO", "Learn basic keyword research."),
            ("Editing", "Revise an article for clarity.")
        ]
    },
    "Human Resources": {
        "skills": ["Communication", "Excel", "Recruitment Basics", "Organization", "Interviewing"],
        "roadmap": [
            ("Communication", "Practice professional emails."),
            ("Excel", "Create a candidate tracking sheet."),
            ("Recruitment Basics", "Learn the recruitment process."),
            ("Organization", "Practice scheduling and record keeping."),
            ("Interviewing", "Learn structured interview questions.")
        ]
    },
    "Customer Support": {
        "skills": ["Communication", "Problem Solving", "Typing", "Email Writing", "Digital Skills"],
        "roadmap": [
            ("Communication", "Practice polite customer conversations."),
            ("Problem Solving", "Work through sample customer issues."),
            ("Typing", "Practice typing accurately."),
            ("Email Writing", "Draft clear support responses."),
            ("Digital Skills", "Learn ticketing-system basics.")
        ]
    },
    "Government Jobs & Competitive Exams": {
        "skills": ["Numerical Ability", "Reasoning", "English", "General Knowledge", "Computer Basics"],
        "roadmap": [
            ("Numerical Ability", "Practice arithmetic fundamentals."),
            ("Reasoning", "Solve basic logic questions."),
            ("English", "Study grammar and comprehension."),
            ("General Knowledge", "Follow reliable current affairs sources."),
            ("Computer Basics", "Revise common computer concepts.")
        ]
    },
    "Entrepreneurship": {
        "skills": ["Communication", "Planning", "Marketing", "Budgeting", "Problem Solving"],
        "roadmap": [
            ("Planning", "Identify a problem worth solving."),
            ("Marketing", "Define a target audience."),
            ("Budgeting", "Estimate costs and revenue."),
            ("Communication", "Prepare a simple business pitch."),
            ("Problem Solving", "Test your idea on a small scale.")
        ]
    }
}

# Authentication
if "user_email" not in st.session_state:
    st.session_state.user_email = None

if not st.session_state.user_email:
    fragments = get_fragments()

    if isinstance(fragments, dict):
        st.session_state["recovery_fragments"] = fragments
    elif isinstance(fragments, str):
        st.session_state["recovery_fragments"] = parse_qs(fragments)
    st.title("🎯 AI Career Execution Agent")
    st.write("Sign in to create your personalized career roadmap.")

    login_tab, register_tab, forgot_password_tab = st.tabs(["Login", "Register", "Forgot Password"])

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
            except Exception as e:
                st.error(f"Login error: {e}")

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
                except Exception as e:
                    st.error(f"Registration error: {e}")

    with forgot_password_tab:
        st.subheader("Forgot Password")
        reset_email = st.text_input(
            "Enter your registered email",
            key="reset_email"
        )

        if st.button("Send Reset Link"):
            if not reset_email.strip():
                st.warning("Please enter your email.")
            else:
                try:
                    supabase.auth.reset_password_for_email(
                        reset_email.strip(),
                        {
                            "redirect_to": "https://ai-career-execution-agent-tzhqzd27gmfgqb7dtnbqzj.streamlit.app"
                        }
                    )
                    st.success(
                        "If the account exists, a password reset email will be sent."
                    )
                except Exception:
                    st.error("Could not send the reset email. Please try again later.")
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

education_level = st.sidebar.selectbox(
    "Your education level",
    [
        "10th / SSC",
        "Intermediate / 12th",
        "Diploma",
        "Undergraduate Degree",
        "Postgraduate Degree",
        "Other"
    ]
)

education_background = st.sidebar.selectbox(
    "Your education background",
    [
        "Engineering & Technology",
        "Commerce & Accounting",
        "Arts & Humanities",
        "Science",
        "Healthcare & Life Sciences",
        "Management",
        "Education",
        "Creative & Digital",
        "Other"
    ]
)

career = st.sidebar.selectbox(
    "Choose your target career",
    list(CAREERS.keys())
)
student_interests = st.sidebar.multiselect(
    "Your career interests",
    [
        "Data Analysis",
        "Programming",
        "Artificial Intelligence",
        "Business",
        "Finance",
        "Research",
        "Healthcare",
        "Teaching",
        "Design",
        "Writing",
        "Communication",
        "Problem Solving"
    ],
    help="Select interests that you enjoy."
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
    st.subheader("🤖 Smart Career Recommendations")

    if current_skills or student_interests:
        recommendations = recommend_careers(
    current_skills,
    student_interests,
    CAREERS,
    top_n=3
)

        if recommendations:
            st.caption(
                "Ranked by skill-profile similarity. "
                "Scores are similarity measures, not success probabilities."
            )

            for item in recommendations:
                st.markdown(
                    f"**{item['Career']} — "
                    f"{item['Similarity (%)']}% similarity**"
                )
                st.write(
                    f"Matched skills: {item['Matched Skills']}"
                )
                st.write(
                    f"Skills to learn: {item['Skills to Learn']}"
                )
        else:
            st.info("No recommendations are available yet.")
    else:
        st.info(
           "Select at least one skill or interest in the sidebar "
"to get smart career recommendations."
        )
    st.subheader("🎓 Education-Based Career Guidance")

    if education_level == "10th / SSC":
        st.info(
            "After SSC, you can explore Intermediate, ITI, or Diploma "
            "pathways. Check the eligibility requirements for your chosen career."
        )
    elif education_level == "Intermediate / 12th":
        st.info(
            "Your next options may include a degree, diploma, professional "
            "course, or eligible entry-level job, depending on your subjects."
        )
    elif education_level == "Diploma":
        st.info(
            "Explore diploma-related jobs, further study, or degree entry "
            "options. Requirements vary by course and employer."
        )
    elif education_level == "Undergraduate Degree":
        st.info(
            "Explore entry-level jobs, internships, competitive exams, "
            "or further study that match your degree and skills."
        )
    elif education_level == "Postgraduate Degree":
        st.info(
            "Explore specialist roles, research, teaching where eligible, "
            "and jobs matching your postgraduate qualification."
        )
    else:
        st.info(
            "Check the qualification requirements for your target career "
            "and choose a suitable learning pathway."
        )

    st.caption(f"Selected education background: {education_background}")

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
    st.subheader("🎤 Interview Preparation")

    interview_level = st.selectbox(
        "Choose interview difficulty",
        ["Beginner", "Intermediate", "Advanced"],
        key="interview_level"
    )

    interview_questions = {
        "AI/ML Engineer": {
            "Beginner": [
                ("What is Artificial Intelligence?",
                 "AI is the ability of machines to perform tasks that normally require human intelligence."),
                ("What is Machine Learning?",
                 "Machine Learning enables computers to learn patterns from data."),
                ("What is Python used for in AI?",
                 "Python is used for data processing, model building and evaluation.")
            ],
            "Intermediate": [
                ("What is overfitting?",
                 "Overfitting happens when a model learns training data too closely and performs poorly on unseen data."),
                ("What is the difference between classification and regression?",
                 "Classification predicts categories, while regression predicts numerical values."),
                ("What is train-test splitting?",
                 "It separates data for training a model and evaluating it on unseen examples.")
            ],
            "Advanced": [
                ("Explain precision and recall.",
                 "Precision measures how many positive predictions are correct; recall measures how many actual positives are identified."),
                ("What is cross-validation?",
                 "It evaluates a model across multiple data splits to estimate how well it generalizes."),
                ("How would you handle imbalanced data?",
                 "Possible approaches include class weighting, resampling and choosing suitable evaluation metrics.")
            ]
        },
        "Data Analyst": {
            "Beginner": [
                ("What does a Data Analyst do?",
                 "A Data Analyst cleans, examines and interprets data to help make decisions."),
                ("What is SQL?",
                 "SQL is used to retrieve and manage data in relational databases."),
                ("What is a spreadsheet used for?",
                 "Spreadsheets help organize, calculate, analyze and visualize data.")
            ],
            "Intermediate": [
                ("What is the difference between WHERE and HAVING?",
                 "WHERE filters rows before grouping; HAVING filters groups after aggregation."),
                ("How do you handle missing values?",
                 "Inspect why values are missing, then remove or impute values when appropriate."),
                ("What is a KPI?",
                 "A Key Performance Indicator measures progress toward an important objective.")
            ],
            "Advanced": [
                ("How would you investigate a sudden sales decline?",
                 "Validate the data, compare periods and segments, identify contributing factors, and communicate evidence."),
                ("What is a window function in SQL?",
                 "It calculates across related rows without collapsing them into a single grouped row."),
                ("How would you validate a dashboard?",
                 "Check data sources, calculations, filters, totals and consistency against trusted reports.")
            ]
        },
        "Web Developer": {
            "Beginner": [
                ("What is HTML?",
                 "HTML structures the content of a web page."),
                ("What is CSS?",
                 "CSS controls the appearance and layout of a web page."),
                ("What is JavaScript?",
                 "JavaScript adds interactive behavior to web pages.")
            ],
            "Intermediate": [
                ("What is an API?",
                 "An API defines how software systems communicate."),
                ("What is responsive design?",
                 "It adapts a website layout to different screen sizes."),
                ("What is the difference between frontend and backend?",
                 "Frontend is the user-facing part; backend handles server-side logic and data.")
            ],
            "Advanced": [
                ("How would you improve website performance?",
                 "Measure bottlenecks, optimize assets and queries, and reduce unnecessary work."),
                ("What is authentication versus authorization?",
                 "Authentication verifies identity; authorization determines permitted actions."),
                ("How do you protect user input?",
                 "Validate input, use parameterized queries, encode output and apply appropriate security controls.")
            ]
        },
        "Banking & Finance": {
            "Beginner": [
                ("What is interest?",
                 "Interest is the cost of borrowing money or the return earned on savings."),
                ("What is a savings account?",
                 "It is a bank account for keeping money while earning applicable interest."),
                ("What is inflation?",
                 "Inflation is a general increase in prices over time.")
            ],
            "Intermediate": [
                ("What is the difference between a debit and credit card?",
                 "A debit card usually uses money in your account; a credit card uses borrowed funds."),
                ("What is a fixed deposit?",
                 "It is a deposit kept for a specified term at an agreed interest rate."),
                ("What is a credit score?",
                 "It summarizes credit history and helps lenders assess credit risk.")
            ],
            "Advanced": [
                ("What is non-performing asset (NPA)?",
                 "An NPA is a loan or advance classified as non-performing under applicable banking rules."),
                ("What is liquidity risk?",
                 "It is the risk of being unable to meet financial obligations when due."),
                ("Why is KYC important?",
                 "Know Your Customer procedures help verify customer identity and reduce misuse of financial services.")
            ]
        },
        "Government Jobs & Competitive Exams": {
            "Beginner": [
                ("Why do you want a government job?",
                 "Explain your interest in public service, responsibility and the specific role."),
                ("What is the Constitution of India?",
                 "It is India's supreme legal framework for government and citizens' rights and duties."),
                ("What are current affairs?",
                 "They are important recent events in India and around the world.")
            ],
            "Intermediate": [
                ("What is the role of the Parliament?",
                 "Parliament makes laws, oversees government and approves public expenditure."),
                ("What is the difference between the Lok Sabha and Rajya Sabha?",
                 "The Lok Sabha is the House of the People; the Rajya Sabha is the Council of States."),
                ("How would you prepare for an aptitude test?",
                 "Build fundamentals, practise timed questions, review mistakes and take mock tests.")
            ],
            "Advanced": [
                ("How would you prioritize questions in a timed exam?",
                 "Answer familiar questions first, manage time and return to difficult questions if time remains."),
                ("How do you verify a current-affairs fact?",
                 "Check the date and confirm it using reliable official or reputable sources."),
                ("How would you handle an ethical dilemma at work?",
                 "Follow applicable rules, document the facts and consult the appropriate authority.")
            ]
        }
    }

    default_questions = {
        "Beginner": [
            ("Tell me about yourself.",
             "Briefly explain your education, skills, interests and career goal."),
            ("Why did you choose this career?",
             "Connect your interests and strengths to the role."),
            ("What skill are you currently improving?",
             "Name a real skill and explain how you practise it.")
        ],
        "Intermediate": [
            ("Describe a project you worked on.",
             "Explain its goal, your contribution, tools used and outcome."),
            ("How do you solve a difficult problem?",
             "Break it down, investigate possible causes, test solutions and review the result."),
            ("How do you learn a new tool?",
             "Use documentation, practise with a small task and apply what you learn.")
        ],
        "Advanced": [
            ("Describe a challenging problem related to your target role.",
             "Use a specific example and explain your reasoning and outcome."),
            ("How would you measure success in this role?",
             "Choose measurable results relevant to the role and explain how you would track them."),
            ("Tell me about a mistake and what you learned.",
             "Give an honest example, explain your response and describe what you changed.")
        ]
    }

    selected_questions = interview_questions.get(
        career, default_questions
    ).get(interview_level, default_questions[interview_level])

    st.caption(
        f"Practice questions for your selected career: {career}"
    )

    for number, (question, answer) in enumerate(
        selected_questions, start=1
    ):
        with st.expander(f"Question {number}: {question}"):
            st.write("**Suggested answer:**")
            st.write(answer)

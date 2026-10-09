import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Career Execution Agent",
    page_icon="🎯",
    layout="wide"
)

st.title("🎯 AI Career Execution Agent")
st.write(
    "Discover suitable career paths, identify skill gaps, "
    "and create a personalized learning roadmap."
)

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
            st.markdown(f"- ✅ **{skill}:** {task} (already selected as known)")

    completed = sum(
        st.session_state.get(f"{career}_{skill}_completed", False)
        for skill in missing
    )
    total = len(missing)
    if total:
        st.write("Roadmap completion")
        st.progress(completed / total, text=f"{completed} of {total} learning steps completed")
    else:
        st.success("You selected all required skills!")

    st.subheader("💡 Career Preparation Advice")
    if missing:
        st.write(
            "Start with the first missing skill in your roadmap. "
            "Practice it with a small project, then move to the next skill."
        )
    else:
        st.write(
            "Review your skills and build a portfolio project "
            "to demonstrate your knowledge."
        )

    st.info(
        "These recommendations use a predefined career-skill dataset "
        "and rule-based matching. They are guidance, not a guarantee "
        "of employment or an automated hiring prediction."
    )
else:
    st.info(
        "Choose your target career and current skills in the sidebar, "
        "then click Analyze My Career to view your personalized results."
    )

st.caption("AI Career Execution Agent | Student Project Prototype") 

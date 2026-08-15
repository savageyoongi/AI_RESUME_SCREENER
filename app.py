import streamlit as st

from resume_parser import extract_text
from ai_analyzer import analyze_resume, match_job_description


st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="📄",
    layout="wide"
)


# -----------------------------
# Header
# -----------------------------

st.title("📄 AI Resume Screener")

st.markdown(
    """
    **AI-powered resume analysis and job recommendation system**

    Upload your resume to discover your skills, profile summary,
    recommended career role, and skill gaps.
    """
)

st.divider()


# -----------------------------
# Upload Resume
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf", "docx"],
    help="Supported formats: PDF and DOCX"
)


# Store resume text
resume_text = None


if uploaded_file:

    st.success(f"📎 {uploaded_file.name}")

    analyze_button = st.button(
        "🤖 Analyze Resume",
        type="primary"
    )

    if analyze_button:

        try:

            with st.spinner(
                "Reading your resume and generating AI analysis..."
            ):

                resume_text = extract_text(uploaded_file)

                if not resume_text.strip():

                    st.error(
                        "Unable to extract text from this resume."
                    )

                    st.stop()

                result = analyze_resume(resume_text)

            st.success("✅ Analysis completed!")


            # -----------------------------
            # Profile Summary
            # -----------------------------

            st.header("👤 Profile Summary")

            st.info(result["profile_summary"])


            # -----------------------------
            # Recommended Role
            # -----------------------------

            st.header("🎯 Recommended Job Role")

            col1, col2 = st.columns(2)

            with col1:

                st.subheader(
                    result["recommended_role"]
                )

            with col2:

                st.metric(
                    "Match Score",
                    f'{result["match_score"]}%'
                )


            st.divider()


            # -----------------------------
            # Skills
            # -----------------------------

            st.header("🛠️ Skills")

            col1, col2 = st.columns(2)

            with col1:

                st.subheader("Technical Skills")

                if result["technical_skills"]:

                    for skill in result["technical_skills"]:

                        st.write(
                            f"✅ {skill}"
                        )

                else:

                    st.write(
                        "No technical skills identified."
                    )


            with col2:

                st.subheader("Soft Skills")

                if result["soft_skills"]:

                    for skill in result["soft_skills"]:

                        st.write(
                            f"⭐ {skill}"
                        )

                else:

                    st.write(
                        "No soft skills identified."
                    )


            st.divider()


            # -----------------------------
            # Education
            # -----------------------------

            st.header("🎓 Education")

            if result["education"]:

                for education in result["education"]:

                    st.write(
                        f"• {education}"
                    )

            else:

                st.write(
                    "No education information identified."
                )


            # -----------------------------
            # Experience
            # -----------------------------

            st.header("💼 Experience")

            if result["experience"]:

                for experience in result["experience"]:

                    st.write(
                        f"• {experience}"
                    )

            else:

                st.write(
                    "No experience information identified."
                )


            st.divider()


            # -----------------------------
            # Missing Skills
            # -----------------------------

            st.header("📚 Skills to Improve")

            if result["missing_skills"]:

                st.write(
                    "These skills could improve your suitability "
                    "for the recommended role:"
                )

                for skill in result["missing_skills"]:

                    st.warning(
                        f"⚠️ {skill}"
                    )

            else:

                st.success(
                    "🎉 No major skill gaps identified."
                )


            # -----------------------------
            # Why This Role?
            # -----------------------------

            st.header("💡 Why This Role?")

            st.write(
                result["reason"]
            )


            # -----------------------------
            # Raw Resume
            # -----------------------------

            with st.expander(
                "📃 View Extracted Resume Text"
            ):

                st.text_area(
                    "Resume Text",
                    resume_text,
                    height=400
                )


        except Exception as e:

            st.error(
                "Something went wrong while analyzing "
                "the resume."
            )

            st.exception(e)


# =====================================================
# JOB DESCRIPTION MATCHER
# =====================================================

st.divider()

st.header("💼 Job Description Matcher")

st.write(
    "Paste a job description below to see how well your "
    "resume matches the position."
)


job_description = st.text_area(
    "Job Description",
    height=250,
    placeholder=(
        "Paste the job description here...\n\n"
        "Example: We are looking for a Python Developer "
        "with experience in Python, Django, SQL, REST APIs..."
    )
)


if st.button("🎯 Match Resume With Job"):

    # Check whether resume was uploaded

    if not uploaded_file:

        st.warning(
            "Please upload a resume first."
        )

    elif not resume_text:

        st.warning(
            "Please click 'Analyze Resume' first."
        )

    elif not job_description.strip():

        st.warning(
            "Please enter a job description first."
        )

    else:

        try:

            with st.spinner(
                "Comparing your resume with the job description..."
            ):

                job_result = match_job_description(
                    resume_text,
                    job_description
                )


            st.success(
                "✅ Job matching analysis completed!"
            )


            # -----------------------------
            # Match Score
            # -----------------------------

            st.subheader("📊 Job Match Score")

            st.metric(
                "Overall Match",
                f'{job_result["match_score"]}%'
            )


            # -----------------------------
            # Matched Skills
            # -----------------------------

            st.subheader("✅ Matched Skills")

            if job_result["matched_skills"]:

                for skill in job_result["matched_skills"]:

                    st.write(
                        f"✅ {skill}"
                    )

            else:

                st.write(
                    "No major matching skills identified."
                )


            # -----------------------------
            # Missing Skills
            # -----------------------------

            st.subheader("⚠️ Missing Skills")

            if job_result["missing_skills"]:

                for skill in job_result["missing_skills"]:

                    st.warning(
                        skill
                    )

            else:

                st.success(
                    "No major missing skills identified."
                )


            # -----------------------------
            # Strengths
            # -----------------------------

            st.subheader("💪 Your Strengths")

            for strength in job_result["strengths"]:

                st.write(
                    f"• {strength}"
                )


            # -----------------------------
            # Recommendation
            # -----------------------------

            st.subheader("💡 Recommendation")

            st.info(
                job_result["recommendation"]
            )


            # -----------------------------
            # Improvement Suggestions
            # -----------------------------

            st.subheader(
                "📚 Improvement Suggestions"
            )

            for suggestion in job_result[
                "improvement_suggestions"
            ]:

                st.write(
                    f"• {suggestion}"
                )


        except Exception as e:

            st.error(
                "Unable to analyze the job description."
            )

            st.exception(e)
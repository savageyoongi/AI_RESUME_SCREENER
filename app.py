import streamlit as st

from resume_parser import extract_text
from ai_analyzer import analyze_resume


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
# Upload
# -----------------------------

uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf", "docx"],
    help="Supported formats: PDF and DOCX"
)


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

                    st.write("No technical skills identified.")


            with col2:

                st.subheader("Soft Skills")

                if result["soft_skills"]:

                    for skill in result["soft_skills"]:

                        st.write(
                            f"⭐ {skill}"
                        )

                else:

                    st.write("No soft skills identified.")


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
            # Why this role?
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
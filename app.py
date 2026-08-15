import streamlit as st
from resume_parser import extract_text


st.set_page_config(
    page_title="AI Resume Screening System",
    page_icon="📄",
    layout="wide"
)


st.title("📄 AI Resume Screening System")

st.write(
    "Upload your resume and our AI system will analyze your "
    "skills, experience, and recommend suitable job roles."
)


st.divider()


uploaded_file = st.file_uploader(
    "Upload your Resume",
    type=["pdf", "docx"],
    help="Upload your resume in PDF or DOCX format."
)


if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("🔍 Extract Resume Text"):

        try:

            resume_text = extract_text(uploaded_file)

            if not resume_text.strip():
                st.error(
                    "Could not extract text from this resume. "
                    "Please make sure the file contains selectable text."
                )

            else:

                st.success("Resume text extracted successfully!")

                st.subheader("📃 Extracted Resume Text")

                st.text_area(
                    "Resume Content",
                    resume_text,
                    height=400
                )

        except Exception as e:

            st.error(
                f"Something went wrong while processing the resume: {str(e)}"
            )
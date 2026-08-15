# AI Resume Screener

An AI-based resume screening and job recommendation system built using Python, Streamlit, and Google Gemini API.

## Project Overview

The application analyzes a candidate's resume and provides information about their skills, education, experience, suitable job role, and missing skills.

It can also compare a resume against a specific job description and generate a match score.

## Features

- Upload resumes in PDF and DOCX format
- Extract text from resumes
- Identify technical skills
- Identify soft skills
- Generate a candidate profile summary
- Recommend a suitable job role
- Identify missing skills
- Compare resume with a job description
- Generate job match score
- Show matched and missing skills
- Provide improvement suggestions

## Technologies Used

- Python
- Streamlit
- Google Gemini API
- PyPDF2 / pdfplumber
- python-docx
- python-dotenv

## Project Structure

```text
AI_RESUME_SCREENER/
│
├── app.py
├── ai_analyzer.py
├── resume_parser.py
├── requirements.txt
├── .gitignore
├── .env
└── README.md
import os
import json

from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is not set in the .env file."
    )

client = genai.Client(api_key=api_key)


def analyze_resume(resume_text):

    prompt = f"""
You are an expert AI resume screening assistant.

Analyze the following resume and return ONLY valid JSON.

The JSON must contain exactly these fields:

{{
    "profile_summary": "A concise professional summary",
    "technical_skills": ["skill1", "skill2"],
    "soft_skills": ["skill1", "skill2"],
    "education": ["education details"],
    "experience": ["experience details"],
    "recommended_role": "Most suitable job role",
    "match_score": 85,
    "missing_skills": ["skill1", "skill2"],
    "reason": "Why this job role is suitable"
}}

Rules:

1. Identify technical skills explicitly mentioned or strongly demonstrated.
2. Identify soft skills from the resume.
3. Summarize education.
4. Summarize work, internship, and project experience.
5. Recommend the SINGLE most suitable job role.
6. Give a match score from 0 to 100.
7. Identify important skills missing for the recommended role.
8. Base your analysis only on the information available in the resume.
9. Do not invent qualifications, experience, or skills.

Resume:

{resume_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    response_text = response.text.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace(
            "```json", ""
        )
        response_text = response_text.replace(
            "```", ""
        )
        response_text = response_text.strip()

    return json.loads(response_text)


def match_job_description(resume_text, job_description):

    prompt = f"""
You are an expert AI recruitment assistant.

Compare the candidate's resume with the provided job description.

Return ONLY valid JSON with exactly these fields:

{{
    "match_score": 85,
    "matched_skills": ["Python", "SQL", "Git"],
    "missing_skills": ["Docker", "AWS"],
    "strengths": [
        "Strong Python experience",
        "Relevant project experience"
    ],
    "recommendation": "Strong match for this position",
    "improvement_suggestions": [
        "Learn Docker",
        "Gain experience with AWS"
    ]
}}

Rules:

1. Match the candidate's actual skills against the job requirements.
2. Do not invent skills that are not present in the resume.
3. match_score must be between 0 and 100.
4. Identify skills present in both the resume and job description.
5. Identify important skills required by the job but missing from the resume.
6. Provide practical improvement suggestions.
7. Keep the recommendation concise.

CANDIDATE RESUME:

{resume_text}

JOB DESCRIPTION:

{job_description}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    response_text = response.text.strip()

    if response_text.startswith("```"):
        response_text = response_text.replace(
            "```json", ""
        )
        response_text = response_text.replace(
            "```", ""
        )
        response_text = response_text.strip()

    return json.loads(response_text)
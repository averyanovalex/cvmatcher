"""Streamlit application for matching CVs with job descriptions."""

import os
from tempfile import NamedTemporaryFile

import streamlit as st

from match import (compare_cv_with_job, extract_cv_features,
                   extract_job_requirements, get_cv_text_from_pdf,
                   total_match_score)

os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]


def main():
    """Run the main Streamlit application."""
    st.title("CV Matcher")

    st.header("Job Description")
    job_description = st.text_area(
        "Paste the job description",
        height=200,
        placeholder="For example: Looking for a Python developer with 3+ years of experience...",
    )

    st.header("CV Upload")
    uploaded_file = st.file_uploader("Upload your CV in PDF format", type=["pdf"])

    if uploaded_file is not None:
        # Save uploaded file to temp file
        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            temp_path = tmp_file.name

        # Extract text from PDF
        cv_text = get_cv_text_from_pdf(temp_path)
        os.unlink(temp_path)  # Remove temp file

        with st.expander("View Uploaded CV"):
            st.text_area("CV Content", cv_text, height=300)

    if st.button("🎯 Compare", type="primary"):
        if not job_description:
            st.error("Please enter the job description")
            return
        if not uploaded_file:
            st.error("Please upload your CV")
            return

        with st.spinner("Analyzing match..."):
            # Extract requirements from job description
            job_reqs = extract_job_requirements(job_description)

            # Extract features from CV
            cv_feats = extract_cv_features(cv_text)

            # Compare CV with requirements
            comparison = compare_cv_with_job(cv_feats, job_reqs)

            # Calculate total score
            total_score = total_match_score(comparison)

            st.success("Analysis complete!")

            # Display results
            st.header("Comparison Results")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Overall Match", f"{total_score}%")

            st.subheader("Detailed Analysis")
            with st.expander("View Details", expanded=True):
                # Position Match
                st.write("🔹 Position Match")
                st.progress(
                    comparison.position_match / 10,
                    text=f"Position Match ({comparison.position_match * 10}%)",
                )

                # Technical Skills
                st.write("🔹 Technical Skills")
                st.progress(
                    comparison.technical_skills_match / 10,
                    text=f"Technical Skills ({comparison.technical_skills_match * 10}%)",
                )

                # Experience
                st.write("🔹 Experience")
                st.progress(
                    comparison.experience_match / 10,
                    text=f"Experience Match ({comparison.experience_match * 10}%)",
                )
                experience_years_icon = (
                    "✅" if comparison.experience_years_match else "❌"
                )
                st.write(f"{experience_years_icon} Required years of experience")

                # Achievements
                st.write("🔹 Achievements")
                st.progress(
                    comparison.achievements_match / 10,
                    text=f"Achievements ({comparison.achievements_match * 10}%)",
                )

                # Education
                st.write("🔹 Education")
                st.progress(
                    comparison.education_match / 10,
                    text=f"Education ({comparison.education_match * 10}%)",
                )

                # Language Skills
                st.write("🔹 Language Skills")
                st.progress(
                    comparison.language_skills_match / 10,
                    text=f"Language Skills ({comparison.language_skills_match * 10}%)",
                )


if __name__ == "__main__":
    st.set_page_config(page_title="CV Matcher", page_icon="📄", layout="wide")
    main()

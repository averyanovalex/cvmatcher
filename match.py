from PyPDF2 import PdfReader
from pydantic import BaseModel, Field
from openai import OpenAI


OPENAI_MODEL = "gpt-4o"

client = OpenAI()


class JobRequirements(BaseModel):
    """Model representing job requirements extracted from job description."""
    position: str = Field(description="The job position (e.g. 'Backend Developer')")
    position_level: str = Field(
        description="The level of the job position (e.g. 'Senior, Middle, Junior, Unknown')"
    )
    technical_skills: list[str] = Field(
        description="The technical skills required for the job, mark 'or' for alternatives"
    )
    requirements: list[str] = Field(
        description="All key requirements for the job as a list of strings"
    )
    experience_years: int = Field(
        description="The number of years of experience required for the job (e.g. 3)"
    )
    education: str = Field(
        description="The education required for the job: level and field of study"
    )
    language_skills: str = Field(
        description="The language skills and level of proficiency"
    )


class CVFeatures(BaseModel):
    """Model representing features extracted from a CV."""
    name: str = Field(description="The full name of the CV")
    email: str = Field(description="The email of the CV")
    location: str = Field(description="The location of the CV")
    position: str = Field(description="The job position from the CV")
    position_level: str = Field(
        description="The level of the job position from the CV"
    )
    experience_years: int = Field(
        description="The number of years of experience from the CV"
    )
    technical_skills: list[str] = Field(
        description="The technical skills from the CV"
    )
    experience: list[str] = Field(
        description="The experience from the CV"
    )
    achievements: list[str] = Field(
        description="The particular achievements from the CV"
    )
    education: list[str] = Field(
        description="The education from the CV"
    )
    language_skills: list[str] = Field(
        description="The language skills and level of proficiency from the CV"
    )


class ComparisonResult(BaseModel):
    """Model representing comparison scores between CV and job requirements."""
    position_match: int = Field(
        description="The score for the position name match (0-10)"
    )
    technical_skills_match: int = Field(
        description="The score for the technical skills match (0-10)"
    )
    experience_years_match: bool = Field(
        description="True if experience years are equal or greater than required"
    )
    experience_match: int = Field(
        description="The score for the experience match (0-10)"
    )
    achievements_match: int = Field(
        description="The score for the achievements match (0-10)"
    )
    education_match: int = Field(
        description="The score for the education match (0-10)"
    )
    language_skills_match: int = Field(
        description="The score for the language skills match (0-10)"
    )


def get_cv_text_from_pdf(file_path: str):
    """Extract and return text content from a PDF CV."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


def extract_job_requirements(job_description: str):
    """Extract structured job requirements from job description text using AI."""
    system_prompt = (
        "You are an assistant with the task of extracting precise information "
        "from job description. You will be prompted with the contents of a job "
        "description. Your task is to extract requirements for the job position, "
        "position level, technical skills, experience years, education, language "
        "skills and other requirements from this job description.\n\n"
        "Do your best to include as many requirements as possible!"
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": job_description},
    ]
    
    response = client.beta.chat.completions.parse(
        model=OPENAI_MODEL,
        messages=messages,
        response_format=JobRequirements
    )
    
    return response.choices[0].message.parsed


def extract_cv_features(cv_text: str):
    """Extract structured features from CV text using AI."""
    system_prompt = (
        "You are an assistant with the task of extracting precise information "
        "from CV. You will be prompted with the contents of a CV. Your task is "
        "to extract features for the CV: name, email, location, position, "
        "position level, experience years, technical skills, experience, "
        "achievements, education, language skills.\n\n"
        "Do your best to include as many requirements as possible!"
    )
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": cv_text},
    ]
    
    response = client.beta.chat.completions.parse(
        model=OPENAI_MODEL,
        messages=messages,
        response_format=CVFeatures
    )
    
    return response.choices[0].message.parsed



def compare_cv_with_job(cv_features: CVFeatures, job_requirements: JobRequirements):
    """Compare CV features with job requirements and return matching scores."""
    system_prompt = (
        "You are an assistant with the task of comparing CV with job requirements. "
        "You will be prompted with the CV features and job requirements. Your task "
        "is to compare the CV with the job requirements and return the score for "
        "each category.\n\n"
        "The score is calculated based on the following criteria:\n"
        "1. Position match: 0-10\n"
        "2. Technical skills match: 0-10\n"
        "3. Experience years match: True/False\n"
        "4. Experience match: 0-10\n"
        "5. Achievements match: 0-10\n"
        "6. Education match: 0-10\n"
        "7. Language skills match: 0-10"
    )
    
    user_prompt = f"CV features: {cv_features}\nJob requirements: {job_requirements}"
    
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
    
    response = client.beta.chat.completions.parse(
        model=OPENAI_MODEL,
        messages=messages,
        response_format=ComparisonResult
    )
    
    return response.choices[0].message.parsed


def total_match_score(comparison: ComparisonResult) -> int:
    """Calculate total matching score as percentage based on weighted criteria."""
    weights = {
        'position_match': 4,
        'experience_years_match': 3,
        'technical_skills_match': 2,
        'experience_match': 3,
        'achievements_match': 3,
        'education_match': 1,
        'language_skills_match': 1,
    }
    
    max_score = 0
    total_score = 0

    total_score += comparison.position_match * weights['position_match']
    total_score += comparison.technical_skills_match * weights['technical_skills_match']
    total_score += int(comparison.experience_years_match) * weights['experience_years_match']
    total_score += comparison.experience_match * weights['experience_match']
    total_score += comparison.achievements_match * weights['achievements_match']
    total_score += comparison.education_match * weights['education_match']
    total_score += comparison.language_skills_match * weights['language_skills_match']

    max_score += weights['position_match'] * 10
    max_score += weights['technical_skills_match'] * 10
    max_score += weights['experience_years_match'] * 1
    max_score += weights['experience_match'] * 10
    max_score += weights['achievements_match'] * 10
    max_score += weights['education_match'] * 10
    max_score += weights['language_skills_match'] * 10

    return round(total_score / max_score * 100)


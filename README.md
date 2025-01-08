# CV Matcher (Proof-Of-Concept)

A Streamlit application that uses AI to match CVs with job descriptions. The app analyzes both the job requirements and CV content to provide a detailed matching score and analysis.

## Features

- Extract requirements from job descriptions
- Parse CV content from PDF files 
- Compare CV features with job requirements
- Calculate matching scores for different criteria:
  - Position match
  - Technical skills
  - Experience
  - Education
  - Language skills
  - And more

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/averyanovalex/cvmatcher.git
   cd cv-matcher
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Set up your OpenAI API key:
   - Create a file named `.streamlit/secrets.toml` in the project root directory.
   - Add your OpenAI API key to the file:
     ```
     [secrets]
     OPENAI_API_KEY = "your_openai_api_key"
     ```

2. Run the Streamlit application:
   ```bash
   streamlit run app.py
   ```

3. Open your web browser and go to `http://localhost:8501` to access the application.


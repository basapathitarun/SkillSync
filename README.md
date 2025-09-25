### **SkillSync: An AI-Powered Resume and Job Matcher**

SkillSync is an AI-driven tool designed to streamline the resume screening process for recruiters and help job seekers optimize their resumes for specific roles. By leveraging advanced language models, the application analyzes a candidate's resume against a job description, provides a compatibility score, and offers tailored suggestions for improvement.

---

### **Features**

* **AI-Powered Matching:** Analyzes resumes and job descriptions to provide a nuanced match score.
* **Actionable Suggestions:** Generates specific, targeted feedback to help candidates improve their resumes.
* **Multi-format Support:** Supports parsing of PDF and DOCX resume files.
* **Robust API:** Built with FastAPI, providing a simple and reliable API endpoint for analysis.

---

### **How It Works**

The application follows a simple, three-step process:

1.  **Parsing:** The user uploads a resume and provides a job description. The application uses libraries like `pypdf` and `python-docx` to extract raw text.
2.  **LLM Analysis:** The raw text from both documents is sent to a powerful Large Language Model (LLM) with a carefully crafted prompt. The LLM performs the core analysis, identifying skills, experience, and key requirements.
3.  **Structured Response:** The LLM returns a structured JSON response containing a match percentage and a list of detailed suggestions. This data is then validated and returned to the user via the API.

---

### **Getting Started**

#### **Prerequisites**

To run this project, you will need:
* Python 3.11
* An OpenAI API key

#### **Installation**

1.  **Clone the repository:**
    ```bash
    git clone [Your-Repository-URL]
    cd skillsync
    ```

2.  **Install dependencies using uv:**
    `uv` will automatically create a virtual environment in `.venv` and install all dependencies listed in your `pyproject.toml` file.
    ```bash
    uv sync
    ```

3.  **Activate the virtual environment:**
    ```bash
    source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
    ```

#### **Configuration**

1.  Create a `.env` file in the root directory.
2.  Add your OpenAI API key to the file:
    ```env
    OPENAI_API_KEY="sk-proj-YOUR_KEY_HERE"
    ```

#### **Running the Application**

1.  Start the FastAPI server using `uvicorn`:
    ```bash
    uvicorn main:app --reload
    ```
2.  The application will be accessible at `http://127.0.0.1:8000`. You can test the API endpoints by navigating to the interactive documentation at `http://127.0.0.1:8000/api/docs`.

---

### **Project Structure**

* `main.py`: The entry point for the FastAPI application.
* `src/routes.py`: Defines the API endpoints for the service.
* `src/resume_parser.py`: Handles the extraction of text from resume files.
* `src/job_description_parser.py`: Manages job description text processing.
* `src/matching.py`: Contains the core logic for communicating with the LLM and generating the analysis.
* `src/custom_types.py`: Defines the Pydantic models for structured data and API responses.

---

### **Contributing**

We welcome contributions! Please feel free to open an issue or submit a pull request.
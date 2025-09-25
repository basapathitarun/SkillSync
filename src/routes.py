# api 1: gets pdf and job desrcption from user 
from fastapi import File, UploadFile, Form
from fastapi import APIRouter
from typing import List
from src.resume_parser import ResumeParser
from src.job_description_parser import parse_job_description
from src.matching import calculate_match_score
from src.custom_types import ResumeAnalysisResponse
import os


router = APIRouter()


@router.post("/match/",response_model=ResumeAnalysisResponse)
def analyze_resume(
    resume: UploadFile = File(...),
    job_description: str = Form(...)
):
    
    # Save uploaded resume to a temporary file
    temp_resume_path = f"temp_{resume.filename}"
    with open(temp_resume_path, "wb") as buffer:
        buffer.write(resume.file.read())
    
    try:
        # STEP1: Parse the resume and job description
        parser = ResumeParser()
        parser.load_resume(temp_resume_path)
        preprocessed_resume = parser.preprocessing()

        # Step 2: Parse job description
        prased_job_description= parse_job_description(job_description)

        # Step 3: 
        return calculate_match_score(resume_data=preprocessed_resume,job_description_data=prased_job_description)

        
    except Exception as e:
        return {"error":str(e)}
        
    finally:
        # Clean up the temporary file
        os.remove(temp_resume_path)
from pydantic import BaseModel, Field
from typing import List

class MatchResult(BaseModel):
    """
    Represents the overall matching result between a resume and job description.
    """
    percentage: float = Field(
        ...,
        description="The percentage of the job description that matches the resume, based on skills, keywords, and experience."
    )

class ImprovementSuggestion(BaseModel):
    """
    Provides a specific suggestion for improvement on the resume.
    """
    original_text: str = Field(
        ...,
        description="The specific text or section from the resume that the suggestion applies to."
    )
    improvements: List[str] = Field(
        ...,
        description="A list of actionable suggestions to improve the 'original_text' for a better match with the job description."
    )

class ResumeAnalysisResponse(BaseModel):
    """
    The final response model for the resume analysis API.
    """
    match_result: MatchResult = Field(
        ...,
        description="A single object containing the overall match percentage."
    )
    suggestions: List[ImprovementSuggestion] = Field(
        ...,
        description="A list of specific suggestions to help the user improve their resume."
    )
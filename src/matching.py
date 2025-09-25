import os
from typing import Any, Type
from pydantic import BaseModel
from abc import ABC, abstractmethod
from src.custom_types import ResumeAnalysisResponse


class LLM(ABC):
    @abstractmethod
    def generate(self, prompt: Any, **kwargs) -> Any:
        """Base interface for all LLMs."""
        pass


class OpenAIWrapper(LLM):
    """
    Wrapper around the OpenAI client.
    Exposes a generate(prompt, pydantic_class=...) -> BaseModel method.
    """

    def __init__(self, model: str, api_key: str | None = None):
        """
        :param model: model name (e.g. "gpt-5-nano-2025-08-07")
        :param api_key: optional override for OPENAI_API_KEY
        """
        # import here so module can be imported even if openai isn't installed in some contexts
        from openai import OpenAI

        self.model = model
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))

    def generate(self, prompt: list, pydantic_class: Type[BaseModel], **kwargs) -> BaseModel:
        """
        :param prompt: list of message dicts (system/user roles)
        :param pydantic_class: a Pydantic model class to parse structured output into
        :returns: an instance of pydantic_class
        """
        try:
            # Use the parse helper to get structured output (SDK method may vary by SDK version)
            response = self.client.responses.parse(
                model=self.model,
                input=prompt,
                text_format=pydantic_class
            )
        except Exception as exc:
            # bubble up as RuntimeError for clearer upstream handling
            raise RuntimeError(f"OpenAI generation failed: {exc}") from exc

        return  response.output_parsed

def calculate_match_score(resume_data: str, job_description_data: str) -> ResumeAnalysisResponse:
    """
    Build the prompt and request a structured ResumeAnalysisResponse from the LLM.
    """
    prompt = [
        {
            "role": "system",
            "content": (
                "You are a recruiter analyzing resumes against job descriptions. "
                "Provide a match score (0-100), strengths, weaknesses, and tailored suggestions "
                "to increase the candidate's chance of getting a call."
            ),
        },
        {
            "role": "user",
            "content": f"Resume:\n{resume_data}\n\nJob Description:\n{job_description_data}",
        },
    ]

    llm_obj = OpenAIWrapper(model="gpt-4o-2024-08-06")
    response: ResumeAnalysisResponse = llm_obj.generate(prompt=prompt, pydantic_class=ResumeAnalysisResponse)
    print("response ", response)
    return response




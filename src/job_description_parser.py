
# The parse_job_description function is empty. Your main task here is to write the logic that takes
# a string of job description text and extracts a structured set of data from it. This should include
# key entities like required skills, years of experience, and responsibilities. You can use a simple 
# approach with keyword matching, or a more advanced method using an LLM to identify and categorize 
# this information.


# get the job description from user and clean it the text
def parse_job_description(job_description: str) -> dict:
    """
    Parses the job description text to extract structured data.
    """
    if not job_description:
        raise ValueError("Job description is empty.")
    return job_description
    
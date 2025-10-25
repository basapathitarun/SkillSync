# Your parse_resume function currently loads the document data, which is a great first step. Now, 
# you need to add the logic to process this raw text and extract structured information from the
# resume. This involves pulling out the candidate's skills, work experience, education, and 
# other relevant details. This structured data will be used for the matching and suggestion tasks.
import os
from typing import Callable, Any

class SimpleResumeReader:
    """A class to read text from different resume file types."""
    
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.file_type = self._check_file_type()
        self.reader_func = self._get_reader_func()

    def _get_reader_func(self) -> Callable[..., str]:
        """Returns the appropriate reader function based on file type."""
        if self.file_type == '.pdf':
            return self._pdf_reader
        elif self.file_type in ['.docx', '.doc']:
            return self._docx_reader
        else:
            raise ValueError(f"Unsupported file type: {self.file_type}")

    def _check_file_type(self) -> str:
        """Determines the file extension and returns it in lowercase."""
        _, file_extension = os.path.splitext(self.file_path)
        return file_extension.lower()

    def _pdf_reader(self) -> str:
        """Reads text from a PDF file."""
    #    """
    #     Issue: it is not reading the links in the pdf file
    #     """
        from pypdf import PdfReader
        reader = PdfReader(self.file_path)
        all_text = []

        for page in reader.pages:
            # Extract visible text

            text = page.extract_text() or ""
            all_text.append(text)

            # Extract links from annotations (if present)
            if "/Annots" in page:
                for annot in page['/Annots']:
                    obj = annot.get_object()
                    print("obj:", obj)
                    if "/A" in obj and "/URI" in obj["/A"]:
                        link = obj["/A"]["/URI"]
                        all_text.append(f"[Link]:{link}")
                
        return "\n".join(all_text)

    def _docx_reader(self) -> str:
        """Reads text from a DOCX file."""
        from docx import Document
        doc = Document(self.file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    def read(self) -> str:
        """Public method to read the file and return the text content."""
        return self.reader_func()

class ResumeParser:
    """A class to parse resume documents and extract structured data."""

    def __init__(self):
        self.file_path = None
        self.raw_text = None

    def load_resume(self, file_path: str) -> str:
        """
        Reads the resume file and stores its content as raw text.
        
        Args:
            file_path (str): The path to the resume file.
        
        Returns:
            str: The raw text content of the resume.
        """
        self.file_path = file_path
        reader = SimpleResumeReader(file_path)
        self.raw_text = reader.read()
        return self.raw_text
    
    def preprocessing(self)-> str:
        """
        Clean the text: remove extra spaces, bullet symbols, headers/footers.
        Split into sections if possible (look for headings like Education, Experience, Skills).
        """
        if not self.raw_text:
            raise ValueError("No resume loaded. Call load_resume() first.")
        
        # Basic cleaning: remove extra spaces and bullet symbols
        cleaned_text = self.raw_text.replace('\n', ' ').replace('•', '').strip()
        self.raw_text = ' '.join(cleaned_text.split())

        return self.raw_text
    
    

        
       
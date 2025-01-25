from pydantic import BaseModel, HttpUrl

class CoverLetterRequest(BaseModel):
    """Request model for cover letter generation."""
    job_url: HttpUrl

class CoverLetterResponse(BaseModel):
    """Response model for cover letter generation."""
    company_name: str
    job_title: str
    markdown_content: str
    pdf_path: str

class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: str | None = None

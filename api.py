from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from pathlib import Path

from models import CoverLetterRequest, CoverLetterResponse, ErrorResponse
from generate_cover_letter import generate_cover_letter
from get_jobs_information import get_job_information

# Define fixed template paths
TEMPLATE_PATH = "template/CL_base_template.txt"
EXAMPLE_CONTENT_PATH = "template/CL_content_exemple.txt"
CV_PATH = "template/CV.txt"

app = FastAPI(
    title="Cover Letter Generator API",
    description="API for generating customized cover letters using Mistral AI",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "Cover Letter Generator API",
        "version": "1.0.0",
        "description": "Generate customized cover letters using Mistral AI"
    }

@app.post("/generate", response_model=CoverLetterResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def generate_cover_letter_endpoint(request: CoverLetterRequest):
    """
    Generate a cover letter based on the provided job URL.
    
    Args:
        request (CoverLetterRequest): The request containing job URL
        
    Returns:
        CoverLetterResponse: The generated cover letter content and metadata
        
    Raises:
        HTTPException: If there's an error during the generation process
    """
    try:
        # Validate template files exist
        for path in [TEMPLATE_PATH, EXAMPLE_CONTENT_PATH, CV_PATH]:
            if not os.path.exists(path):
                raise HTTPException(
                    status_code=500,
                    detail=f"Required template file not found: {path}"
                )

        # Get job information first
        company_name, job_title, _ = get_job_information(str(request.job_url))

        # Generate the cover letter
        generated_letter = generate_cover_letter(
            str(request.job_url),
            TEMPLATE_PATH,
            EXAMPLE_CONTENT_PATH,
            CV_PATH
        )

        # Construct the PDF path
        pdf_path = f"result/{company_name}_cover_letter.pdf"

        return CoverLetterResponse(
            company_name=company_name,
            job_title=job_title,
            markdown_content=generated_letter,
            pdf_path=pdf_path
        )

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/download/{company_name}")
async def download_pdf(company_name: str):
    """
    Download the generated PDF cover letter for a specific company.
    
    Args:
        company_name (str): Name of the company to get the cover letter for
        
    Returns:
        FileResponse: The PDF file
        
    Raises:
        HTTPException: If the file is not found
    """
    pdf_path = f"result/{company_name}_cover_letter.pdf"
    
    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=404,
            detail=f"PDF not found for company: {company_name}"
        )
    
    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"{company_name}_cover_letter.pdf"
    )

if __name__ == "__main__":
    import uvicorn
    # Create result directory if it doesn't exist
    Path("result").mkdir(exist_ok=True)
    # Run the API server
    uvicorn.run(app, host="0.0.0.0", port=8000)

# AI-Powered Cover Letter Generator

Automated cover letter generator using Mistral AI to create personalized cover letters from LinkedIn job postings.

## Features

- Scrapes job information from LinkedIn job postings
- Generates customized cover letters using Mistral AI
- Converts generated cover letters to professionally formatted PDFs
- REST API for easy integration

## Prerequisites

- Python 3.8+
- Mistral AI API key
- Required packages: `pip install -r requirements.txt`
- Set environment variable: `export MISTRAL_API_KEY="your-api-key-here"`

## Project Structure

```
├── api.py                    # FastAPI application
├── models.py                 # API data models
├── generate_cover_letter.py  # Cover letter generation
├── get_jobs_information.py   # LinkedIn scraper
├── create_pdf.py            # PDF utilities
├── template/                # Templates and CV
└── result/                  # Generated files
```

## Usage

### Using the API

1. Place your CV and templates:
   - CV: `template/CV.txt`
   - Cover letter template: `template/CL_base_template.txt`
   - Example content: `template/CL_content_exemple.txt`

2. Start the server:
```bash
python api.py
```

3. Generate a cover letter:
```bash
curl -X POST "http://localhost:8000/generate" \
     -H "Content-Type: application/json" \
     -d '{"job_url": "https://www.linkedin.com/jobs/view/..."}'
```

4. Download the PDF:
```bash
curl -O "http://localhost:8000/download/CompanyName"
```

Interactive API documentation available at: `http://localhost:8000/docs`

### Using the Python Script

```python
from generate_cover_letter import generate_cover_letter

cover_letter = generate_cover_letter(
    "linkedin-job-url",
    "template/CL_base_template.txt",
    "template/CL_content_exemple.txt",
    "template/CV.txt"
)
```

### Batch Testing

The project includes a test script to process multiple job URLs:

1. Add your LinkedIn job URLs to `linkedin_jobs_example.txt`:
```text
https://www.linkedin.com/jobs/view/...
https://www.linkedin.com/jobs/view/...
```

2. Run the test script:
```bash
python test_examples.py
```

This will:
- Process each URL in the file
- Generate cover letters for each job
- Create both markdown and PDF versions
- Save results in the `result` directory

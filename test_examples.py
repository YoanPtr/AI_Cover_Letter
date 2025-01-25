import requests
import time
import sys

def test_job_url(job_url):
    """Test generating a cover letter for a specific job URL."""
    print(f"\nTesting job URL: {job_url}")
    
    try:
        # Generate the cover letter
        response = requests.post(
            "http://localhost:8000/generate",
            json={"job_url": job_url}
        )
        
        if response.status_code == 200:
            data = response.json()
            print(f"Success! Generated cover letter for {data['company_name']} - {data['job_title']}")
            
            # Download the PDF
            pdf_response = requests.get(f"http://localhost:8000/download/{data['company_name']}")
            if pdf_response.status_code == 200:
                print(f"Successfully downloaded PDF: {data['pdf_path']}")
            else:
                print(f"Failed to download PDF: {pdf_response.status_code} - {pdf_response.text}")
        else:
            print(f"Failed to generate cover letter: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"Error: {str(e)}")

def main():
    # Read job URLs from the example file
    with open("linkedin_jobs_example.txt", "r") as f:
        job_urls = [line.strip() for line in f if line.strip()]
    
    # Wait for the API server to start
    print("Waiting for API server to start...")
    time.sleep(2)
    
    # Test each job URL
    for job_url in job_urls:
        test_job_url(job_url)
        time.sleep(1)  # Small delay between requests

if __name__ == "__main__":
    main()

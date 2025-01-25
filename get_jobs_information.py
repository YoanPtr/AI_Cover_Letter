import requests
from bs4 import BeautifulSoup
from typing import Tuple


def get_job_information(url: str) -> Tuple[str, str, str]:
    """
    Scrape job information from a LinkedIn job posting URL.
    
    Args:
        url (str): The LinkedIn job posting URL
        
    Returns:
        Tuple[str, str, str]: A tuple containing (company_name, job_title, job_description)
        
    Raises:
        ValueError: If the URL is invalid or empty
        requests.RequestException: If there's an error fetching the webpage
        Exception: For other unexpected errors
    """
    if not url or not url.startswith("https://www.linkedin.com/jobs/"):
        raise ValueError("Invalid LinkedIn job URL provided")

    try:
        # Headers to simulate a browser request (important for LinkedIn scraping)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        # Send a GET request to fetch the content of the page
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an exception for bad status codes

        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract the company name
        company_name_tag = soup.find("a", class_="topcard__org-name-link")
        company_name = company_name_tag.get_text(strip=True) if company_name_tag else "Company name not found"

        # Extract the job title
        job_title_tag = soup.find("h1", class_="top-card-layout__title")
        job_title = job_title_tag.get_text(strip=True) if job_title_tag else "Job title not found"

        # Extract the job description
        job_description_div = soup.find("div", class_="show-more-less-html__markup")
        job_description = job_description_div.get_text(separator="\n", strip=True) if job_description_div else "Job description not found"

        if all(x == "not found" for x in [company_name, job_title, job_description]):
            raise Exception("Failed to extract job information from the webpage")

        return company_name, job_title, job_description

    except requests.RequestException as e:
        print(f"Error fetching job information: {str(e)}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        # URL of the LinkedIn job page
        url = "https://www.linkedin.com/jobs/view/4130715328/?alternateChannel=search&refId=NotAvailable&trackingId=fJwU6OLvQzmQPcYMLh%2BGrQ%3D%3D"

        company_name, job_title, job_description = get_job_information(url)
        
        print(f"Company Name: {company_name}")
        print(f"Job Title: {job_title}")
        print(f"Job Description: {job_description}")
    except Exception as e:
        print(f"Failed to get job information: {str(e)}")
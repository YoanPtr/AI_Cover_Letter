import os
from mistralai import Mistral
from get_jobs_information import get_job_information
from create_pdf import md_to_pdf

def generate_cover_letter(job_url, motivation_letter_template_path, example_cover_letter_content_path, cv_path):
    """
    Generate a customized cover letter using Mistral AI based on job information and templates.
    
    Args:
        job_url (str): URL of the job posting (LinkedIn)
        motivation_letter_template_path (str): Path to the cover letter template file
        example_cover_letter_content_path (str): Path to the example cover letter content
        cv_path (str): Path to the CV file
    
    Returns:
        str: The generated cover letter content
        
    Raises:
        FileNotFoundError: If any of the required files are not found
        ValueError: If the API key is not set or if the API call fails
        Exception: For other unexpected errors
    """
    try:
        # Step 1: Retrieve job information
        company_name, job_title, job_description = get_job_information(job_url)

        # Step 2: Load the motivation letter template
        with open(motivation_letter_template_path, 'r', encoding='utf-8') as file:
            motivation_letter_template = file.read()

        with open(example_cover_letter_content_path, 'r', encoding='utf-8') as file:
            example_cover_letter_content = file.read()

        # Step 3: Load the CV
        with open(cv_path, 'r', encoding='utf-8') as file:
            cv_text = file.read()

        # Step 4: Create a prompt for the Mistral API
        prompt = f"""
        You are a professional expert in writing cover letters, and your task is to help a student write theirs for an internship position. You have a template for the cover letter, an example of content, and the CV of the student. Your task is to adapt the content of the cover letter according to the template, using the student's CV and the example content as references. 
        You must only provide the content part from "Dear Hiring Manager" to the Name

        A template of the cover letter is already available:

        [BEGINNING OF THE TEMPLATE]
        {motivation_letter_template}
        [END OF THE TEMPLATE]

        And an example of content is available:

        [BEGINNING OF THE CONTENT]
        {example_cover_letter_content}
        [END OF THE CONTENT]
        
        And here is their CV with the relevant skills:

        {cv_text}

        Below are the details of the job they are applying for:

        - Job Title: {job_title}
        - Company: {company_name}
        - Job Description: {job_description}

        Please use the above information to customize the template and provide a markdown cover letter, adapting the student's skills to the job requirements.

        The cover letter should:

        1. Mention the job title and the company.
        2. Explain why the candidate is interested in the position, based on key points from the job description.
        3. Include details about the relevant skills the candidate can bring (based on the skills mentioned in the job description).
        4. Be professional, concise, and engaging.
        5. It is mandatory to use the template I provided.
        6. Do not invent content to fill the template, the candidate's CV and the example content must be used to write the cover letter.
        7. Generate only the content of the cover letter that will be replace in the template.
        8. Try to enlighten the capabilities of the candidates by using their CV for the job.
        9. The cover letter should be written in a professional and engaging way, using the candidate's skills to explain their interest in the job.
        """

        # Step 5: Call the Mistral API
        api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("MISTRAL_API_KEY environment variable is not set")

        model = "mistral-large-latest"
        client = Mistral(api_key=api_key)

        print("Calling the Mistral API...")
        response = client.chat.complete(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ]
        )

        # Step 6: Extract the generated cover letter
        generated_content = response.choices[0].message.content.replace('```', '').replace('markdown', '').replace("---", "")
        
        generated_letter = motivation_letter_template.replace("[CONTENT]", generated_content)

        # Create result directory if it doesn't exist
        os.makedirs("result", exist_ok=True)
        
        # Step 7: Save the generated letter to a file
        output_path = f"result/{company_name}_cover_letter.md"
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(generated_letter)

        print("Cover letter generated successfully!")
        
        # Step 8: Convert the generated letter to a PDF
        md_to_pdf(output_path)
        
        print("Cover letter PDF generated successfully!")
        return generated_letter

    except FileNotFoundError as e:
        print(f"Error: Required file not found - {str(e)}")
        raise
    except ValueError as e:
        print(f"Error: Invalid value or configuration - {str(e)}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        job_url = "https://www.linkedin.com/jobs/view/4072495275/?alternateChannel=search&refId=SFlJxdIQT44vgQJLgRSr%2Fg%3D%3D&trackingId=gkvwVQ5h%2B0%2BgzjxWNAlMxA%3D%3D"
        motivation_letter_template_path = "template/CL_base_template.txt"
        example_cover_letter_content_path = "template/CL_content_exemple.txt"
        cv_path = "template/CV.txt"
        generate_cover_letter(job_url, motivation_letter_template_path, example_cover_letter_content_path, cv_path)
    except Exception as e:
        print(f"Failed to generate cover letter: {str(e)}")

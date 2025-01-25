import markdown
from weasyprint import HTML
import os

def read_markdown_file(file_path: str) -> str:
    """
    Read content from a markdown file.
    
    Args:
        file_path (str): Path to the markdown file
        
    Returns:
        str: Content of the markdown file
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        Exception: For other unexpected errors
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File not found at path: {file_path}")
        raise
    except Exception as e:
        print(f"Error reading markdown file: {str(e)}")
        raise

def markdown_to_html(markdown_text: str) -> str:
    """
    Convert markdown text to HTML.
    
    Args:
        markdown_text (str): Text in markdown format
        
    Returns:
        str: HTML content
        
    Raises:
        Exception: If markdown conversion fails
    """
    try:
        return markdown.markdown(markdown_text)
    except Exception as e:
        print(f"Error converting markdown to HTML: {str(e)}")
        raise

def generate_pdf_from_html(html_content: str, output_pdf: str) -> None:
    """
    Generate a PDF file from HTML content with custom CSS styling.
    
    Args:
        html_content (str): HTML content to convert to PDF
        output_pdf (str): Path where to save the PDF file
        
    Raises:
        Exception: If PDF generation fails
    """
    try:
        # CSS for customizing the PDF rendering
        custom_css = """
        @import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&display=swap');
        
        body {
            font-family: 'Open Sans', sans-serif;
            margin: 5mm; /* Reduced margins */
            line-height: 1.6;
            font-size: 8pt; /* Font size */
        }

        h1, h2, h3, h4, h5, h6 {
            margin-bottom: 10px;
        }

        p {
            margin-bottom: 15px;
        }

        ul {
            margin-bottom: 15px;
        }
        """

        # Apply CSS and generate PDF
        html_content_with_css = f'<style>{custom_css}</style>' + html_content
        HTML(string=html_content_with_css).write_pdf(output_pdf)
    except Exception as e:
        print(f"Error generating PDF: {str(e)}")
        raise

def md_to_pdf(input_file: str) -> None:
    """
    Convert a markdown file to PDF with custom styling.
    
    Args:
        input_file (str): Path to the input markdown file
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
        Exception: For other unexpected errors
    """
    try:
        # Create the output directory if it doesn't exist
        output_dir = os.path.dirname(input_file)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            
        # Read and convert the markdown file
        markdown_text = read_markdown_file(input_file)
        html_content = markdown_to_html(markdown_text)
        
        # Generate the PDF with reduced margins and Open Sans font
        output_pdf = input_file.replace(".md", ".pdf")
        generate_pdf_from_html(html_content, output_pdf)
        
        print(f"PDF file generated successfully: {output_pdf}")
    except Exception as e:
        print(f"Failed to convert markdown to PDF: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        input_file = "example.md"  # Replace with your markdown file
        md_to_pdf(input_file)
    except Exception as e:
        print(f"Error in main: {str(e)}")

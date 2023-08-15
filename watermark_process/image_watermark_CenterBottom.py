import fitz
import requests
from PIL import Image
from io import BytesIO

def CenterBottom(pdf_url, output_file_name, image_path):
    # URL of the PDF file
    pdf_url = str(pdf_url)

    # Path to the PNG image
    image_path = str(image_path)

    # Download the PDF file
    response = requests.get(pdf_url)
    pdf_bytes = response.content

    # Read the PDF file
    pdf_reader = fitz.open(stream=pdf_bytes, filetype="pdf")

    # Load the image
    image = Image.open(image_path)
    image_stream = BytesIO()
    image.save(image_stream, format="png")
    image_bytes = image_stream.getvalue()

    # Get the image dimensions
    original_width, original_height = image.size

    # Iterate through the pages and add the watermark
    for page in pdf_reader:
        # Calculate the new width as 20% of the page width
        new_width = page.rect.width * 0.40
        scale_factor = new_width / original_width
        new_height = original_height * scale_factor

        # Calculate the position
        x = (page.rect.width - new_width) / 2
        y = page.rect.height - new_height  # Position at the bottom

        # Define the image rectangle
        image_rect = fitz.Rect(x, y, x + new_width, y + new_height)

        # Add the image without resizing
        page.insert_image(image_rect, stream=image_bytes)

    # Write the output PDF
    output_path = output_file_name
    pdf_reader.save(output_path)


CenterBottom(pdf_url="https://cdn.salla.sa/djRrP/rX7KeJV1fXG6j53RDNhZ7If4AeLM2lmtA4FPP4Fc.pdf", output_file_name="create_downloading_PDF_link/STAMPED.pdf", image_path="design_PNG_text/empty.png")
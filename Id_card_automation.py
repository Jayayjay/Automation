import pdfplumber
from pdf2image import convert_from_path
from PIL import Image

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF using PDFplumber.
    """
    text_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text:
                text_data.append(f"Page {page_num}:\n{text}")
    return text_data


def extract_images_from_pdf(pdf_path, output_dir="images"):
    """
    Extract images from a PDF by converting each page to an image using pdf2image.
    """
    images = convert_from_path(pdf_path)
    image_paths = []

    for i, page_image in enumerate(images, start=1):
        image_path = f"{output_dir}/page_{i}.png"
        page_image.save(image_path, "PNG")
        image_paths.append(image_path)

    return image_paths


def main():
    # Input PDF path
    pdf_path = "mml-book.pdf"
    
    # Extract text from PDF
    print("Extracting text...")
    text_data = extract_text_from_pdf(pdf_path)
    for text in text_data:
        print(text)
    
    # Extract images from PDF
    print("Extracting images...")
    image_paths = extract_images_from_pdf(pdf_path)
    print("Images saved at:", image_paths)


if __name__ == "__main__":
    main()

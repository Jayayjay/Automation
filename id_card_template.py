from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import black
from pdfrw import PdfReader, PdfWriter, PageMerge
import os

def create_pdf_form(output_path="id_form.pdf"):
    """
    Create a fillable PDF form with text and signature placeholders.
    """
    c = canvas.Canvas(output_path, pagesize=A4)

    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, 800, "ID Card Information Form")

    # Labels and Text Fields
    c.setFont("Helvetica", 12)
    c.drawString(50, 750, "Full Name:")
    c.rect(150, 740, 300, 20)  # Placeholder for text

    c.drawString(50, 700, "ID Number:")
    c.rect(150, 690, 300, 20)  # Placeholder for text

    c.drawString(50, 650, "Upload Photo Here:")
    c.rect(150, 600, 100, 100)  # Placeholder for image

    c.drawString(50, 500, "Signature:")
    c.rect(150, 470, 200, 50)  # Placeholder for signature image

    # Instructions
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 420, "Please fill out all fields, upload a photo, and provide your signature in the designated area.")

    c.save()
    print(f"PDF form saved at: {output_path}")

def make_pdf_fillable(input_pdf, output_pdf):
    """
    Convert a regular PDF to a fillable PDF using pdfrw.
    """
    template_pdf = PdfReader(input_pdf)
    output = PdfWriter()

    for page in template_pdf.pages:
        annotations = page["/Annots"]
        if annotations:
            for annot in annotations:
                annot["/F"] = 4  # Make field visible
                annot.update({
                    "/DA": "0 g /Helv 12 Tf",
                    "/MK": {"/BC": [0, 0, 0], "/BG": [1, 1, 1]}
                })
        PageMerge(page).render()
        output.addpage(page)

    output.write(output_pdf)
    print(f"Fillable PDF saved at: {output_pdf}")

def main():
    # Create the base PDF form
    form_path = "id_form.pdf"
    fillable_form_path = "id_form_fillable.pdf"

    create_pdf_form(form_path)

    # Make the PDF fillable
    make_pdf_fillable(form_path, fillable_form_path)

    # Optional: Clean up original form
    if os.path.exists(form_path):
        os.remove(form_path)

if __name__ == "__main__":
    main()

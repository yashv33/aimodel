from fpdf import FPDF

def generate_pdf_report(text: str, output_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    # Split text to avoid PDF overflow
    for line in text.split('\n'):
        pdf.multi_cell(0, 10, line)
    pdf.output(output_path)

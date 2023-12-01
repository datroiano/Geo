from PDFCreation.__init__ import *


def raw_data_pdf(cleaned_response):
    download_folder = os.path.expanduser("~" + os.sep + "Downloads")
    pdf_filename = os.path.join(download_folder, "raw_data.pdf")

    doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

    content = []

    styles = getSampleStyleSheet()
    style = styles['Normal']

    json_data = json.dumps(cleaned_response, indent=2)

    json_paragraph = Paragraph(json_data, style)

    content.append(json_paragraph)
    doc.build(content)
    print(f"PDF saved as {pdf_filename}")
    subprocess.Popen(["start", "", pdf_filename], shell=True)


def write_dict_to_pdf(data, line_height=8, font_size=10):

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=font_size)

    json_str = json.dumps(data, indent=4)  # Convert the dictionary to a nicely formatted JSON string

    pdf.multi_cell(0, h=line_height, txt=json_str)  # Use multi_cell() for handling larger text

    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    output_path = os.path.join(download_folder, 'data_as_pdf.pdf')
    pdf.output(output_path)

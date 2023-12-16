from PDFCreation.__init__ import *
from UserInterface import sample_cleaned_data


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


# creation = raw_data_pdf(sample_cleaned_data.cleaned_data)


def write_dict_to_pdf(data, line_height=8, font_size=10, title="Simulation Results"):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", size=15)  # Set font for the title
    pdf.set_xy(0, 10)  # Position the title at coordinates (0, 10)
    pdf.cell(210, 10, txt=title, ln=True, align='C')  # Centered title

    pdf.set_font("Arial", size=font_size)  # Set font for the dictionary content

    json_str = json.dumps(data, indent=4)  # Convert the dictionary to a nicely formatted JSON string

    pdf.multi_cell(0, h=line_height, txt=json_str)  # Use multi_cell() for handling larger text

    download_folder = os.path.join(os.path.expanduser('~'), 'Downloads')
    output_path = os.path.join(download_folder, 'data_as_pdf.pdf')
    pdf.output(output_path)

from PDFCreation.__init__ import *


def raw_data_pdf(self, cleaned_response):
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
from fpdf import FPDF
import os

class PDF(FPDF):
    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "SmartFile AI - Summary Report", 0, 1, "C")
        self.ln(10)

    def section_title(self, title):
        self.set_font("Arial", "B", 14)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, title, 0, 1)
        self.ln(2)

    def section_body(self, text):
        self.set_font("Arial", "", 12)
        self.set_text_color(50, 50, 50)
        self.multi_cell(0, 8, text)
        self.ln()

    def insert_image(self, image_path, label):
        if os.path.exists(image_path):
            self.section_title(label)
            self.image(image_path, x=25, w=160)
            self.ln(10)

def generate_pdf(api_summary, web_summary, api_chart_path, web_chart_path, output_path="reports/smartfile_report.pdf"):
    pdf = PDF()
    pdf.add_page()

    # ✅ Add Summaries
    pdf.section_title("API File Summary")
    pdf.section_body(api_summary)

    pdf.section_title("Web File Summary")
    pdf.section_body(web_summary)

    # ✅ Add Charts
    pdf.insert_image(api_chart_path, "API Chart")
    pdf.insert_image(web_chart_path, "Web Chart")

    pdf.output(output_path)
    print(f"✅ PDF report generated: {output_path}")
    return output_path

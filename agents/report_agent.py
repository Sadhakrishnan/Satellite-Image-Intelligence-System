from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
import os

class ReportAgent:
    def __init__(self):
        pass

    def generate_pdf_report(self, data, summary, output_path):
        """
        Generates a professional PDF report.
        """
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title
        elements.append(Paragraph("Geospatial Intelligence Report", styles['Title']))
        elements.append(Spacer(1, 12))

        # Summary Section
        elements.append(Paragraph("Executive Summary", styles['Heading2']))
        elements.append(Paragraph(summary, styles['BodyText']))
        elements.append(Spacer(1, 12))

        # Statistics Table
        elements.append(Paragraph("Key Metrics", styles['Heading2']))
        table_data = [
            ["Metric", "Value"],
            ["Flood Area (sq km)", str(data.get('flood_area', 0))],
            ["Urban Growth (%)", str(data.get('urban_growth', 0))],
            ["Vegetation Loss (%)", str(data.get('veg_loss', 0))],
            ["Wildfire Detected", "Yes" if data.get('wildfire', False) else "No"]
        ]
        
        t = Table(table_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 12))

        # AI Insights
        elements.append(Paragraph("AI-Generated Intelligence Insights", styles['Heading2']))
        elements.append(Paragraph(data.get('insights', "No additional insights provided."), styles['BodyText']))

        doc.build(elements)
        print(f"Report generated: {output_path}")

if __name__ == "__main__":
    agent = ReportAgent()
    data = {"flood_area": 12.4, "urban_growth": 25, "veg_loss": 11, "wildfire": True, "insights": "The region is undergoing rapid development..."}
    agent.generate_pdf_report(data, "This is a sample summary.", "sample_report.pdf")

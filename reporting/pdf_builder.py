import os
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch


def add_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica-Bold', 48)
    canvas.setFillColor(colors.Color(0.95, 0.95, 0.95))
    canvas.setFillAlpha(0.3)
    canvas.drawCentredString(A4[0]/2, A4[1]/2, "BeaconAI")
    canvas.setFillAlpha(1.0)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0]/2, 0.5 * inch, "© 2024 BeaconAI. All rights reserved.")
    canvas.restoreState()


def generate_pdf_report(company_name, persona, insights, solution_section, output_path="generated_reports"):
    os.makedirs(output_path, exist_ok=True)
    filename = f"{company_name}_{persona}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}.pdf"
    filepath = os.path.join(output_path, filename)
    doc = SimpleDocTemplate(filepath, pagesize=A4, onFirstPage=add_footer, onLaterPages=add_footer)
    styles = getSampleStyleSheet()
    body = []

    def styled_paragraph(text, style):
        return Paragraph(text, style)

    def section_title(text):
        return styled_paragraph(text, ParagraphStyle('SectionHeader', parent=styles['Heading2'],
            fontSize=16, fontName='Helvetica-Bold', textColor=colors.Color(0.2, 0.6, 0.8),
            spaceAfter=15, spaceBefore=20))

    # Logo
    logo_path = "reporting/assets/beaconai_logo.png"
    if os.path.exists(logo_path):
        body.append(Image(logo_path, width=160, height=45))
        body.append(Spacer(1, 25))

    # Title and Subtitle
    body.append(styled_paragraph("AI Readiness Insight Report", ParagraphStyle('TitleCentered',
        parent=styles['Title'], alignment=TA_CENTER, fontSize=24, fontName='Helvetica-Bold',
        textColor=colors.Color(0.2, 0.4, 0.8), spaceAfter=20)))
    body.append(styled_paragraph(f"<b>{company_name}</b>", ParagraphStyle('SubtitleCentered',
        parent=styles['Normal'], alignment=TA_CENTER, fontSize=14, fontName='Helvetica',
        textColor=colors.Color(0.4, 0.4, 0.4), spaceAfter=30)))

    # Info Table
    info_data = [
        [Paragraph("<b>👤 Persona:</b>", styles['Normal']), Paragraph(persona, styles['Normal'])],
        [Paragraph("<b>🗕️ Date:</b>", styles['Normal']), Paragraph(datetime.now().strftime('%B %d, %Y'), styles['Normal'])],
        [Paragraph("<b>🏢 Company:</b>", styles['Normal']), Paragraph(company_name, styles['Normal'])]
    ]
    info_table = Table(info_data, colWidths=[120, 300])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.Color(0.95, 0.97, 1.0)),
        ("BOX", (0, 0), (-1, -1), 1, colors.Color(0.8, 0.9, 1.0)),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    body.append(info_table)
    body.append(Spacer(1, 30))

    # Insights
    body.append(section_title("🔍 CARE Diagnostic Insights"))
    for qid, content in insights.items():
        insight_data = [
            [Paragraph(f"<b>{qid}: {content.get('question')}</b>", styles['Normal'])],
            [Paragraph(f"<b>Answer:</b> {content.get('answer')}", styles['Normal'])],
            [Paragraph(f"<b>💡 Strategic Insight:</b>", styles['Normal'])],
            [Paragraph(content.get('insight'), styles['Normal'])]
        ]
        insight_table = Table(insight_data, colWidths=[460])
        insight_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.2, 0.6, 0.8)),
            ("BACKGROUND", (0, 1), (-1, 1), colors.whitesmoke),
            ("BACKGROUND", (0, 2), (-1, 2), colors.Color(0.9, 0.95, 1.0)),
            ("BACKGROUND", (0, 3), (-1, 3), colors.Color(0.98, 0.98, 1.0)),
            ("BOX", (0, 0), (-1, -1), 1, colors.Color(0.7, 0.8, 0.9)),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
        ]))
        body.append(insight_table)
        body.append(Spacer(1, 20))

    # Solution
    body.append(section_title("🛠 How BeaconAI Can Help You"))
    body.append(Table([[Paragraph(solution_section, ParagraphStyle('NormalText', parent=styles['BodyText'], fontSize=11, alignment=TA_JUSTIFY))]],
                      colWidths=[460],
                      style=[
                          ("BACKGROUND", (0, 0), (-1, -1), colors.Color(0.98, 0.99, 1.0)),
                          ("BOX", (0, 0), (-1, -1), 2, colors.Color(0.2, 0.6, 0.8)),
                          ("LEFTPADDING", (0, 0), (-1, -1), 15),
                          ("TOPPADDING", (0, 0), (-1, -1), 12)
                      ]))
    body.append(Spacer(1, 30))

    # Contact CTA
    body.append(section_title("📞 Get In Touch"))
    cta_info = [
        [Paragraph("<b>📞 Contact Us</b>", styles['Normal'])],
        [Paragraph("📱 <b>Phone:</b> +1 (720) 749-1174", styles['Normal'])],
        [Paragraph("✉️ <b>Email:</b> info@beaconai.ai", styles['Normal'])],
        [Paragraph("🗓 <b>Schedule a call:</b>", styles['Normal'])],
        [Paragraph('<a href="https://app.usemotion.com/meet/dalemyska/linkedin" color="blue"><u>🌟 Book Consultation →</u></a>', styles['Normal'])]
    ]
    body.append(Table(cta_info, colWidths=[460], style=[
        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.2, 0.6, 0.8)),
        ("BACKGROUND", (0, 1), (-1, -1), colors.Color(0.98, 0.99, 1.0)),
        ("BOX", (0, 0), (-1, -1), 2, colors.Color(0.1, 0.4, 0.7)),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("TOPPADDING", (0, 0), (-1, -1), 12)
    ]))

    doc.build(body)
    return filepath

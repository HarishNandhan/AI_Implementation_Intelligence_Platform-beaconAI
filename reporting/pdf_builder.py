import os
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def add_footer(canvas, doc):
    """Add copyright footer and subtle watermark to each page"""
    canvas.saveState()
    
    # Add subtle BeaconAI watermark
    canvas.setFont('Helvetica-Bold', 48)
    canvas.setFillColor(colors.Color(0.95, 0.95, 0.95))  # Very light grey
    canvas.setFillAlpha(0.3)  # 30% opacity
    canvas.drawCentredString(A4[0]/2, A4[1]/2, "BeaconAI")
    canvas.setFillAlpha(1.0)  # Reset opacity
    
    # Add copyright footer
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(colors.grey)
    canvas.drawCentredString(A4[0]/2, 0.5*inch, "© 2024 BeaconAI. All rights reserved.")
    
    canvas.restoreState()

def generate_pdf_report(company_name: str, persona: str, insights: dict, solution_section: str, output_path: str = "generated_reports") -> str:
    """
    Generates a beautifully designed PDF with BeaconAI branding, per-question insights, and a final solution section.
    """
    os.makedirs(output_path, exist_ok=True)

    filename = f"{company_name}_{persona}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}.pdf"
    filepath = os.path.join(output_path, filename)

    doc = SimpleDocTemplate(filepath, pagesize=A4, onFirstPage=add_footer, onLaterPages=add_footer)
    styles = getSampleStyleSheet()
    body = []

    # Beautiful custom styles
    title_style = ParagraphStyle(
        'TitleCentered', 
        parent=styles['Title'], 
        alignment=TA_CENTER,
        fontSize=24,
        fontName='Helvetica-Bold',
        textColor=colors.Color(0.2, 0.4, 0.8),  # Dark blue
        spaceAfter=20
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleCentered',
        parent=styles['Normal'],
        alignment=TA_CENTER,
        fontSize=14,
        fontName='Helvetica',
        textColor=colors.Color(0.4, 0.4, 0.4),  # Medium grey
        spaceAfter=30
    )
    
    section_header = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=16,
        fontName='Helvetica-Bold',
        textColor=colors.Color(0.2, 0.6, 0.8),  # Blue
        spaceAfter=15,
        spaceBefore=20
    )
    
    question_style = ParagraphStyle(
        'QuestionStyle',
        parent=styles['BodyText'],
        fontSize=12,
        fontName='Helvetica-Bold',
        textColor=colors.Color(0.2, 0.2, 0.2),  # Dark grey
        spaceAfter=8
    )
    
    answer_style = ParagraphStyle(
        'AnswerStyle',
        parent=styles['BodyText'],
        fontSize=11,
        fontName='Helvetica',
        textColor=colors.Color(0.4, 0.4, 0.4),  # Medium grey
        spaceAfter=10
    )
    
    insight_style = ParagraphStyle(
        'InsightCentered',
        parent=styles['BodyText'],
        alignment=TA_CENTER,
        fontSize=12,
        fontName='Helvetica',
        textColor=colors.Color(0.1, 0.1, 0.1),  # Almost black
        spaceAfter=15,
        leftIndent=20,
        rightIndent=20,
        backColor=colors.Color(0.98, 0.98, 1.0)  # Very light blue background
    )
    
    normal = ParagraphStyle(
        'NormalText',
        parent=styles['BodyText'],
        fontSize=11,
        fontName='Helvetica',
        textColor=colors.Color(0.2, 0.2, 0.2),
        alignment=TA_JUSTIFY
    )
    
    small = ParagraphStyle(
        name='Small', 
        parent=styles['Normal'], 
        fontSize=9,
        fontName='Helvetica',
        textColor=colors.Color(0.5, 0.5, 0.5)
    )

    # Optional: Add logo
    logo_path = "reporting/assets/beaconai_logo.png"
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=160, height=45)
        body.append(logo)
        body.append(Spacer(1, 25))

    # Beautiful cover page
    body.append(Paragraph(f"AI Readiness Insight Report", title_style))
    body.append(Paragraph(f"<b>{company_name}</b>", subtitle_style))
    body.append(Spacer(1, 15))
    
    # Company info in a styled table
    info_data = [
        [Paragraph("<b>👤 Persona:</b>", small), Paragraph(persona, small)],
        [Paragraph("<b>📅 Date:</b>", small), Paragraph(datetime.now().strftime('%B %d, %Y'), small)],
        [Paragraph("<b>🏢 Company:</b>", small), Paragraph(company_name, small)]
    ]
    
    info_table = Table(info_data, colWidths=[120, 300])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.Color(0.95, 0.97, 1.0)),
        ("BOX", (0, 0), (-1, -1), 1, colors.Color(0.8, 0.9, 1.0)),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    body.append(info_table)
    body.append(Spacer(1, 30))

    # Beautiful Insights Section
    body.append(Paragraph("🔍 CARE Diagnostic Insights", section_header))
    
    for qid, content in insights.items():
        question = content.get("question", "")
        answer = content.get("answer", "")
        insight = content.get("insight", "")

        # Create a beautiful insight card
        insight_data = [
            [Paragraph(f"<b>{qid}: {question}</b>", question_style)],
            [Paragraph(f"<b>Answer:</b> {answer}", answer_style)],
            [Paragraph(f"<b>💡 Strategic Insight:</b>", answer_style)],
            [Paragraph(insight, insight_style)]
        ]
        
        insight_table = Table(insight_data, colWidths=[460])
        insight_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.2, 0.6, 0.8)),  # Blue header
            ("BACKGROUND", (0, 1), (-1, 1), colors.Color(0.95, 0.95, 0.95)),  # Light grey for answer
            ("BACKGROUND", (0, 2), (-1, 2), colors.Color(0.9, 0.95, 1.0)),  # Light blue for insight label
            ("BACKGROUND", (0, 3), (-1, 3), colors.Color(0.98, 0.98, 1.0)),  # Very light blue for insight
            ("BOX", (0, 0), (-1, -1), 1, colors.Color(0.7, 0.8, 0.9)),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.Color(0.8, 0.9, 1.0)),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("LEFTPADDING", (0, 0), (-1, -1), 12),
            ("TOPPADDING", (0, 0), (-1, -1), 8),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),  # White text for header
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ]))
        
        body.append(insight_table)
        body.append(Spacer(1, 20))

    # Beautiful Solution Summary
    body.append(Spacer(1, 25))
    body.append(Paragraph("🛠 How BeaconAI Can Help You", section_header))
    
    # Solution in a styled box
    solution_data = [
        [Paragraph(solution_section, normal)]
    ]
    
    solution_table = Table(solution_data, colWidths=[460])
    solution_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.Color(0.98, 0.99, 1.0)),
        ("BOX", (0, 0), (-1, -1), 2, colors.Color(0.2, 0.6, 0.8)),
        ("ALIGN", (0, 0), (-1, -1), "LEFT"),
        ("LEFTPADDING", (0, 0), (-1, -1), 15),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    body.append(solution_table)
    body.append(Spacer(1, 30))

    # Beautiful Contact Section
    body.append(Paragraph("📞 Get In Touch", section_header))
    
    cta_data = [
        [Paragraph("<b>📞 Contact Us</b>", normal)],
        [Paragraph("📱 <b>Phone:</b> +1 (720) 749-1174", small)],
        [Paragraph("✉️ <b>Email:</b> info@beaconai.ai", small)],
        [Paragraph("📅 <b>Schedule a call with Dale:</b>", small)],
        [Paragraph('<a href="https://app.usemotion.com/meet/dalemyska/linkedin" color="blue"><u>🎯 Book Your Consultation →</u></a>', small)]
    ]

    cta_table = Table(cta_data, colWidths=[460])
    cta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.2, 0.6, 0.8)),  # Blue header
        ("BACKGROUND", (0, 1), (-1, -1), colors.Color(0.98, 0.99, 1.0)),  # Light blue background
        ("BOX", (0, 0), (-1, -1), 2, colors.Color(0.1, 0.4, 0.7)),  # Dark blue border
        ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.Color(0.8, 0.9, 1.0)),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("LEFTPADDING", (0, 0), (-1, -1), 20),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, 0), 14),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("ROUNDEDCORNERS", [10, 10, 10, 10]),
    ]))
    body.append(cta_table)

    # Build PDF
    doc.build(body)
    return filepath

import os
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.pdfgen import canvas as pdf_canvas

# Visual Identity Colors
NAVY_BLUE = colors.Color(0.04, 0.19, 0.38)  # #0A3161
AMBER = colors.Color(1.0, 0.65, 0.0)        # #FFA500
TEAL = colors.Color(0.0, 0.5, 0.5)          # #008080
LIGHT_GRAY = colors.Color(0.95, 0.95, 0.95)
WHITE = colors.white

def add_header_footer(canvas, doc):
    """Professional header and footer for consultant report"""
    canvas.saveState()
    
    # Get page dimensions
    page_width = A4[0]
    page_height = A4[1]
    
    try:
        # Header background - Navy Blue
        canvas.setFillColorRGB(0.04, 0.19, 0.38)  # Navy Blue
        canvas.rect(0, page_height - 60, page_width, 60, fill=1, stroke=0)
        
        # Header text - White
        canvas.setFillColorRGB(1, 1, 1)  # White
        canvas.setFont('Helvetica-Bold', 14)
        canvas.drawString(40, page_height - 35, "beaconAI")
        canvas.setFont('Helvetica', 10)
        canvas.drawString(40, page_height - 50, "AI Implementation Intelligence Platform")
        
        # Amber accent line
        canvas.setFillColorRGB(1.0, 0.65, 0.0)  # Amber
        canvas.rect(0, page_height - 65, page_width, 5, fill=1, stroke=0)
        
        # Footer background - Navy Blue
        canvas.setFillColorRGB(0.04, 0.19, 0.38)  # Navy Blue
        canvas.rect(0, 0, page_width, 40, fill=1, stroke=0)
        
        # Footer text - White
        canvas.setFillColorRGB(1, 1, 1)  # White
        canvas.setFont('Helvetica', 8)
        canvas.drawString(40, 20, "© 2025 beaconAI. All rights reserved.")
        canvas.drawString(40, 10, "info@beaconai.ai | +1 (303) 877-4292")
        
        # Page number
        canvas.drawRightString(page_width - 40, 20, f"Page {doc.page}")
        
    except Exception as e:
        # Fallback: simple text header/footer if graphics fail
        canvas.setFillColorRGB(0, 0, 0)  # Black text
        canvas.setFont('Helvetica-Bold', 10)
        canvas.drawString(40, page_height - 30, "beaconAI - AI Implementation Intelligence Platform")
        canvas.setFont('Helvetica', 8)
        canvas.drawString(40, 20, "© 2025 beaconAI. All rights reserved.")
        canvas.drawRightString(page_width - 40, 20, f"Page {doc.page}")
    
    canvas.restoreState()


def create_professional_styles():
    """Create professional styles following visual identity standards"""
    styles = getSampleStyleSheet()
    
    # Helper function to safely add styles
    def safe_add_style(name, style_def):
        if name not in styles:
            styles.add(style_def)
        return styles[name]
    
    # Main Title Style (Montserrat equivalent)
    safe_add_style('MainTitle', ParagraphStyle(
        name='MainTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=28,
        textColor=NAVY_BLUE,
        alignment=TA_CENTER,
        spaceAfter=30,
        spaceBefore=20
    ))
    
    # Section Header Style - with keepWithNext to prevent page breaks
    safe_add_style('SectionHeader', ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=NAVY_BLUE,
        alignment=TA_LEFT,
        spaceAfter=5,  # Reduced spacing
        spaceBefore=20,  # Reduced spacing
        keepWithNext=True,  # Keep with next paragraph
        borderWidth=0,
        borderColor=AMBER,
        borderPadding=0,
        leftIndent=0
    ))
    
    # Subsection Header Style - with keepWithNext
    safe_add_style('SubsectionHeader', ParagraphStyle(
        name='SubsectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=TEAL,
        alignment=TA_LEFT,
        spaceAfter=8,  # Reduced spacing
        spaceBefore=15,  # Reduced spacing
        keepWithNext=True  # Keep with next paragraph
    ))
    
    # Professional Body Text Style (Source Sans Pro equivalent)
    safe_add_style('ProfessionalBody', ParagraphStyle(
        name='ProfessionalBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
        spaceAfter=12,
        leading=14
    ))
    
    # Executive Summary Style
    safe_add_style('ExecutiveSummary', ParagraphStyle(
        name='ExecutiveSummary',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        textColor=colors.black,
        alignment=TA_JUSTIFY,
        spaceAfter=15,
        leading=16,
        leftIndent=20,
        rightIndent=20
    ))
    
    return styles

def generate_pdf_report(company_name, persona, insights, solution_section, output_path=None):
    # Use Docker-aware path
    if output_path is None:
        output_path = "/app/generated_reports" if os.getenv("DOCKER_ENV") else "generated_reports"
    
    os.makedirs(output_path, exist_ok=True)
    filename = f"{company_name.replace(' ', '_')}_{persona}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(output_path, filename)
    
    # Create document with standard margins (no header/footer callbacks)
    doc = SimpleDocTemplate(
        filepath, 
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )
    
    styles = create_professional_styles()
    story = []

    # COVER PAGE
    # Add header as content
    header_data = [
        ["beaconAI", "AI Implementation Intelligence Platform"]
    ]
    
    header_table = Table(header_data, colWidths=[200, 280])
    header_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
        ("FONTNAME", (0, 0), (0, -1), 'Helvetica-Bold'),
        ("FONTNAME", (1, 0), (1, -1), 'Helvetica'),
        ("FONTSIZE", (0, 0), (0, -1), 14),
        ("FONTSIZE", (1, 0), (1, -1), 10),
        ("ALIGN", (0, 0), (0, -1), 'LEFT'),
        ("ALIGN", (1, 0), (1, -1), 'RIGHT'),
        ("VALIGN", (0, 0), (-1, -1), 'MIDDLE'),
        ("LEFTPADDING", (0, 0), (-1, -1), 15),
        ("RIGHTPADDING", (0, 0), (-1, -1), 15),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
    ]))
    
    story.append(header_table)
    
    # Amber accent line
    accent_header = Table([[""]], colWidths=[480])
    accent_header.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMBER),
        ("LINEBELOW", (0, 0), (-1, -1), 5, AMBER),
    ]))
    story.append(accent_header)
    story.append(Spacer(1, 30))
    
    # Logo - use Docker-aware path
    if os.getenv("DOCKER_ENV"):
        logo_path = "/app/reporting/assets/beaconai_logo.png"
    else:
        logo_path = "reporting/assets/beaconai_logo.png"
    
    if os.path.exists(logo_path):
        # Optimal dimensions for 500x300 image: maintain aspect ratio
        story.append(Image(logo_path, width=120, height=72))
        story.append(Spacer(1, 40))

    # Main Title
    story.append(Paragraph("AI READINESS ASSESSMENT REPORT", styles['MainTitle']))
    story.append(Spacer(1, 30))
    
    # Company Name with Amber accent
    company_style = ParagraphStyle(
        'CompanyName',
        parent=styles['MainTitle'],
        fontSize=22,
        textColor=AMBER,
        alignment=TA_CENTER
    )
    story.append(Paragraph(f"<b>{company_name.upper()}</b>", company_style))
    story.append(Spacer(1, 50))
    
    # Executive Information Table
    exec_data = [
        ["REPORT DETAILS", ""],
        ["Client Organization", company_name],
        ["Assessment Date", datetime.now().strftime('%B %d, %Y')],
        ["Stakeholder Role", persona],
        ["Assessment Framework", "CARE Diagnostic Model"],
        ["Prepared By", "beaconAI AI Readiness Intelligence Engine"]
    ]
    
    exec_table = Table(exec_data, colWidths=[150, 300])
    exec_table.setStyle(TableStyle([
        # Header row
        ("BACKGROUND", (0, 0), (-1, 0), NAVY_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), 'Helvetica-Bold'),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("SPAN", (0, 0), (1, 0)),
        ("ALIGN", (0, 0), (-1, 0), 'CENTER'),
        
        # Data rows
        ("BACKGROUND", (0, 1), (0, -1), LIGHT_GRAY),
        ("FONTNAME", (0, 1), (0, -1), 'Helvetica-Bold'),
        ("FONTNAME", (1, 1), (1, -1), 'Helvetica'),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 1, NAVY_BLUE),
        ("VALIGN", (0, 0), (-1, -1), 'MIDDLE'),
        ("LEFTPADDING", (0, 0), (-1, -1), 15),
        ("RIGHTPADDING", (0, 0), (-1, -1), 15),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
    ]))
    
    story.append(exec_table)
    story.append(PageBreak())
    
    # EXECUTIVE SUMMARY
    story.append(Paragraph("EXECUTIVE SUMMARY", styles['SectionHeader']))
    
    # Add amber accent line under section headers
    accent_line = Table([[""]], colWidths=[500])
    accent_line.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMBER),
        ("LINEBELOW", (0, 0), (-1, -1), 3, AMBER),
    ]))
    story.append(accent_line)
    story.append(Spacer(1, 20))
    
    summary_text = f"""
    This comprehensive AI readiness assessment evaluates {company_name}'s current position and strategic opportunities 
    for artificial intelligence implementation. Through our proprietary CARE diagnostic framework (Culture, 
    Adoption, Readiness, and Evolution), we have identified key insights and actionable recommendations to accelerate 
    your organization's AI transformation journey.
    
    The assessment reveals specific areas of strength and opportunities for improvement, providing a clear roadmap 
    for successful AI adoption aligned with your business objectives and operational capabilities.
    """
    
    story.append(Paragraph(summary_text, styles['ExecutiveSummary']))
    story.append(Spacer(1, 30))
    
    # ASSESSMENT METHODOLOGY
    story.append(Paragraph("ASSESSMENT METHODOLOGY", styles['SectionHeader']))
    story.append(accent_line)
    story.append(Spacer(1, 20))
    
    methodology_text = """
    Our CARE diagnostic framework provides a structured approach to evaluating AI readiness across four critical dimensions:
    """
    
    story.append(Paragraph(methodology_text, styles['ProfessionalBody']))
    story.append(Spacer(1, 15))
    
    # Add each dimension as separate paragraphs for better formatting
    dimensions = [
        ("<b>Culture:</b> Organizational mindset, change readiness, and cultural alignment with AI adoption"),
        ("<b>Adoption:</b> Strategic vision, leadership commitment, and implementation approach"),
        ("<b>Readiness:</b> Technical infrastructure, data maturity, and existing technology capabilities"),
        ("<b>Evolution:</b> Long-term planning, scalability considerations, and continuous improvement frameworks")
    ]
    
    bullet_style = ParagraphStyle(
        'BulletPoint',
        parent=styles['ProfessionalBody'],
        fontSize=11,
        leftIndent=20,
        spaceAfter=8,
        bulletIndent=10,
        bulletFontName='Symbol'
    )
    
    for dimension in dimensions:
        story.append(Paragraph(f"• {dimension}", bullet_style))
    story.append(PageBreak())
    
    # DETAILED FINDINGS
    story.append(Paragraph("DETAILED ASSESSMENT FINDINGS", styles['SectionHeader']))
    
    findings_accent = Table([[""]], colWidths=[500])
    findings_accent.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMBER),
        ("LINEBELOW", (0, 0), (-1, -1), 3, AMBER),
    ]))
    story.append(findings_accent)
    story.append(Spacer(1, 10))
    
    # Group insights by category
    categories = {'C': 'CULTURE', 'A': 'ADOPTION', 'R': 'READINESS', 'E': 'EVOLUTION'}
    
    for category_key, category_name in categories.items():
        category_insights = {k: v for k, v in insights.items() if k.startswith(category_key)}
        
        if category_insights:
            # Create a list to hold all category content
            category_content = []
            
            # Add category header to the content list
            category_content.append(Paragraph(f"{category_name} ASSESSMENT", styles['SubsectionHeader']))
            category_content.append(Spacer(1, 10))
            
            # Process each insight in this category
            insight_items = list(category_insights.items())
            
            for i, (qid, content) in enumerate(insight_items):
                # Question header
                question_style = ParagraphStyle(
                    'QuestionHeader',
                    parent=styles['ProfessionalBody'],
                    fontName='Helvetica-Bold',
                    fontSize=12,
                    textColor=NAVY_BLUE,
                    spaceAfter=8
                )
                category_content.append(Paragraph(f"Assessment Item {qid}: {content.get('question')}", question_style))
                
                # Response
                response_style = ParagraphStyle(
                    'Response',
                    parent=styles['ProfessionalBody'],
                    fontSize=10,
                    textColor=colors.black,
                    spaceAfter=10,
                    leftIndent=20
                )
                category_content.append(Paragraph(f"<b>Response:</b> {content.get('answer')}", response_style))
                
                # Strategic Analysis
                analysis_style = ParagraphStyle(
                    'Analysis',
                    parent=styles['ProfessionalBody'],
                    fontSize=11,
                    textColor=colors.black,
                    alignment=TA_JUSTIFY,
                    spaceAfter=20,
                    leftIndent=20,
                    rightIndent=20
                )
                category_content.append(Paragraph(f"<b>Strategic Analysis:</b> {content.get('insight')}", analysis_style))
                
                # Add separator line (except for the last item)
                if i < len(insight_items) - 1:
                    separator = Table([[""]], colWidths=[500])
                    separator.setStyle(TableStyle([
                        ("LINEBELOW", (0, 0), (-1, -1), 1, LIGHT_GRAY),
                    ]))
                    category_content.append(separator)
                    category_content.append(Spacer(1, 15))
            
            # Keep the entire category (header + first few items) together
            # Split into smaller groups if there are many items
            if len(category_insights) <= 2:
                # Keep entire category together if 2 or fewer items
                story.append(KeepTogether(category_content))
            else:
                # For larger categories, keep header with first item, then add others
                header_with_first = category_content[:6]  # Header + spacer + first complete item
                story.append(KeepTogether(header_with_first))
                
                # Add remaining items
                remaining_content = category_content[6:]
                for item in remaining_content:
                    story.append(item)
            
            # Add space between categories
            story.append(Spacer(1, 20))
    
    story.append(PageBreak())
    
    # STRATEGIC RECOMMENDATIONS
    story.append(Paragraph("STRATEGIC RECOMMENDATIONS", styles['SectionHeader']))
    
    recommendations_accent = Table([[""]], colWidths=[500])
    recommendations_accent.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMBER),
        ("LINEBELOW", (0, 0), (-1, -1), 3, AMBER),
    ]))
    story.append(recommendations_accent)
    story.append(Spacer(1, 10))
    
    # Solution section in professional format
    solution_style = ParagraphStyle(
        'Solution',
        parent=styles['ProfessionalBody'],
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=15,
        leading=15
    )
    story.append(Paragraph(solution_section, solution_style))
    story.append(Spacer(1, 30))
    
    # NEXT STEPS & CONTACT
    story.append(Paragraph("NEXT STEPS & ENGAGEMENT", styles['SectionHeader']))
    
    nextsteps_accent = Table([[""]], colWidths=[500])
    nextsteps_accent.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), AMBER),
        ("LINEBELOW", (0, 0), (-1, -1), 3, AMBER),
    ]))
    story.append(nextsteps_accent)
    story.append(Spacer(1, 10))
    
    next_steps_intro = """
    Based on this assessment, we recommend scheduling a strategic consultation to discuss:
    """
    
    story.append(Paragraph(next_steps_intro, styles['ProfessionalBody']))
    story.append(Spacer(1, 15))
    
    # Add each next step as separate bullet points
    next_steps = [
        "Detailed implementation roadmap and timeline",
        "Resource allocation and investment planning",
        "Technology stack recommendations and vendor selection", 
        "Change management and training programs",
        "Success metrics and performance monitoring frameworks"
    ]
    
    for step in next_steps:
        story.append(Paragraph(f"• {step}", bullet_style))
    
    story.append(Spacer(1, 15))
    
    conclusion_text = """
    Our team is ready to partner with you in transforming these insights into actionable results.
    """
    
    story.append(Paragraph(conclusion_text, styles['ProfessionalBody']))
    story.append(Spacer(1, 20))
    
    # Call-to-Action Section
    cta_style = ParagraphStyle(
        'CallToAction',
        parent=styles['ProfessionalBody'],
        fontSize=12,
        fontName='Helvetica-Bold',
        textColor=NAVY_BLUE,
        alignment=TA_CENTER,
        spaceAfter=20,
        spaceBefore=10
    )
    story.append(Paragraph("Ready to Transform Your AI Strategy?", cta_style))
    story.append(Spacer(1, 20))
    
    # Contact Information Table with better alignment
    contact_data = [
        [Paragraph("<b>bEACONAI CONSULTING TEAM</b>", styles['ProfessionalBody']), ""],
        [Paragraph("<b>Email</b>", styles['ProfessionalBody']), 
         Paragraph('<a href="mailto:info@beaconai.ai" color="blue">info@beaconai.ai</a>', styles['ProfessionalBody'])],
        [Paragraph("<b>Phone</b>", styles['ProfessionalBody']), 
         Paragraph('<a href="tel:+13038774292" color="blue">+1 (303) 877-4292</a>', styles['ProfessionalBody'])],
        [Paragraph("<b>Schedule Consultation</b>", styles['ProfessionalBody']), 
         Paragraph('<a href="https://app.usemotion.com/meet/dalemyska/linkedin" color="blue"><u>Book Your Strategy Session →</u></a>', styles['ProfessionalBody'])],
        [Paragraph("<b>Website</b>", styles['ProfessionalBody']), 
         Paragraph('<a href="https://www.beaconai.ai" color="blue">www.beaconai.ai</a>', styles['ProfessionalBody'])]
    ]
    
    contact_table = Table(contact_data, colWidths=[160, 260])  # Adjusted column widths
    contact_table.setStyle(TableStyle([
        # Header
        ("BACKGROUND", (0, 0), (-1, 0), AMBER),
        ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
        ("FONTNAME", (0, 0), (-1, 0), 'Helvetica-Bold'),
        ("FONTSIZE", (0, 0), (-1, 0), 12),
        ("SPAN", (0, 0), (1, 0)),
        ("ALIGN", (0, 0), (-1, 0), 'CENTER'),
        
        # Data rows
        ("BACKGROUND", (0, 1), (0, -1), LIGHT_GRAY),
        ("FONTNAME", (0, 1), (0, -1), 'Helvetica-Bold'),
        ("FONTSIZE", (0, 1), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 1, NAVY_BLUE),
        ("VALIGN", (0, 0), (-1, -1), 'MIDDLE'),
        ("LEFTPADDING", (0, 0), (-1, -1), 15),
        ("RIGHTPADDING", (0, 0), (-1, -1), 15),
        ("TOPPADDING", (0, 0), (-1, -1), 12),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ("ALIGN", (0, 0), (-1, -1), 'LEFT'),  # Left align all content
        ("VALIGN", (0, 0), (-1, -1), 'TOP'),  # Top align for better text flow
    ]))
    
    # Keep the contact table together on one page
    story.append(KeepTogether([contact_table]))
    
    # Add footer information as content
    story.append(Spacer(1, 30))
    
    # Footer content table
    footer_data = [
        ["© 2025 beaconAI. All rights reserved.", f"Generated: {datetime.now().strftime('%B %d, %Y')}"],
        ["info@beaconai.ai | +1 (303) 877-4292", "AI Implementation Intelligence Platform"]
    ]
    
    footer_table = Table(footer_data, colWidths=[280, 200])
    footer_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), NAVY_BLUE),
        ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
        ("FONTNAME", (0, 0), (-1, -1), 'Helvetica'),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("ALIGN", (0, 0), (0, -1), 'LEFT'),
        ("ALIGN", (1, 0), (1, -1), 'RIGHT'),
        ("VALIGN", (0, 0), (-1, -1), 'MIDDLE'),
        ("LEFTPADDING", (0, 0), (-1, -1), 15),
        ("RIGHTPADDING", (0, 0), (-1, -1), 15),
        ("TOPPADDING", (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
    ]))
    
    story.append(footer_table)
    
    # Build the PDF
    doc.build(story)
    return filepath

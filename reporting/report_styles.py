"""
Professional Report Styles
"""
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT, TA_RIGHT
from .report_config import ReportColors

def create_professional_styles():
    """Create professional styles following visual identity standards"""
    styles = getSampleStyleSheet()
    
    # Helper function to safely add styles
    def safe_add_style(name, style_def):
        if name not in styles:
            styles.add(style_def)
        return styles[name]
    
    # Main Title Style
    safe_add_style('MainTitle', ParagraphStyle(
        name='MainTitle',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=28,
        textColor=ReportColors.NAVY_BLUE,
        alignment=TA_CENTER,
        spaceAfter=30,
        spaceBefore=20
    ))
    
    # Company Name Style
    safe_add_style('CompanyName', ParagraphStyle(
        name='CompanyName',
        parent=styles['Title'],
        fontName='Helvetica-Bold',
        fontSize=22,
        textColor=ReportColors.AMBER,
        alignment=TA_CENTER,
        spaceAfter=50,
        spaceBefore=30
    ))
    
    # Section Header Style
    safe_add_style('SectionHeader', ParagraphStyle(
        name='SectionHeader',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        textColor=ReportColors.NAVY_BLUE,
        alignment=TA_LEFT,
        spaceAfter=5,
        spaceBefore=20,
        keepWithNext=True
    ))
    
    # Subsection Header Style
    safe_add_style('SubsectionHeader', ParagraphStyle(
        name='SubsectionHeader',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=14,
        textColor=ReportColors.TEAL,
        alignment=TA_LEFT,
        spaceAfter=8,
        spaceBefore=15,
        keepWithNext=True
    ))
    
    # Professional Body Text Style
    safe_add_style('ProfessionalBody', ParagraphStyle(
        name='ProfessionalBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        textColor=ReportColors.BLACK,
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
        textColor=ReportColors.BLACK,
        alignment=TA_JUSTIFY,
        spaceAfter=15,
        leading=16,
        leftIndent=20,
        rightIndent=20
    ))
    
    # Question Header Style
    safe_add_style('QuestionHeader', ParagraphStyle(
        name='QuestionHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=ReportColors.NAVY_BLUE,
        spaceAfter=8
    ))
    
    # Response Style
    safe_add_style('Response', ParagraphStyle(
        name='Response',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        textColor=ReportColors.BLACK,
        spaceAfter=10,
        leftIndent=20
    ))
    
    # Analysis Style
    safe_add_style('Analysis', ParagraphStyle(
        name='Analysis',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        textColor=ReportColors.BLACK,
        alignment=TA_JUSTIFY,
        spaceAfter=20,
        leftIndent=20,
        rightIndent=20
    ))
    
    # Bullet Point Style
    safe_add_style('BulletPoint', ParagraphStyle(
        name='BulletPoint',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leftIndent=20,
        spaceAfter=8,
        bulletIndent=10,
        bulletFontName='Symbol'
    ))
    
    # Solution Style
    safe_add_style('Solution', ParagraphStyle(
        name='Solution',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        alignment=TA_JUSTIFY,
        spaceAfter=15,
        leading=15
    ))
    
    # Call-to-Action Style
    safe_add_style('CallToAction', ParagraphStyle(
        name='CallToAction',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        textColor=ReportColors.NAVY_BLUE,
        alignment=TA_CENTER,
        spaceAfter=20,
        spaceBefore=10
    ))
    
    return styles
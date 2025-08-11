"""
Report Components - Reusable PDF elements
"""
import os
from datetime import datetime
from reportlab.platypus import Paragraph, Spacer, Image, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib.enums import TA_CENTER
from .report_config import ReportColors, ReportLayout, CompanyInfo, CAREFramework
from .report_styles import create_professional_styles

class ReportComponents:
    def __init__(self):
        self.styles = create_professional_styles()
        self.colors = ReportColors()
        self.layout = ReportLayout()
        self.company = CompanyInfo()
        self.care = CAREFramework()
    
    def create_header_table(self):
        """Create the main header table"""
        header_data = [[self.company.NAME, self.company.TAGLINE]]
        header_table = Table(header_data, colWidths=self.layout.HEADER_COLUMNS)
        header_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), self.colors.NAVY_BLUE),
            ("TEXTCOLOR", (0, 0), (-1, -1), self.colors.WHITE),
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
        return header_table
    
    def create_accent_line(self, width=500):
        """Create amber accent line"""
        accent_line = Table([[""]], colWidths=[width])
        accent_line.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), self.colors.AMBER),
            ("LINEBELOW", (0, 0), (-1, -1), 3, self.colors.AMBER),
        ]))
        return accent_line
    
    def create_logo(self):
        """Create logo image if available"""
        logo_path = "/app/reporting/assets/beaconai_logo.png" if os.getenv("DOCKER_ENV") else "reporting/assets/beaconai_logo.png"
        
        if os.path.exists(logo_path):
            return Image(logo_path, width=120, height=72)
        return None
    
    def create_executive_table(self, company_name, persona):
        """Create executive information table"""
        exec_data = [
            ["REPORT DETAILS", ""],
            ["Client Organization", company_name],
            ["Assessment Date", datetime.now().strftime('%B %d, %Y')],
            ["Stakeholder Role", persona],
            ["Assessment Framework", "CARE Diagnostic Model"],
            ["Prepared By", f"{self.company.NAME} AI Readiness Intelligence Engine"]
        ]
        
        exec_table = Table(exec_data, colWidths=self.layout.EXEC_TABLE_COLUMNS)
        exec_table.setStyle(TableStyle([
            # Header row
            ("BACKGROUND", (0, 0), (-1, 0), self.colors.NAVY_BLUE),
            ("TEXTCOLOR", (0, 0), (-1, 0), self.colors.WHITE),
            ("FONTNAME", (0, 0), (-1, 0), 'Helvetica-Bold'),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("SPAN", (0, 0), (1, 0)),
            ("ALIGN", (0, 0), (-1, 0), 'CENTER'),
            # Data rows
            ("BACKGROUND", (0, 1), (0, -1), self.colors.LIGHT_GRAY),
            ("FONTNAME", (0, 1), (0, -1), 'Helvetica-Bold'),
            ("FONTNAME", (1, 1), (1, -1), 'Helvetica'),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 1, self.colors.NAVY_BLUE),
            ("VALIGN", (0, 0), (-1, -1), 'MIDDLE'),
            ("LEFTPADDING", (0, 0), (-1, -1), 15),
            ("RIGHTPADDING", (0, 0), (-1, -1), 15),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]))
        return exec_table
    
    def create_methodology_bullets(self):
        """Create methodology bullet points"""
        bullets = []
        for dimension in self.care.DIMENSIONS:
            bullets.append(Paragraph(f"• {dimension}", self.styles['BulletPoint']))
        return bullets
    
    def create_next_steps_bullets(self):
        """Create next steps bullet points"""
        bullets = []
        for step in self.care.NEXT_STEPS:
            bullets.append(Paragraph(f"• {step}", self.styles['BulletPoint']))
        return bullets
    
    def create_contact_table(self):
        """Create contact information table"""
        contact_data = [
            [Paragraph(f"<b>{self.company.NAME.upper()} CONSULTING TEAM</b>", self.styles['ProfessionalBody']), ""],
            [Paragraph("<b>Email</b>", self.styles['ProfessionalBody']), 
             Paragraph(f'<a href="mailto:{self.company.EMAIL}" color="blue">{self.company.EMAIL}</a>', self.styles['ProfessionalBody'])],
            [Paragraph("<b>Phone</b>", self.styles['ProfessionalBody']), 
             Paragraph(f'<a href="tel:+13038774292" color="blue">{self.company.PHONE}</a>', self.styles['ProfessionalBody'])],
            [Paragraph("<b>Schedule Consultation</b>", self.styles['ProfessionalBody']), 
             Paragraph(f'<a href="{self.company.CONSULTATION_LINK}" color="blue"><u>Book Your Strategy Session →</u></a>', self.styles['ProfessionalBody'])],
            [Paragraph("<b>Website</b>", self.styles['ProfessionalBody']), 
             Paragraph(f'<a href="https://{self.company.WEBSITE}" color="blue">{self.company.WEBSITE}</a>', self.styles['ProfessionalBody'])]
        ]
        
        contact_table = Table(contact_data, colWidths=self.layout.CONTACT_TABLE_COLUMNS)
        contact_table.setStyle(TableStyle([
            # Header
            ("BACKGROUND", (0, 0), (-1, 0), self.colors.AMBER),
            ("TEXTCOLOR", (0, 0), (-1, 0), self.colors.WHITE),
            ("FONTNAME", (0, 0), (-1, 0), 'Helvetica-Bold'),
            ("FONTSIZE", (0, 0), (-1, 0), 12),
            ("SPAN", (0, 0), (1, 0)),
            ("ALIGN", (0, 0), (-1, 0), 'CENTER'),
            # Data rows
            ("BACKGROUND", (0, 1), (0, -1), self.colors.LIGHT_GRAY),
            ("FONTNAME", (0, 1), (0, -1), 'Helvetica-Bold'),
            ("FONTSIZE", (0, 1), (-1, -1), 10),
            ("GRID", (0, 0), (-1, -1), 1, self.colors.NAVY_BLUE),
            ("VALIGN", (0, 0), (-1, -1), 'MIDDLE'),
            ("LEFTPADDING", (0, 0), (-1, -1), 15),
            ("RIGHTPADDING", (0, 0), (-1, -1), 15),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
            ("ALIGN", (0, 0), (-1, -1), 'LEFT'),
            ("VALIGN", (0, 0), (-1, -1), 'TOP'),
        ]))
        return contact_table
    
    def create_footer_table(self):
        """Create footer table"""
        footer_data = [
            [self.company.COPYRIGHT, f"Generated: {datetime.now().strftime('%B %d, %Y')}"],
            [f"{self.company.EMAIL} | {self.company.PHONE}", self.company.TAGLINE]
        ]
        
        footer_table = Table(footer_data, colWidths=self.layout.FOOTER_COLUMNS)
        footer_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), self.colors.NAVY_BLUE),
            ("TEXTCOLOR", (0, 0), (-1, -1), self.colors.WHITE),
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
        return footer_table
    
    def create_separator_line(self, width=500):
        """Create separator line"""
        separator = Table([[""]], colWidths=[width])
        separator.setStyle(TableStyle([
            ("LINEBELOW", (0, 0), (-1, -1), 1, self.colors.LIGHT_GRAY),
        ]))
        return separator
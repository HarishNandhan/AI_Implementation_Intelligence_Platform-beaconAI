"""
Structured PDF Report Builder
"""
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate
from io import BytesIO

# Import structured components
from .report_config import ReportLayout
from .report_sections import ReportSections

class PDFReportBuilder:
    """Main PDF Report Builder using structured components"""
    
    def __init__(self):
        self.sections = ReportSections()
        self.layout = ReportLayout()
    
    def generate_pdf_report(self, company_name, persona, insights, solution_section, output_path=None):
        """Generate structured PDF report"""
        # Use Docker-aware path
        if output_path is None:
            output_path = "/app/generated_reports" if os.getenv("DOCKER_ENV") else "generated_reports"
        
        os.makedirs(output_path, exist_ok=True)
        filename = f"{company_name.replace(' ', '_')}_{persona}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        filepath = os.path.join(output_path, filename)
        
        # Create document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=self.layout.PAGE_SIZE,
            rightMargin=self.layout.MARGINS['right'],
            leftMargin=self.layout.MARGINS['left'],
            topMargin=self.layout.MARGINS['top'],
            bottomMargin=self.layout.MARGINS['bottom']
        )
        
        # Build story using structured sections
        story = []
        
        # Add all sections
        story.extend(self.sections.create_cover_page(company_name, persona))
        story.extend(self.sections.create_executive_summary(company_name))
        story.extend(self.sections.create_methodology_section())
        story.extend(self.sections.create_findings_section(insights))
        story.extend(self.sections.create_recommendations_section(solution_section))
        story.extend(self.sections.create_next_steps_section())
        
        # Build the PDF
        doc.build(story)
        return filepath
    
    def generate_pdf_to_buffer(self, company_name, persona, insights, solution_section):
        """Generate PDF report directly to memory buffer"""
        buffer = BytesIO()
        
        # Create document with buffer
        doc = SimpleDocTemplate(
            buffer,
            pagesize=self.layout.PAGE_SIZE,
            rightMargin=self.layout.MARGINS['right'],
            leftMargin=self.layout.MARGINS['left'],
            topMargin=self.layout.MARGINS['top'],
            bottomMargin=self.layout.MARGINS['bottom']
        )
        
        # Build story using structured sections
        story = []
        
        # Add all sections
        story.extend(self.sections.create_cover_page(company_name, persona))
        story.extend(self.sections.create_executive_summary(company_name))
        story.extend(self.sections.create_methodology_section())
        story.extend(self.sections.create_findings_section(insights))
        story.extend(self.sections.create_recommendations_section(solution_section))
        story.extend(self.sections.create_next_steps_section())
        
        # Build the PDF
        doc.build(story)
        
        # Get PDF content
        pdf_content = buffer.getvalue()
        buffer.close()
        
        return pdf_content


# Create global instance for backward compatibility
_builder = PDFReportBuilder()

# Export functions for backward compatibility
def generate_pdf_report(company_name, persona, insights, solution_section, output_path=None):
    """Generate PDF report (backward compatibility function)"""
    return _builder.generate_pdf_report(company_name, persona, insights, solution_section, output_path)

def generate_pdf_to_buffer(company_name, persona, insights, solution_section):
    """Generate PDF report to buffer (backward compatibility function)"""
    return _builder.generate_pdf_to_buffer(company_name, persona, insights, solution_section)

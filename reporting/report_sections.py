"""
Report Sections - Individual report sections
"""
from reportlab.platypus import Paragraph, Spacer, PageBreak, KeepTogether
from .report_components import ReportComponents
from .report_config import CAREFramework

class ReportSections:
    def __init__(self):
        self.components = ReportComponents()
        self.styles = self.components.styles
        self.care = CAREFramework()
    
    def create_cover_page(self, company_name, persona):
        """Create the cover page"""
        story = []
        
        # Header
        story.append(self.components.create_header_table())
        
        # Amber accent line
        story.append(self.components.create_accent_line(480))
        story.append(Spacer(1, 30))
        
        # Logo
        logo = self.components.create_logo()
        if logo:
            story.append(logo)
            story.append(Spacer(1, 40))
        
        # Main Title
        story.append(Paragraph("AI READINESS ASSESSMENT REPORT", self.styles['MainTitle']))
        story.append(Spacer(1, 30))
        
        # Company Name
        story.append(Paragraph(f"<b>{company_name.upper()}</b>", self.styles['CompanyName']))
        
        # Executive Information Table
        story.append(self.components.create_executive_table(company_name, persona))
        story.append(PageBreak())
        
        return story
    
    def create_executive_summary(self, company_name):
        """Create executive summary section"""
        story = []
        
        # Section Header
        story.append(Paragraph("EXECUTIVE SUMMARY", self.styles['SectionHeader']))
        story.append(self.components.create_accent_line())
        story.append(Spacer(1, 20))
        
        # Summary Text
        summary_text = f"""
        This comprehensive AI readiness assessment evaluates {company_name}'s current position and strategic opportunities 
        for artificial intelligence implementation. Through our proprietary CARE diagnostic framework (Culture, 
        Adoption, Readiness, and Evolution), we have identified key insights and actionable recommendations to accelerate 
        your organization's AI transformation journey.
        
        The assessment reveals specific areas of strength and opportunities for improvement, providing a clear roadmap 
        for successful AI adoption aligned with your business objectives and operational capabilities.
        """
        
        story.append(Paragraph(summary_text, self.styles['ExecutiveSummary']))
        story.append(Spacer(1, 30))
        
        return story
    
    def create_methodology_section(self):
        """Create assessment methodology section"""
        story = []
        
        # Section Header
        story.append(Paragraph("ASSESSMENT METHODOLOGY", self.styles['SectionHeader']))
        story.append(self.components.create_accent_line())
        story.append(Spacer(1, 20))
        
        # Methodology Introduction
        methodology_text = """
        Our CARE diagnostic framework provides a structured approach to evaluating AI readiness across four critical dimensions:
        """
        story.append(Paragraph(methodology_text, self.styles['ProfessionalBody']))
        story.append(Spacer(1, 15))
        
        # Add methodology bullets
        story.extend(self.components.create_methodology_bullets())
        story.append(PageBreak())
        
        return story
    
    def create_findings_section(self, insights):
        """Create detailed findings section"""
        story = []
        
        # Section Header
        story.append(Paragraph("DETAILED ASSESSMENT FINDINGS", self.styles['SectionHeader']))
        story.append(self.components.create_accent_line())
        story.append(Spacer(1, 10))
        
        # Process each category
        for category_key, category_name in self.care.CATEGORIES.items():
            category_insights = {k: v for k, v in insights.items() if k.startswith(category_key)}
            
            if category_insights:
                category_content = self._create_category_content(category_key, category_name, category_insights)
                
                # Keep smaller categories together
                if len(category_insights) <= 2:
                    story.append(KeepTogether(category_content))
                else:
                    # For larger categories, keep header with first item
                    header_with_first = category_content[:6]
                    story.append(KeepTogether(header_with_first))
                    
                    # Add remaining items
                    remaining_content = category_content[6:]
                    story.extend(remaining_content)
                
                # Add space between categories
                story.append(Spacer(1, 20))
        
        story.append(PageBreak())
        return story
    
    def _create_category_content(self, category_key, category_name, category_insights):
        """Create content for a single category"""
        content = []
        
        # Category header
        content.append(Paragraph(f"{category_name} ASSESSMENT", self.styles['SubsectionHeader']))
        content.append(Spacer(1, 10))
        
        # Process each insight
        insight_items = list(category_insights.items())
        for i, (qid, insight_data) in enumerate(insight_items):
            # Question header
            content.append(Paragraph(
                f"Assessment Item {qid}: {insight_data.get('question')}", 
                self.styles['QuestionHeader']
            ))
            
            # Response
            content.append(Paragraph(
                f"<b>Response:</b> {insight_data.get('answer')}", 
                self.styles['Response']
            ))
            
            # Strategic Analysis
            content.append(Paragraph(
                f"<b>Strategic Analysis:</b> {insight_data.get('insight')}", 
                self.styles['Analysis']
            ))
            
            # Add separator (except for last item)
            if i < len(insight_items) - 1:
                content.append(self.components.create_separator_line())
                content.append(Spacer(1, 15))
        
        return content
    
    def create_recommendations_section(self, solution_section):
        """Create strategic recommendations section"""
        story = []
        
        # Section Header
        story.append(Paragraph("STRATEGIC RECOMMENDATIONS", self.styles['SectionHeader']))
        story.append(self.components.create_accent_line())
        story.append(Spacer(1, 10))
        
        # Solution content
        story.append(Paragraph(solution_section, self.styles['Solution']))
        story.append(Spacer(1, 30))
        
        return story
    
    def create_next_steps_section(self):
        """Create next steps and engagement section"""
        story = []
        
        # Section Header
        story.append(Paragraph("NEXT STEPS & ENGAGEMENT", self.styles['SectionHeader']))
        story.append(self.components.create_accent_line())
        story.append(Spacer(1, 10))
        
        # Introduction
        intro_text = "Based on this assessment, we recommend scheduling a strategic consultation to discuss:"
        story.append(Paragraph(intro_text, self.styles['ProfessionalBody']))
        story.append(Spacer(1, 15))
        
        # Next steps bullets
        story.extend(self.components.create_next_steps_bullets())
        story.append(Spacer(1, 15))
        
        # Conclusion
        conclusion_text = "Our team is ready to partner with you in transforming these insights into actionable results."
        story.append(Paragraph(conclusion_text, self.styles['ProfessionalBody']))
        story.append(Spacer(1, 20))
        
        # Call-to-Action
        story.append(Paragraph("Ready to Transform Your AI Strategy?", self.styles['CallToAction']))
        story.append(Spacer(1, 20))
        
        # Contact Information
        story.append(KeepTogether([self.components.create_contact_table()]))
        story.append(Spacer(1, 30))
        
        # Footer
        story.append(self.components.create_footer_table())
        
        return story
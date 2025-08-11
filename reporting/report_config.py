"""
Report Configuration and Constants
"""
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4

# Visual Identity Colors
class ReportColors:
    NAVY_BLUE = colors.Color(0.04, 0.19, 0.38)  # #0A3161
    AMBER = colors.Color(1.0, 0.65, 0.0)        # #FFA500
    TEAL = colors.Color(0.0, 0.5, 0.5)          # #008080
    LIGHT_GRAY = colors.Color(0.95, 0.95, 0.95)
    WHITE = colors.white
    BLACK = colors.black

# Report Layout Configuration
class ReportLayout:
    PAGE_SIZE = A4
    MARGINS = {
        'top': 40,
        'bottom': 40,
        'left': 40,
        'right': 40
    }
    
    # Column widths for tables
    HEADER_COLUMNS = [200, 280]
    EXEC_TABLE_COLUMNS = [150, 300]
    CONTACT_TABLE_COLUMNS = [160, 260]
    FOOTER_COLUMNS = [280, 200]
    
    # Spacing constants
    SECTION_SPACING = 30
    SUBSECTION_SPACING = 20
    PARAGRAPH_SPACING = 15

# Company Information
class CompanyInfo:
    NAME = "beaconAI"
    TAGLINE = "AI Implementation Intelligence Platform"
    EMAIL = "info@beaconai.ai"
    PHONE = "+1 (303) 877-4292"
    WEBSITE = "www.beaconai.ai"
    CONSULTATION_LINK = "https://app.usemotion.com/meet/dalemyska/linkedin"
    COPYRIGHT = "© 2025 beaconAI. All rights reserved."

# CARE Framework Categories
class CAREFramework:
    CATEGORIES = {
        'C': 'CULTURE',
        'A': 'ADOPTION', 
        'R': 'READINESS',
        'E': 'EVOLUTION'
    }
    
    DIMENSIONS = [
        ("<b>Culture:</b> Organizational mindset, change readiness, and cultural alignment with AI adoption"),
        ("<b>Adoption:</b> Strategic vision, leadership commitment, and implementation approach"),
        ("<b>Readiness:</b> Technical infrastructure, data maturity, and existing technology capabilities"),
        ("<b>Evolution:</b> Long-term planning, scalability considerations, and continuous improvement frameworks")
    ]
    
    NEXT_STEPS = [
        "Detailed implementation roadmap and timeline",
        "Resource allocation and investment planning",
        "Technology stack recommendations and vendor selection",
        "Change management and training programs",
        "Success metrics and performance monitoring frameworks"
    ]
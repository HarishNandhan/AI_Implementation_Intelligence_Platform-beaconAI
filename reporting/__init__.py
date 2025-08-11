"""
BeaconAI Report Generation Module
"""
from .pdf_builder import generate_pdf_report, generate_pdf_to_buffer, PDFReportBuilder
from .report_config import ReportColors, ReportLayout, CompanyInfo, CAREFramework
from .report_styles import create_professional_styles
from .report_components import ReportComponents
from .report_sections import ReportSections

__all__ = [
    'generate_pdf_report',
    'generate_pdf_to_buffer', 
    'PDFReportBuilder',
    'ReportColors',
    'ReportLayout',
    'CompanyInfo',
    'CAREFramework',
    'create_professional_styles',
    'ReportComponents',
    'ReportSections'
]
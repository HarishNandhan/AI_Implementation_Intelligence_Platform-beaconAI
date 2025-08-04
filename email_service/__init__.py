"""
BeaconAI Email Service Package

This package handles email sending functionality using Mailgun API.
"""

from .mailgun_client import MailgunClient

__all__ = ['MailgunClient']
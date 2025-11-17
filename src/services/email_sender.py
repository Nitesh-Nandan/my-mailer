#!/usr/bin/env python3
"""
Email sending service using Gmail SMTP.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
from dotenv import load_dotenv

load_dotenv()


class EmailSender:
    """A class to handle email sending via Gmail SMTP."""
    
    def __init__(self, username: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize EmailSender for Gmail.
        
        Args:
            username: Gmail address (from EMAIL_USERNAME env var if not provided)
            password: Gmail app password (from EMAIL_PASSWORD env var if not provided)
        """
        self.username = username or os.getenv('EMAIL_USERNAME')
        self.password = password or os.getenv('EMAIL_PASSWORD')
        self.smtp_host = 'smtp.gmail.com'
        self.smtp_port = 587
        self.recipient_email = os.getenv('RECIPIENT_EMAIL', self.username)
    
    def send_email(
        self,
        subject: str,
        html_body: str,
        text_body: str,
        reply_to: Optional[str] = None
    ) -> bool:
        """
        Send an email with both HTML and plain text versions.
        
        Args:
            subject: Email subject
            html_body: HTML email body
            text_body: Plain text email body
            reply_to: Reply-to email address
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.username or not self.password:
            print("✗ Email credentials not configured")
            return False
        
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = f"My Website <{self.username}>"
            msg['To'] = self.recipient_email
            msg['Subject'] = subject
            
            if reply_to:
                msg['Reply-To'] = reply_to
            
            # Attach both plain text and HTML versions
            part1 = MIMEText(text_body, 'plain')
            part2 = MIMEText(html_body, 'html')
            msg.attach(part1)
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            print(f"✓ Email sent successfully to {self.recipient_email}")
            return True
            
        except Exception as e:
            print(f"✗ Failed to send email: {str(e)}")
            return False
    
    def is_configured(self) -> bool:
        """
        Check if email credentials are configured.
        
        Returns:
            True if credentials are set, False otherwise
        """
        return bool(self.username and self.password)


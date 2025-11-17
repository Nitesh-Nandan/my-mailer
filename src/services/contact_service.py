#!/usr/bin/env python3
"""
Contact form service for handling submissions and notifications.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Tuple
from .email_sender import EmailSender


class ContactService:
    """Service for handling contact form submissions."""
    
    def __init__(self, data_dir: str = "contact_submissions"):
        """
        Initialize ContactService.
        
        Args:
            data_dir: Directory to store contact submissions
        """
        self.data_dir = data_dir
        self.email_sender = EmailSender()
        self.template_dir = Path(__file__).parent.parent / "email_templates"
        
        # Create data directory if it doesn't exist
        os.makedirs(self.data_dir, exist_ok=True)
    
    def process_submission(
        self,
        name: str,
        email: str,
        subject: str,
        message: str,
        ip_address: str = "Unknown"
    ) -> Tuple[bool, Dict]:
        """
        Process a contact form submission.
        
        Args:
            name: Sender's name
            email: Sender's email
            subject: Message subject
            message: Message content
            ip_address: Sender's IP address
            
        Returns:
            Tuple of (success, result_dict)
        """
        try:
            # Create submission object with IST timezone
            from datetime import timezone, timedelta
            ist = timezone(timedelta(hours=5, minutes=30))
            submission = {
                'name': name,
                'email': email,
                'subject': subject,
                'message': message,
                'timestamp': datetime.now(ist).isoformat(),
                'ip_address': ip_address
            }
            
            # Save to file
            submission_id = self._save_submission(submission)
            
            # Send email notification
            email_sent = self._send_notification(submission)
            
            return True, {
                'success': True,
                'message': 'Thank you for your message! We will get back to you soon.',
                'submission_id': submission_id,
                'email_sent': email_sent
            }
            
        except Exception as e:
            return False, {
                'success': False,
                'error': f'Failed to process submission: {str(e)}'
            }
    
    def _save_submission(self, submission: Dict) -> str:
        """
        Save submission to JSON file.
        
        Args:
            submission: Submission data dictionary
            
        Returns:
            Submission ID (filename without extension)
        """
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}.json"
        filepath = os.path.join(self.data_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(submission, f, indent=2)
        
        return filename.replace('.json', '')
    
    def _send_notification(self, submission: Dict) -> bool:
        """
        Send email notification for the submission.
        
        Args:
            submission: Submission data dictionary
            
        Returns:
            True if email sent successfully, False otherwise
        """
        if not self.email_sender.is_configured():
            print("⚠️  Email not configured - skipping notification")
            return False
        
        # Load and populate template
        html_body = self._render_template('contact_form.html', submission)
        text_body = self._create_text_body(submission)
        
        # Send email
        email_subject = f"New Contact Form: {submission.get('subject', 'No Subject')}"
        return self.email_sender.send_email(
            subject=email_subject,
            html_body=html_body,
            text_body=text_body,
            reply_to=submission.get('email')
        )
    
    def _render_template(self, template_name: str, data: Dict) -> str:
        """
        Render an email template with data.
        
        Args:
            template_name: Name of the template file
            data: Data to populate the template
            
        Returns:
            Rendered HTML string
        """
        template_path = self.template_dir / template_name
        
        with open(template_path, 'r') as f:
            template = f.read()
        
        # Format timestamp to be human readable in IST
        timestamp_str = data.get('timestamp', 'Unknown')
        if timestamp_str != 'Unknown':
            try:
                from datetime import datetime, timezone, timedelta
                dt = datetime.fromisoformat(timestamp_str)
                # Convert to IST (UTC+5:30)
                ist = timezone(timedelta(hours=5, minutes=30))
                dt_ist = dt.astimezone(ist)
                timestamp_str = dt_ist.strftime('%B %d, %Y at %I:%M %p IST')
            except:
                pass  # Keep original if parsing fails
        
        # Use simple string replacement to avoid conflicts with CSS braces
        replacements = {
            '{name}': data.get('name', 'Unknown'),
            '{email}': data.get('email', 'Unknown'),
            '{subject}': data.get('subject', 'No Subject'),
            '{message}': data.get('message', 'No message provided'),
            '{timestamp}': timestamp_str,
            '{ip_address}': data.get('ip_address', 'Unknown')
        }
        
        for placeholder, value in replacements.items():
            template = template.replace(placeholder, str(value))
        
        return template
    
    def _create_text_body(self, submission: Dict) -> str:
        """
        Create plain text email body.
        
        Args:
            submission: Submission data dictionary
            
        Returns:
            Plain text email body
        """
        # Format timestamp to be human readable in IST
        timestamp_str = submission.get('timestamp', 'Unknown')
        if timestamp_str != 'Unknown':
            try:
                from datetime import datetime, timezone, timedelta
                dt = datetime.fromisoformat(timestamp_str)
                # Convert to IST (UTC+5:30)
                ist = timezone(timedelta(hours=5, minutes=30))
                dt_ist = dt.astimezone(ist)
                timestamp_str = dt_ist.strftime('%B %d, %Y at %I:%M %p IST')
            except:
                pass
        
        return f"""
New Contact Form Submission

From: {submission.get('name', 'Unknown')}
Email: {submission.get('email', 'Unknown')}
Subject: {submission.get('subject', 'No Subject')}

Message:
{submission.get('message', 'No message provided')}

---
Submitted: {timestamp_str}
IP Address: {submission.get('ip_address', 'Unknown')}
"""


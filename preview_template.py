#!/usr/bin/env python3
"""
Script to preview email templates in the browser.
Usage: python preview_template.py
"""

from pathlib import Path
from datetime import datetime
import webbrowser
import tempfile

def preview_contact_form_template():
    """Generate and open preview of the contact form email template."""
    
    # Load the template
    template_path = Path(__file__).parent / "src" / "email_templates" / "contact_form.html"
    
    with open(template_path, 'r') as f:
        template = f.read()
    
    # Sample data
    sample_data = {
        'name': 'John Doe',
        'email': 'john.doe@example.com',
        'subject': 'Inquiry About Your Services',
        'message': '''Hello,

I came across your website and I'm very interested in learning more about your services. I have a project that I think would be a great fit for your expertise.

Could we schedule a call this week to discuss the details?

Looking forward to hearing from you!

Best regards,
John''',
        'timestamp': datetime.now().strftime('%B %d, %Y at %I:%M %p IST'),
        'ip_address': '192.168.1.100'
    }
    
    # Render the template (simple string replacement to avoid CSS brace conflicts)
    rendered_html = template
    for key, value in sample_data.items():
        rendered_html = rendered_html.replace(f'{{{key}}}', str(value))
    
    # Wrap in a container for better preview
    preview_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contact Form Email Preview</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            background-color: #e5e5e5;
            margin: 0;
            padding: 20px;
        }}
        .preview-note {{
            background: #fff3cd;
            border: 2px solid #ffc107;
            padding: 15px;
            border-radius: 8px;
            margin: 0 auto 20px;
            text-align: center;
            max-width: 600px;
        }}
        .email-container {{
            max-width: 600px;
            margin: 0 auto;
            background: white;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <div class="preview-note">
        <h3 style="margin: 0 0 10px 0;">📧 Email Template Preview</h3>
        <p style="margin: 0; font-size: 14px;">This is how your contact form notification email will appear</p>
        <p style="margin: 10px 0 0 0; font-size: 12px; color: #666;">
            Template: <code>src/email_templates/contact_form.html</code>
        </p>
    </div>

    <div class="email-container">
        {rendered_html}
    </div>
</body>
</html>
"""
    
    # Save to temporary file and open in browser
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
        f.write(preview_html)
        temp_path = f.name
    
    print(f"✓ Preview generated: {temp_path}")
    print(f"🌐 Opening in browser...")
    
    # Open in default browser
    webbrowser.open(f'file://{temp_path}')
    
    print(f"✓ Preview opened in browser!")
    print(f"\nNote: The temporary file will remain at: {temp_path}")
    print(f"You can delete it manually or it will be cleaned up by the system.")

if __name__ == "__main__":
    preview_contact_form_template()


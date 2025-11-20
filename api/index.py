"""
Vercel Serverless Function for My Mailer API
This file contains the complete Flask app for Vercel deployment
"""
import os
import sys
from pathlib import Path

# Setup paths for imports
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.insert(0, str(parent_dir))

# Now import everything we need
from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
from flasgger import Swagger
from datetime import datetime, timezone, timedelta
from src.services.contact_service import ContactService

# Create Flask app
app = Flask(__name__)

# CORS Configuration - allow your portfolio domain
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://my-portfolio-git-main-nitesh-nandans-projects.vercel.app",
            "https://www.niteshnandan.in"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

# Swagger configuration
app.config['SWAGGER'] = {
    'title': 'My Mailer API',
    'version': '0.1.0',
    'description': 'Contact form API with email notifications',
    'uiversion': 3
}
Swagger(app)

# Initialize services
contact_service = ContactService()


@app.route('/api/contact', methods=['POST'])
def contact_me():
    """Submit contact form
    ---
    tags:
      - Contact
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - name
            - email
            - subject
            - message
          properties:
            name:
              type: string
              example: John Doe
            email:
              type: string
              example: john.doe@example.com
            subject:
              type: string
              example: Inquiry About Services
            message:
              type: string
              example: I would like to know more about your services
    responses:
      201:
        description: Success
      400:
        description: Validation error
      500:
        description: Server error
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'No data provided'}), 400
        
        # Validate
        required = ['name', 'email', 'subject', 'message']
        missing = [f for f in required if not data.get(f)]
        if missing:
            return jsonify({'success': False, 'error': f"Missing: {', '.join(missing)}"}), 400
        
        # Clean data
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
        
        # Validate email
        if '@' not in email or '.' not in email:
            return jsonify({'success': False, 'error': 'Invalid email'}), 400
        
        # Process
        success, result = contact_service.process_submission(
            name=name,
            email=email,
            subject=subject,
            message=message,
            ip_address=request.remote_addr or 'Unknown'
        )
        
        return jsonify(result), 201 if success else 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/hello', methods=['GET'])
def hello_world():
    """Hello World
    ---
    tags:
      - Utilities
    responses:
      200:
        description: Success
    """
    return jsonify({
        'message': 'Hello World! 👋',
        'status': 'success',
        'service': 'my-mailer',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check
    ---
    tags:
      - Utilities
    responses:
      200:
        description: Healthy
    """
    return jsonify({
        'status': 'healthy',
        'service': 'my-mailer',
        'timestamp': datetime.now().isoformat()
    })


@app.route('/')
def home():
    """Redirect to API docs"""
    return redirect('/apidocs')

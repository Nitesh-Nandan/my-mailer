from flask import Flask, request, jsonify
from flask_cors import CORS
from flasgger import Swagger
from datetime import datetime
import os
from src.services import ContactService

app = Flask(__name__)
CORS(app)

# Note: The 'app' variable is used by Vercel for serverless deployment

# Simple Swagger configuration
app.config['SWAGGER'] = {
    'title': 'My Mailer API',
    'version': '0.1.0',
    'description': 'A simple REST API for contact form submissions with email notifications',
    'uiversion': 3
}
Swagger(app)

# Initialize contact service
contact_service = ContactService()


@app.route('/api/contact', methods=['POST'])
def contact_me():
    """Submit a contact form message
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
              example: I would like to know more about your services.
    responses:
      201:
        description: Contact form submitted successfully
      400:
        description: Validation error
      500:
        description: Server error
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'subject', 'message']
        missing_fields = [field for field in required_fields if not data.get(field)]
        
        if missing_fields:
            return jsonify({'success': False, 'error': f"Missing required fields: {', '.join(missing_fields)}"}), 400
        
        # Extract and clean form data
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
        
        # Basic email validation
        if '@' not in email or '.' not in email:
            return jsonify({'success': False, 'error': 'Invalid email address'}), 400
        
        # Process submission
        success, result = contact_service.process_submission(
            name=name, email=email, subject=subject, message=message,
            ip_address=request.remote_addr or 'Unknown'
        )
        
        return jsonify(result), 201 if success else 500
        
    except Exception as e:
        return jsonify({'success': False, 'error': f'Server error: {str(e)}'}), 500


@app.route('/api/hello', methods=['GET'])
def hello_world():
    """Hello World test endpoint
    ---
    tags:
      - Utilities
    responses:
      200:
        description: Hello World message
    """
    return jsonify({
        'message': 'Hello World! 👋',
        'status': 'success',
        'service': 'my-mailer',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint
    ---
    tags:
      - Utilities
    responses:
      200:
        description: Service health status
    """
    return jsonify({
        'status': 'healthy',
        'service': 'my-mailer',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/')
def home():
    """Root endpoint - redirects to Swagger docs"""
    from flask import redirect
    return redirect('/apidocs')


def main():
    """Run the Flask application"""
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    print(f"\n{'='*55}")
    print(f"🚀 My Mailer API")
    print(f"{'='*55}")
    print(f"📚 Swagger:     http://localhost:{port}/apidocs")
    print(f"📧 Contact:     http://localhost:{port}/api/contact")
    print(f"👋 Hello:       http://localhost:{port}/api/hello")
    print(f"💚 Health:      http://localhost:{port}/api/health")
    print(f"{'='*55}")
    
    if contact_service.email_sender.is_configured():
        print(f"✉️  Email: ENABLED ✓")
    else:
        print(f"⚠️  Email: DISABLED")
    print(f"{'='*55}\n")
    
    app.run(host='0.0.0.0', port=port, debug=debug)


if __name__ == "__main__":
    main()

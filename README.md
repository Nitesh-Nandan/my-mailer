# My Mailer API

A simple Flask REST API for handling contact form submissions.

## Features

- 📧 Contact form API endpoint
- 📚 **Swagger UI documentation** at `/apidocs`
- 👋 Hello World endpoint for deployment testing
- 💾 Saves submissions to local JSON files
- ✉️ Email notifications via Gmail SMTP
- ✅ Input validation
- 🔒 CORS enabled
- 🎨 Beautiful HTML email templates

## Setup

### 1. Install Dependencies

Using `uv` (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

### 2. Run the Application

```bash
# Using uv (recommended)
uv run python main.py

# Or activate the virtual environment first
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
python main.py
```

The server will start on `http://localhost:8000`

## 📚 Swagger Documentation

Interactive API documentation is available at **http://localhost:8000/apidocs**

Features:
- 🧪 Test all endpoints directly from browser
- 📖 View request/response schemas
- ✅ Pre-filled example values
- 🎨 Clean, interactive UI

## API Endpoints

### 🧪 Test Endpoints

#### GET `/api/hello`
Simple Hello World endpoint to verify deployment.

**Response:**
```json
{
  "message": "Hello World! 👋",
  "status": "success",
  "service": "my-mailer",
  "timestamp": "2025-11-17T12:00:00.000000"
}
```

**Test with curl:**
```bash
curl http://localhost:5000/api/hello
```

#### GET `/api/health`
Health check endpoint.

**Response:**
```json
{
  "status": "healthy",
  "service": "my-mailer",
  "timestamp": "2025-11-17T12:00:00.000000"
}
```

### 📬 Contact Form Endpoint

#### POST `/api/contact`
Submit a contact form message.

**Request Body:**
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "subject": "Project Inquiry",
  "message": "I would like to discuss a project..."
}
```

**Success Response (201):**
```json
{
  "success": true,
  "message": "Thank you for your message! We will get back to you soon.",
  "submission_id": "20251117_120000_123456",
  "email_sent": true
}
```

**Note:** `email_sent` will be `true` if email notification was sent successfully, `false` if email credentials are not configured or sending failed.

**Error Response (400):**
```json
{
  "success": false,
  "error": "Missing required fields: name, email"
}
```

**Test with curl:**
```bash
curl -X POST http://localhost:5000/api/contact \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "subject": "Test Subject",
    "message": "This is a test message"
  }'
```

## Configuration

### Environment Variables

Create a `.env` file in the project root (copy from `config.example`):

```bash
cp config.example .env
```

Then edit `.env` with your settings:

```env
# Flask Configuration
PORT=5000
DEBUG=True

# Email Configuration (Gmail)
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-gmail-app-password
RECIPIENT_EMAIL=nitesh.nandan.ai@gmail.com
```

### Gmail Setup for Email Notifications

1. **Enable 2-Factor Authentication** on your Gmail account
   - Go to: https://myaccount.google.com/security

2. **Generate App Password**
   - Visit: https://myaccount.google.com/apppasswords
   - Select "Mail" and your device
   - Copy the 16-character password

3. **Add to .env file**
   ```env
   EMAIL_USERNAME=your-email@gmail.com
   EMAIL_PASSWORD=abcd efgh ijkl mnop  # 16-char app password
   RECIPIENT_EMAIL=where-to-receive@email.com
   ```

### Running with Configuration

```bash
# Using .env file (recommended)
python main.py

# Or set environment variables directly
export PORT=8080
export DEBUG=True
export EMAIL_USERNAME=your-email@gmail.com
export EMAIL_PASSWORD=your-app-password
python main.py
```

## Project Structure

```
my-mailer/
├── src/
│   ├── services/
│   │   ├── email_sender.py      # Email sending service via SMTP
│   │   └── contact_service.py   # Contact form business logic
│   └── email_templates/
│       └── contact_form.html    # HTML email template
├── main.py                       # Flask application (controller)
├── pyproject.toml                # Project dependencies
├── config.example                # Environment variable template
└── contact_submissions/          # Stored form submissions (gitignored)
```

## Architecture

- **Controller** (`main.py`): Flask routes and request handling
- **Services** (`src/services/`):
  - `ContactService`: Orchestrates submission processing, storage, and notifications
  - `EmailSender`: Handles SMTP email sending via Gmail
- **Templates** (`src/email_templates/`): HTML email templates

## Data Storage

Contact submissions are **sent via email only** - no local file storage. This makes the app perfect for serverless deployment on platforms like Vercel.

For local development, you can optionally add file storage back if needed.

## Development

To run in debug mode:
```bash
DEBUG=True python main.py
```

## 🚀 Deployment

### Deploy to Vercel

This project is configured for easy deployment to Vercel:

1. Push to GitHub
2. Import to Vercel Dashboard
3. Set environment variables
4. Deploy!

See **[DEPLOYMENT.md](DEPLOYMENT.md)** for detailed deployment instructions.

### Quick Deploy Button

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/Nitesh-Nandan/my-mailer)

**Note:** This app is optimized for Vercel - contact submissions are sent via email only (no file storage needed).

## License

MIT


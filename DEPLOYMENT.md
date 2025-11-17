# Deployment Guide

## 🚀 Deploy to Vercel

### Prerequisites
- [Vercel Account](https://vercel.com/signup)
- [Vercel CLI](https://vercel.com/cli) (optional, for CLI deployment)
- GitHub repository (for automatic deployments)

### Method 1: Deploy via Vercel Dashboard (Recommended)

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Add Vercel configuration"
   git push origin main
   ```

2. **Import to Vercel:**
   - Go to [Vercel Dashboard](https://vercel.com/new)
   - Click "Import Project"
   - Select your `my-mailer` repository
   - Click "Import"

3. **Configure Environment Variables:**
   In the Vercel project settings, add these environment variables:
   ```
   EMAIL_USERNAME=your-email@gmail.com
   EMAIL_PASSWORD=your-gmail-app-password
   RECIPIENT_EMAIL=nitesh.nandan.ai@gmail.com
   PORT=8000
   DEBUG=False
   ```

4. **Deploy:**
   - Click "Deploy"
   - Wait for deployment to complete
   - Your API will be live at `https://your-project.vercel.app`

### Method 2: Deploy via Vercel CLI

1. **Install Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel:**
   ```bash
   vercel login
   ```

3. **Deploy:**
   ```bash
   vercel
   ```
   
4. **Set Environment Variables:**
   ```bash
   vercel env add EMAIL_USERNAME
   vercel env add EMAIL_PASSWORD
   vercel env add RECIPIENT_EMAIL
   ```

5. **Deploy to Production:**
   ```bash
   vercel --prod
   ```

### 🔧 Vercel Configuration Files

- **`vercel.json`** - Vercel build and routing configuration
- **`requirements.txt`** - Python dependencies for Vercel
- **`.vercelignore`** - Files to exclude from deployment

### 📋 After Deployment

Your API will be available at:
- **Swagger Docs:** `https://your-project.vercel.app/apidocs`
- **Contact API:** `https://your-project.vercel.app/api/contact`
- **Hello API:** `https://your-project.vercel.app/api/hello`
- **Health Check:** `https://your-project.vercel.app/api/health`

### 🧪 Test Your Deployment

```bash
# Replace with your actual Vercel URL
curl -X POST "https://your-project.vercel.app/api/contact" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "subject": "Testing Vercel Deployment",
    "message": "This is a test message!"
  }'
```

### ⚠️ Important Notes

#### File Storage Limitation
Vercel uses **serverless functions**, which means:
- ❌ Files saved to `contact_submissions/` **won't persist** between requests
- ✅ Email notifications will work fine
- 📝 For production, consider:
  - Using a database (PostgreSQL, MongoDB, Supabase)
  - Cloud storage (AWS S3, Cloudflare R2)
  - Or removing file storage entirely (rely only on emails)

#### Environment Variables
- Set all environment variables in Vercel Dashboard
- Never commit `.env` file to Git
- Email credentials must be configured for notifications to work

#### Cold Starts
- First request after inactivity may be slower (1-2 seconds)
- Subsequent requests will be fast

### 🔄 Automatic Deployments

Once connected to GitHub:
- Push to `main` branch → Auto-deploy to production
- Push to other branches → Preview deployments
- Pull requests → Preview deployments with unique URLs

### 🐛 Troubleshooting

#### Deployment Fails
- Check build logs in Vercel Dashboard
- Ensure `requirements.txt` has all dependencies
- Verify Python version compatibility (3.12)

#### Email Not Sending
- Verify environment variables are set in Vercel
- Check Gmail App Password is valid
- View function logs in Vercel Dashboard

#### 404 Errors
- Check `vercel.json` routing configuration
- Ensure main.py exports `app` at module level

### 📚 Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
- [Vercel CLI Documentation](https://vercel.com/docs/cli)

### 🎯 Next Steps

After successful deployment:
1. ✅ Test all endpoints
2. ✅ Verify email notifications work
3. ✅ Update frontend to use new API URL
4. ✅ Set up custom domain (optional)
5. ✅ Monitor function usage in Vercel Dashboard


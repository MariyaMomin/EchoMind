# 🚀 EchoMind Deployment Guide

This guide will help you deploy EchoMind to the internet using **Render** (backend) and **Vercel** (frontend).

## Prerequisites

- GitHub account
- Git installed on your computer
- GitHub repository for this project

---

## Part 1: Prepare Your Code

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Create a new repository named `echomind`
3. Make it **Public** (required for free tier)
4. Don't initialize with README (we already have files)

### Step 2: Push Code to GitHub

Open PowerShell in your project directory:

```powershell
cd C:\Users\Mariya\Documents\dev\echomind

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: EchoMind mental wellness platform"

# Add your GitHub repository as remote (replace with your username)
git remote add origin https://github.com/YOUR_USERNAME/echomind.git

# Push to GitHub
git branch -M main
git push -u origin main
```

**✅ Your code is now on GitHub!**

---

## Part 2: Deploy Backend to Render

### Step 1: Create Render Account

1. Go to https://render.com
2. Click "Get Started" or "Sign Up"
3. Sign up with your GitHub account (easiest option)

### Step 2: Deploy Backend Service

1. **Click "New +"** in the dashboard
2. Select **"Web Service"**
3. Connect your GitHub account if prompted
4. Select your **`echomind`** repository
5. Configure the service:

**Basic Settings:**
- **Name:** `echomind-backend` (or any name you prefer)
- **Region:** Choose closest to you
- **Branch:** `main`
- **Root Directory:** `backend`
- **Runtime:** `Python 3`
- **Build Command:** 
  ```
  pip install -r requirements.txt && python -m spacy download en_core_web_sm
  ```
- **Start Command:** 
  ```
  python -m app.main
  ```

**Environment Variables** (click "Advanced" then "Add Environment Variable"):
Add these one by one:

| Key | Value |
|-----|-------|
| `API_HOST` | `0.0.0.0` |
| `API_PORT` | `8000` |
| `ENVIRONMENT` | `production` |
| `CHROMA_PERSIST_DIR` | `/opt/render/project/src/data/chromadb` |
| `SECRET_KEY` | (click "Generate" to auto-create) |
| `CORS_ORIGINS` | `*` (temporarily allow all, we'll update this) |

**Plan:**
- Select **"Free"** plan

6. Click **"Create Web Service"**

### Step 3: Wait for Deployment

- First deployment takes 5-10 minutes
- Watch the logs in real-time
- You'll see: "Installing dependencies..." → "Starting server..." → "Live ✅"

### Step 4: Get Your Backend URL

Once deployed, you'll see:
```
Your service is live at https://echomind-backend-XXXX.onrender.com
```

**📝 Copy this URL! You'll need it for the frontend.**

### Step 5: Test Backend

Visit: `https://your-backend-url.onrender.com/health`

You should see:
```json
{
  "status": "healthy",
  "version": "1.0.0",
  ...
}
```

**API Docs:** `https://your-backend-url.onrender.com/docs`

---

## Part 3: Deploy Frontend to Vercel

### Step 1: Create Vercel Account

1. Go to https://vercel.com
2. Click "Sign Up"
3. Sign up with your GitHub account

### Step 2: Deploy Frontend

1. Click **"Add New..."** → **"Project"**
2. Import your **`echomind`** repository
3. Configure the project:

**Framework Preset:** Vite

**Root Directory:** Click "Edit" and set to `frontend`

**Build & Development Settings:**
- **Build Command:** `npm run build`
- **Output Directory:** `dist`
- **Install Command:** `npm install`

**Environment Variables:**
Click "Add" and enter:

| Name | Value |
|------|-------|
| `VITE_API_URL` | Your Render backend URL (e.g., `https://echomind-backend-XXXX.onrender.com`) |

4. Click **"Deploy"**

### Step 3: Wait for Deployment

- Takes 1-2 minutes
- Watch build logs
- You'll see: "Building..." → "Deploying..." → "Ready ✅"

### Step 4: Get Your Frontend URL

Once deployed:
```
✅ Your site is live at https://echomind-XXXX.vercel.app
```

---

## Part 4: Final Configuration

### Update Backend CORS

1. Go back to your **Render dashboard**
2. Click on your backend service
3. Go to **"Environment"** tab
4. Update `CORS_ORIGINS`:
   ```
   https://echomind-XXXX.vercel.app
   ```
   (Replace with your actual Vercel URL)
5. Click **"Save Changes"**
6. Service will redeploy (takes ~2 minutes)

---

## Part 5: Ingest Sample Data

Your backend needs mental wellness documents. You have two options:

### Option A: Use Render Shell (Recommended)

1. In Render dashboard, click your backend service
2. Click **"Shell"** tab in top right
3. Run:
   ```bash
   cd ../data
   python sample_ingest.py
   ```
4. Wait for "Ingestion Complete!"

### Option B: Use API Endpoint

You can use the `/api/v1/ingest` endpoint via the API docs:

1. Go to `https://your-backend-url.onrender.com/docs`
2. Expand **POST `/api/v1/ingest`**
3. Click "Try it out"
4. Use sample documents from `data/sample_ingest.py`

---

## 🎉 Your Website is Live!

### Test Your Deployment

1. **Visit your Vercel URL**: `https://echomind-XXXX.vercel.app`
2. You should see the EchoMind chat interface
3. Try queries:
   - "What are stress management techniques?"
   - "I'm feeling anxious"
   - "I'm having a panic attack"

### Share Your Website

Your website is now live at:
```
🌐 https://echomind-XXXX.vercel.app
```

Share this URL with anyone!

---

## 🔧 Maintenance & Updates

### Update Your Website

When you make changes:

```powershell
# Make your changes
# Then commit and push

git add .
git commit -m "Description of changes"
git push
```

**Automatic deployment:**
- Render will automatically redeploy backend
- Vercel will automatically redeploy frontend

### Monitor Your Services

**Render Dashboard:**
- View logs
- Monitor performance
- Check error reports

**Vercel Dashboard:**
- View analytics
- Monitor build logs
- Check performance metrics

---

## 💰 Cost & Limitations

### Free Tier Limits

**Render (Backend):**
- ✅ Free forever
- ⚠️ Spins down after 15 minutes of inactivity
- First request after sleep: 30-60 seconds
- 750 hours/month free (enough for continuous running)

**Vercel (Frontend):**
- ✅ Free forever for personal projects
- Unlimited bandwidth
- 100 GB bandwidth/month
- Automatic HTTPS

### Keep Backend Active

To prevent cold starts, you can:

1. **Use UptimeRobot** (free service):
   - Sign up at https://uptimerobot.com
   - Add monitor for your backend health endpoint
   - Ping every 14 minutes

2. **Upgrade to Render paid plan** ($7/month):
   - Always-on service
   - No cold starts

---

## 🐛 Troubleshooting

### Backend Issues

**"Build failed"**
- Check Render logs
- Verify `requirements.txt` is correct
- Ensure all dependencies are listed

**"Application error"**
- Check environment variables
- Verify `CORS_ORIGINS` is set correctly
- Check logs for Python errors

**"No data in responses"**
- Run data ingestion script via Render Shell
- Check ChromaDB persistence path

### Frontend Issues

**"API Error"**
- Verify `VITE_API_URL` is correct in Vercel
- Check backend is running
- Verify CORS settings on backend

**"Build failed"**
- Check build logs in Vercel
- Verify `package.json` is correct
- Try rebuilding

---

## 🔐 Security Best Practices

### For Production

1. **Update SECRET_KEY** in Render environment variables
2. **Set specific CORS origins** (not `*`)
3. **Add rate limiting** (future enhancement)
4. **Monitor logs** regularly
5. **Keep dependencies updated**

### Environment Variables

Never commit these to GitHub:
- ❌ `.env` (already in `.gitignore`)
- ❌ API keys
- ❌ Secret keys
- ✅ Always use environment variables

---

## 📊 Custom Domain (Optional)

### Add Your Own Domain

**Vercel:**
1. Go to project settings
2. Click "Domains"
3. Add your domain
4. Follow DNS configuration instructions

**Render:**
1. Upgrade to paid plan
2. Go to service settings
3. Add custom domain

---

## 🎓 What You've Accomplished

✅ Deployed a full-stack AI application  
✅ Backend API with RAG pipeline on Render  
✅ React frontend on Vercel  
✅ Automatic CI/CD from GitHub  
✅ Production-ready mental wellness platform  
✅ Free hosting with HTTPS  

---

## 📞 Need Help?

- **Render Docs:** https://render.com/docs
- **Vercel Docs:** https://vercel.com/docs
- **Check logs:** Both platforms have detailed logs

---

## 🚀 Next Steps

1. **Share your website** with friends and get feedback
2. **Add more data** by modifying `data/sample_ingest.py`
3. **Customize** the UI in `frontend/src/components/`
4. **Monitor** usage via Render and Vercel dashboards
5. **Update** crisis hotlines for your region in backend `.env`

---

**Congratulations! Your EchoMind platform is now live and helping people! 🎉**

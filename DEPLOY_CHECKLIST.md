# ✅ EchoMind Deployment Checklist

Follow these steps to deploy your website!

## 📋 Pre-Deployment Checklist

- [ ] Git is installed on your computer
- [ ] You have a GitHub account
- [ ] You have a Render account (free)
- [ ] You have a Vercel account (free)

## 🚀 Deployment Steps

### 1️⃣ Push to GitHub (5 minutes)

```powershell
cd C:\Users\Mariya\Documents\dev\echomind
git init
git add .
git commit -m "Initial commit: EchoMind platform"
git remote add origin https://github.com/YOUR_USERNAME/echomind.git
git branch -M main
git push -u origin main
```

- [ ] Code is on GitHub
- [ ] Repository is public

---

### 2️⃣ Deploy Backend to Render (10 minutes)

1. Go to https://render.com
2. Sign in with GitHub
3. Click "New +" → "Web Service"
4. Select `echomind` repository
5. Configure:
   - **Name**: `echomind-backend`
   - **Root Directory**: `backend`
   - **Build Command**: `pip install -r requirements.txt && python -m spacy download en_core_web_sm`
   - **Start Command**: `python -m app.main`
   - **Plan**: Free
6. Add environment variables:
   - `API_HOST` = `0.0.0.0`
   - `API_PORT` = `8000`
   - `ENVIRONMENT` = `production`
   - `CORS_ORIGINS` = `*`
   - `SECRET_KEY` = (Generate)
7. Click "Create Web Service"

- [ ] Backend is deployed
- [ ] Backend URL copied: `________________________`
- [ ] Health check works: `/health`

---

### 3️⃣ Deploy Frontend to Vercel (5 minutes)

1. Go to https://vercel.com
2. Sign in with GitHub
3. Click "Add New..." → "Project"
4. Import `echomind` repository
5. Configure:
   - **Framework**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
6. Add environment variable:
   - `VITE_API_URL` = (Your Render backend URL)
7. Click "Deploy"

- [ ] Frontend is deployed
- [ ] Frontend URL: `________________________`
- [ ] Can access the chat interface

---

### 4️⃣ Update CORS (2 minutes)

1. Go back to Render dashboard
2. Click your backend service
3. Environment tab
4. Update `CORS_ORIGINS` with your Vercel URL
5. Save changes

- [ ] CORS updated
- [ ] Backend redeployed

---

### 5️⃣ Add Sample Data (5 minutes)

**Option A - Render Shell:**
1. Render dashboard → Your service
2. Click "Shell" tab
3. Run: `cd ../data && python sample_ingest.py`

**Option B - API Endpoint:**
1. Visit: `YOUR_BACKEND_URL/docs`
2. Use POST `/api/v1/ingest` endpoint
3. Add documents from `data/sample_ingest.py`

- [ ] Sample data ingested
- [ ] Queries return results

---

### 6️⃣ Test Your Website (5 minutes)

Visit your Vercel URL and test:
- [ ] Chat interface loads
- [ ] Can send messages
- [ ] Receives responses
- [ ] Emergency banner works (try: "I'm feeling suicidal")
- [ ] Resources display correctly

---

## 🎉 Deployment Complete!

Your website is live at:
```
🌐 https://________________________.vercel.app
```

Backend API:
```
🔧 https://________________________.onrender.com
```

---

## 📱 Share Your Website

Share your Vercel URL with:
- [ ] Friends and family
- [ ] Social media
- [ ] Portfolio
- [ ] LinkedIn

---

## 🔄 Future Updates

When you make changes:
```powershell
git add .
git commit -m "Your changes"
git push
```

Both Render and Vercel will auto-deploy! ✨

---

## 🆘 Having Issues?

Check:
1. **Render logs** - View deployment logs
2. **Vercel logs** - Check build logs
3. **DEPLOYMENT.md** - Full detailed guide
4. **Browser console** - Check for errors

Common fixes:
- Verify environment variables
- Check CORS settings
- Ensure data is ingested
- Verify backend is awake (free tier sleeps)

---

## 📞 Keep Backend Active (Optional)

Free Render services sleep after 15 minutes.

Use **UptimeRobot** (free):
1. Sign up: https://uptimerobot.com
2. Add monitor: Your backend `/health` endpoint
3. Check interval: Every 14 minutes

- [ ] UptimeRobot configured (optional)

---

**Time to complete: ~30 minutes**
**Cost: $0 (completely free!)**

**🎊 Congratulations on deploying your AI-powered mental wellness platform!**

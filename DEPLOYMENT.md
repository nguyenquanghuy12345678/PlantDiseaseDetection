# Deployment Guide - Render.com

## 🚀 Quick Deploy to Render

### Option 1: One-Click Deploy (Recommended)

1. **Fork/Clone this repository** to your GitHub account

2. **Click the Deploy button:**

   [![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy?repo=https://github.com/nguyenquanghuy12345678/PlantDiseaseDetection)

3. **Configure environment variables** in Render dashboard (auto-filled from render.yaml)

4. **Wait for deployment** (~5-10 minutes for first build)

5. **Access your app** at: `https://your-app-name.onrender.com`

---

### Option 2: Manual Deployment

#### Step 1: Create Render Account
- Sign up at [render.com](https://render.com)
- Connect your GitHub account

#### Step 2: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your repository: `PlantDiseaseDetection`
3. Configure settings:
   - **Name:** `plant-disease-detection`
   - **Region:** Oregon (or closest to you)
   - **Branch:** `main`
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### Step 3: Set Environment Variables
Add these in Render dashboard → Environment:

```bash
# Required
SECRET_KEY=<generate-random-32-char-string>
DEBUG=false
PYTHON_VERSION=3.12.0

# Optional (defaults work)
MAX_FILE_SIZE=16777216
ALLOWED_EXTENSIONS=png,jpg,jpeg
SESSION_MAX_AGE=86400
```

**Generate SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

#### Step 4: Add Persistent Disk (for uploads)
1. Go to **"Disks"** tab
2. Click **"Add Disk"**
3. Configure:
   - **Name:** `uploads`
   - **Mount Path:** `/opt/render/project/src/static/uploads`
   - **Size:** 1 GB (free tier)

#### Step 5: Deploy
- Click **"Create Web Service"**
- Wait for build to complete (~5-10 minutes)

---

## 📋 Requirements

### Python Version
- Python 3.11+ (Render supports 3.11, 3.12)
- Specified in `render.yaml`: `PYTHON_VERSION=3.12.0`

### Dependencies
All dependencies in `requirements.txt` will be installed automatically:
- FastAPI
- Uvicorn
- Pydantic
- Pillow, NumPy
- TensorFlow (CPU - auto-installed on Render)

### Build Time
- **First build:** ~5-10 minutes (installs TensorFlow)
- **Subsequent builds:** ~2-3 minutes (cached)

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description | Required |
|----------|---------|-------------|----------|
| `SECRET_KEY` | - | Session encryption key (32+ chars) | ✅ Yes |
| `DEBUG` | `false` | Debug mode (set false in production) | ❌ No |
| `PORT` | `8000` | Server port (Render sets automatically) | ❌ No |
| `MAX_FILE_SIZE` | `16777216` | Max upload size (16MB) | ❌ No |
| `ALLOWED_EXTENSIONS` | `png,jpg,jpeg` | Allowed file types | ❌ No |
| `SESSION_MAX_AGE` | `86400` | Session duration (24h) | ❌ No |
| `TF_ENABLE_ONEDNN_OPTS` | `0` | Disable TensorFlow warnings | ❌ No |

### Disk Storage
- **Purpose:** Store uploaded images persistently
- **Path:** `/opt/render/project/src/static/uploads`
- **Size:** 1 GB (free tier)
- **Note:** Without disk, uploads are lost on restart

---

## 🌐 Post-Deployment

### Check Deployment Status
1. Visit your Render dashboard
2. Check **"Logs"** tab for any errors
3. Verify deployment: `https://your-app.onrender.com`

### Test API
```bash
# Homepage
curl https://your-app.onrender.com/

# API Documentation
curl https://your-app.onrender.com/docs

# Health check
curl https://your-app.onrender.com/api/history
```

### View API Documentation
- **Swagger UI:** `https://your-app.onrender.com/docs`
- **ReDoc:** `https://your-app.onrender.com/redoc`
- **OpenAPI JSON:** `https://your-app.onrender.com/openapi.json`

---

## ⚙️ Render Configuration Files

### `render.yaml`
Blueprint file for infrastructure-as-code deployment. Defines:
- Service type (web)
- Build/start commands
- Environment variables
- Health checks
- Persistent disk configuration

### `.env.example`
Template for local development environment variables. Copy to `.env`:
```bash
cp .env.example .env
# Edit .env with your values
```

**Note:** `.env` is gitignored and won't be deployed. Use Render dashboard for production env vars.

---

## 🐛 Troubleshooting

### Build Fails
**Issue:** `ERROR: Could not find a version that satisfies tensorflow`
- **Solution:** Render auto-detects and installs TensorFlow CPU version
- **Wait:** First build takes 5-10 minutes

### App Crashes on Startup
**Issue:** `ModuleNotFoundError: No module named 'app'`
- **Check:** Build command is `pip install -r requirements.txt`
- **Check:** Start command is `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Uploads Disappear
**Issue:** Uploaded images lost after restart
- **Solution:** Add persistent disk (see Step 4 above)
- **Path:** `/opt/render/project/src/static/uploads`

### 502 Bad Gateway
**Issue:** App not responding
- **Check:** Logs in Render dashboard
- **Common cause:** Port mismatch (use `$PORT` environment variable)
- **Fix:** Start command must include `--port $PORT`

### TensorFlow Warnings
**Issue:** Too many TensorFlow logs
- **Solution:** Set `TF_CPP_MIN_LOG_LEVEL=2` in environment variables

---

## 📊 Performance

### Free Tier Limits
- **RAM:** 512 MB
- **CPU:** Shared
- **Disk:** 1 GB (optional)
- **Sleep:** Inactive after 15 minutes (cold start ~30s)
- **Build minutes:** 500/month

### Optimization Tips
1. **Keep app warm:** Use UptimeRobot or similar to ping every 14 minutes
2. **Reduce model size:** Model is 10.5 MB (acceptable)
3. **Cache dependencies:** Render caches pip packages
4. **Enable OneDNN:** Set `TF_ENABLE_ONEDNN_OPTS=1` (may speed up CPU inference)

---

## 🔒 Security

### Production Checklist
- ✅ Set `DEBUG=false`
- ✅ Use strong `SECRET_KEY` (32+ characters)
- ✅ Enable HTTPS (automatic on Render)
- ✅ Set CORS origins (if using separate frontend)
- ✅ Don't commit `.env` file
- ✅ Use Render's secret management

### CORS Configuration
If deploying frontend separately, update `app/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourfrontend.com"],  # Update this
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 🔄 Updates & Redeployment

### Auto-Deploy
- Render auto-deploys on push to `main` branch
- Check `render.yaml`: `autoDeploy: true`

### Manual Deploy
1. Go to Render dashboard
2. Click **"Manual Deploy"** → **"Deploy latest commit"**

### Rollback
1. Go to **"Events"** tab
2. Find previous successful deployment
3. Click **"Rollback"**

---

## 💰 Pricing

### Free Tier (Current)
- ✅ 1 web service
- ✅ 512 MB RAM
- ✅ Automatic HTTPS
- ✅ Auto-deploys
- ⚠️ Sleeps after 15 min inactivity

### Starter ($7/month)
- ✅ No sleep
- ✅ 2 GB RAM
- ✅ Faster builds
- ✅ Multiple services

### Upgrade
```bash
# Via dashboard: Settings → Plan → Upgrade
```

---

## 📚 Additional Resources

- [Render Documentation](https://render.com/docs)
- [FastAPI Deployment Guide](https://fastapi.tiangolo.com/deployment/)
- [Python on Render](https://render.com/docs/deploy-python)
- [Environment Variables](https://render.com/docs/environment-variables)

---

## 🆘 Support

### Render Support
- [Community Forum](https://community.render.com/)
- [Status Page](https://status.render.com/)
- Email: support@render.com

### Project Issues
- [GitHub Issues](https://github.com/nguyenquanghuy12345678/PlantDiseaseDetection/issues)

---

**Last Updated:** December 25, 2025
**Render Version:** Blueprint Spec v1

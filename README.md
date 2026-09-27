# 🌐 Social Media Hub — Unified Dashboard with VPN/Proxy Support

A Streamlit dashboard that connects to Facebook, Instagram, Twitter/X,
TikTok, LinkedIn, and YouTube — with optional proxy routing for VPN use.

> ⚠️ **Important:** Streamlit Cloud cannot run a VPN server. This app
> works **alongside** a VPN on your device. The proxy feature lets the
> dashboard route its own API calls through your VPN's proxy endpoint.

## 🎯 Features

- 🔗 Connect all your social media accounts in one place
- 🔐 Credentials stored in session only (never written to disk)
- 🌐 Optional proxy routing (SOCKS5/HTTP) for VPN integration
- 🧪 Test API connectivity with one click
- 📊 Connection summary with masked credentials

## 🚀 Deploy in 5 minutes

### 1. Push to GitHub

```bash
git init social-media-hub
cd social-media-hub
# copy the files listed below
git add .
git commit -m "Initial Social Media Hub"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/social-media-hub.git
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io) and sign in.
2. Click **Create app** → **Deploy a public app from GitHub**[reference:3].
3. Fill in:
   - **Repository**: `YOUR_USERNAME/social-media-hub`
   - **Branch**: `main`
   - **Main file path**: `app.py`
4. Click **Deploy**.

### 3. Optional — Add secrets

In Streamlit Cloud → App Settings → **Secrets**, paste:
```toml
PROXY_URL = "socks5://your-vpn-proxy:port"
```

## 🗂 File structure

```
social-media-hub/
├── app.py
├── requirements.txt
├── README.md
└── .streamlit/
    ├── config.toml
    └── secrets.toml
```

## 🔐 How VPN + Proxy Work Together

1. Install a **VPN app** on your phone or computer (Proton VPN, NordVPN, etc.).
2. Connect the VPN to a supported region (US, FR, CA).
3. If the VPN provides a **proxy endpoint** (some do — check your VPN's dashboard),
   paste it into the sidebar and enable proxy routing.
4. Now your **device** and this **dashboard** both appear to be in that region.

## 📞 Contact

**Gesner Deslandes · Software Engineer**
- 📞 (509)-47385663
- ✉️ deslandes78@gmail.com

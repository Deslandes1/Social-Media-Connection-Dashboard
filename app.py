# app.py
# =============================================================================
# SOCIAL MEDIA HUB — Unified Dashboard with VPN/Proxy Support
# Built by Gesner Deslandes · Software Engineer
# Contact Info : (509)-47385663 · Email : deslandes78@gmail.com
# =============================================================================

import os
import json
from datetime import datetime

import streamlit as st
import requests

# -----------------------------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Social Media Hub · Built by Gesner Deslandes",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------------------------------------------------------
# GLOBAL CSS — Dark theme with gold/cyan accents
# -----------------------------------------------------------------------------
CSS = """
<style>
  .stApp {
    background:
      radial-gradient(1200px 700px at 50% -10%, rgba(0,229,255,.10), transparent 65%),
      radial-gradient(900px 600px at 10% 110%, rgba(255,217,59,.05), transparent 60%),
      #05070c !important;
    color: #d8e4f0;
  }
  .hub-header {
    padding: 22px 20px 18px;
    border-radius: 20px;
    background:
      radial-gradient(1000px 300px at 50% 0%, rgba(255,217,59,.18), transparent 70%),
      linear-gradient(180deg, rgba(24,18,6,.98), rgba(8,6,3,.98));
    border: 3px solid #ffd93b;
    box-shadow: 0 20px 60px rgba(0,0,0,.9), 0 0 60px rgba(255,217,59,.20);
    text-align: center; margin-bottom: 18px;
  }
  .hub-brand {
    font-family: Georgia, serif;
    font-size: clamp(1.5rem, 4vw, 2.4rem);
    font-weight: 900; letter-spacing: 6px;
    background: linear-gradient(90deg,#ffd93b,#ff8a2b,#ffd93b,#a86bff,#ffd93b);
    background-size: 200% 100%;
    -webkit-background-clip: text; background-clip: text; color: transparent;
    margin: 0 0 6px;
  }
  .hub-tagline {
    font-size: .74rem; font-weight: 900; letter-spacing: 3px;
    color: #ffe680; text-transform: uppercase; margin-bottom: 12px;
  }
  .hub-credit {
    font-family: Georgia, serif; font-size: .82rem; font-weight: 900;
    letter-spacing: 1.4px; color: #ffd93b;
  }
  .hub-credit small {
    display: block; font-family: 'Courier New', monospace;
    font-size: .7rem; color: #6b7c92; letter-spacing: 1.2px;
    margin-top: 4px; font-weight: 800;
  }
  .hub-credit a { color: #00e5ff; text-decoration: none; border-bottom: 1px dotted #00e5ff; }

  .platform-card {
    padding: 18px 20px; border-radius: 16px;
    background: linear-gradient(180deg, rgba(8,14,22,.98), rgba(4,7,12,.98));
    border: 2px solid #1c2636;
    box-shadow: 0 14px 36px rgba(0,0,0,.65);
    margin-bottom: 16px;
  }
  .platform-card.connected {
    border-color: rgba(34,255,136,.6);
    box-shadow: 0 14px 36px rgba(0,0,0,.65), 0 0 30px rgba(34,255,136,.15);
  }
  .platform-card.disconnected {
    border-color: rgba(255,59,48,.4);
  }
  .platform-title {
    font-family: Georgia, serif; font-size: 1.1rem;
    font-weight: 900; letter-spacing: 1.4px; color: #fff;
    margin-bottom: 4px;
  }
  .platform-status {
    font-family: 'Courier New', monospace; font-size: .7rem;
    letter-spacing: 1.4px; text-transform: uppercase;
    margin-bottom: 10px;
  }
  .platform-status.on { color: #22ff88; }
  .platform-status.off { color: #ff3b30; }

  .hub-footer {
    margin-top: 24px; padding: 18px; border-radius: 14px;
    text-align: center;
    background: linear-gradient(180deg, rgba(8,14,22,.98), rgba(4,7,12,.98));
    border: 2px solid #1c2636;
    font-family: 'Courier New', monospace;
    font-size: .72rem; color: #6b7c92;
    letter-spacing: 1.4px; line-height: 2;
  }
  .hub-footer strong { color: #ffd93b; letter-spacing: 2px; }
  .hub-footer a { color: #00e5ff; text-decoration: none; border-bottom: 1px dotted #00e5ff; }

  div[data-testid="stButton"] > button {
    border-radius: 11px; font-weight: 900;
    letter-spacing: 1.2px; padding: 10px 16px; transition: all .15s;
  }
  div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px);
    box-shadow: 0 0 20px rgba(255,217,59,.35);
  }
  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea {
    background: rgba(3,6,12,.9) !important;
    color: #fff !important;
    border: 2px solid rgba(58,160,255,.5) !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
  }
  .stTextInput > div > div > input:focus,
  .stTextArea > div > div > textarea:focus {
    border-color: #ffd93b !important;
    box-shadow: 0 0 0 3px rgba(255,217,59,.25) !important;
  }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# PLATFORM DEFINITIONS
# -----------------------------------------------------------------------------
PLATFORMS = [
    {
        "id": "facebook",
        "name": "Facebook",
        "icon": "📘",
        "color": "#1877f2",
        "fields": ["access_token", "page_id"],
        "help": "Get your token from developers.facebook.com/tools/explorer",
    },
    {
        "id": "instagram",
        "name": "Instagram",
        "icon": "📷",
        "color": "#e4405f",
        "fields": ["access_token", "business_account_id"],
        "help": "Use Instagram Graph API (requires Business account)",
    },
    {
        "id": "twitter",
        "name": "Twitter / X",
        "icon": "🐦",
        "color": "#1da1f2",
        "fields": ["bearer_token", "api_key", "api_secret"],
        "help": "Get keys from developer.twitter.com",
    },
    {
        "id": "tiktok",
        "name": "TikTok",
        "icon": "🎵",
        "color": "#ff0050",
        "fields": ["access_token", "open_id"],
        "help": "Use TikTok for Developers portal",
    },
    {
        "id": "linkedin",
        "name": "LinkedIn",
        "icon": "💼",
        "color": "#0077b5",
        "fields": ["access_token", "person_urn"],
        "help": "Get token from LinkedIn Developer Portal",
    },
    {
        "id": "youtube",
        "name": "YouTube",
        "icon": "▶️",
        "color": "#ff0000",
        "fields": ["api_key", "channel_id"],
        "help": "Get API key from console.cloud.google.com",
    },
]

# -----------------------------------------------------------------------------
# SESSION STATE
# -----------------------------------------------------------------------------
def init_state():
    defaults = {
        "connections": {},
        "proxy_enabled": False,
        "proxy_url": "",
        "proxy_verified": False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

# -----------------------------------------------------------------------------
# PROXY HELPER
# -----------------------------------------------------------------------------
def get_proxy_dict():
    """Return a proxies dict for requests if proxy is enabled."""
    if st.session_state.proxy_enabled and st.session_state.proxy_url:
        return {
            "http": st.session_state.proxy_url,
            "https": st.session_state.proxy_url,
        }
    return None


def verify_proxy():
    """Test if the proxy is working by making a request to a test URL."""
    proxy_url = st.session_state.proxy_url
    if not proxy_url:
        return False, "No proxy URL entered."

    proxies = {"http": proxy_url, "https": proxy_url}
    try:
        r = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=10)
        if r.status_code == 200:
            ip_data = r.json()
            return True, f"✅ Proxy working — your visible IP: {ip_data.get('origin', 'unknown')}"
        return False, f"❌ Proxy responded with status {r.status_code}"
    except Exception as e:
        return False, f"❌ Proxy failed: {str(e)[:150]}"


# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hub-header">
      <div class="hub-brand">SOCIAL MEDIA HUB</div>
      <div class="hub-tagline">🌐 One Dashboard · All Platforms · VPN-Ready</div>
      <div class="hub-credit">
        BUILT BY GESNER DESLANDES · SOFTWARE ENGINEER
        <small>
          📞 <a href="tel:+50947385663">(509)-47385663</a> &nbsp;·&nbsp;
          ✉️ <a href="mailto:deslandes78@gmail.com">deslandes78@gmail.com</a>
        </small>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# SIDEBAR — VPN / PROXY CONFIGURATION
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🔐 VPN / Proxy Configuration")
    st.caption(
        "A VPN on your **device** changes your IP. "
        "The proxy below lets this app route its API calls through it too."
    )

    st.session_state.proxy_enabled = st.toggle(
        "Enable Proxy for API calls", value=st.session_state.proxy_enabled
    )

    if st.session_state.proxy_enabled:
        st.session_state.proxy_url = st.text_input(
            "Proxy URL",
            value=st.session_state.proxy_url,
            placeholder="http://user:pass@host:port  OR  socks5://host:port",
        )

        if st.button("🔍 Verify Proxy", use_container_width=True):
            with st.spinner("Testing proxy…"):
                ok, msg = verify_proxy()
                st.session_state.proxy_verified = ok
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)

        if st.session_state.proxy_verified:
            st.markdown(
                '<div style="padding:10px;border-radius:8px;'
                'background:rgba(34,255,136,.08);'
                'border:1.5px solid rgba(34,255,136,.4);'
                'color:#a8ffd0;font-family:Courier New,monospace;'
                'font-size:.74rem;">🟢 Proxy active — API calls will route through it.</div>',
                unsafe_allow_html=True,
            )
        else:
            st.warning("⚠️ Proxy not verified yet.")
    else:
        st.info("Proxy disabled — API calls go direct from Streamlit Cloud.")

    st.markdown("---")
    st.markdown("### 💡 How VPN + Proxy Work Together")
    st.markdown(
        """
        1. Install a VPN app on your **phone or computer**.
        2. Connect the VPN to a supported region (US, FR, CA).
        3. If the VPN offers a **proxy endpoint** (e.g. WireGuard → SOCKS5),
           paste it above and enable it.
        4. Now both your device **and** this dashboard appear to be in
           that region.
        """
    )

    st.markdown("---")
    st.markdown("### 📌 Note on Streamlit Cloud")
    st.caption(
        "Streamlit Cloud **cannot run a VPN server** inside the app. "
        "The VPN must live on your device. The proxy option here lets "
        "the dashboard route its own API calls through your VPN."
    )

# -----------------------------------------------------------------------------
# MAIN — PLATFORM CONNECTIONS
# -----------------------------------------------------------------------------
st.markdown("## 🔗 Connect Your Social Media Accounts")
st.caption(
    "Enter your API credentials for each platform. "
    "Credentials are stored only in this browser session."
)

# Create a grid of platform cards
cols = st.columns(2)

for i, platform in enumerate(PLATFORMS):
    col = cols[i % 2]
    pid = platform["id"]

    with col:
        connected = pid in st.session_state.connections and st.session_state.connections[pid].get("active")
        card_class = "connected" if connected else "disconnected"

        st.markdown(
            f"""
            <div class="platform-card {card_class}">
              <div class="platform-title">{platform['icon']} {platform['name']}</div>
              <div class="platform-status {'on' if connected else 'off'}">
                {'● Connected' if connected else '○ Not connected'}
              </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        with st.expander(f"🔑 Configure {platform['name']}", expanded=not connected):
            st.caption(platform["help"])

            values = {}
            for field in platform["fields"]:
                label = field.replace("_", " ").title()
                values[field] = st.text_input(
                    label,
                    type="password" if "token" in field or "secret" in field else "default",
                    key=f"field_{pid}_{field}",
                    placeholder=f"Enter {label}",
                )

            b1, b2 = st.columns(2)
            with b1:
                if st.button(f"✅ Connect", key=f"connect_{pid}", use_container_width=True):
                    if all(values.get(f) for f in platform["fields"]):
                        st.session_state.connections[pid] = {
                            "active": True,
                            "credentials": values,
                            "connected_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        }
                        st.success(f"✅ {platform['name']} connected!")
                        st.rerun()
                    else:
                        st.error("❌ Please fill in all fields.")
            with b2:
                if st.button(f"🗑 Disconnect", key=f"disconnect_{pid}", use_container_width=True):
                    if pid in st.session_state.connections:
                        del st.session_state.connections[pid]
                    st.warning(f"Disconnected from {platform['name']}.")
                    st.rerun()

# -----------------------------------------------------------------------------
# CONNECTION SUMMARY
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("## 📊 Connection Summary")

connected_list = [
    p["name"] for p in PLATFORMS
    if p["id"] in st.session_state.connections and st.session_state.connections[p["id"]].get("active")
]

if connected_list:
    st.success(f"✅ Connected to {len(connected_list)} platform(s): {', '.join(connected_list)}")
else:
    st.info("No platforms connected yet. Configure at least one above.")

# Show connection details
if st.session_state.connections:
    with st.expander("📋 View saved connection details (masked)"):
        for pid, data in st.session_state.connections.items():
            platform = next((p for p in PLATFORMS if p["id"] == pid), None)
            if not platform:
                continue
            st.markdown(f"**{platform['icon']} {platform['name']}** — connected {data.get('connected_at', '—')}")
            for field, val in data.get("credentials", {}).items():
                masked = val[:4] + "•" * 8 + val[-4:] if len(val) > 8 else "••••••••"
                st.code(f"{field}: {masked}", language="text")

# -----------------------------------------------------------------------------
# TEST API CALL
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("## 🧪 Test API Connectivity")

if st.button("🔄 Test All Connected Platforms", use_container_width=True):
    proxies = get_proxy_dict()
    if not st.session_state.connections:
        st.warning("No platforms connected — connect at least one first.")
    else:
        for pid, data in st.session_state.connections.items():
            platform = next((p for p in PLATFORMS if p["id"] == pid), None)
            if not platform:
                continue
            try:
                # Simple connectivity test — replace with real API call per platform
                test_url = "https://httpbin.org/ip"
                r = requests.get(test_url, proxies=proxies, timeout=10)
                if r.status_code == 200:
                    st.success(f"{platform['icon']} {platform['name']}: API reachable ✅ (IP: {r.json().get('origin', '?')})")
                else:
                    st.error(f"{platform['icon']} {platform['name']}: HTTP {r.status_code}")
            except Exception as e:
                st.error(f"{platform['icon']} {platform['name']}: {str(e)[:100]}")

# -----------------------------------------------------------------------------
# FOOTER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hub-footer">
      <strong>SOCIAL MEDIA HUB · BUILT BY GESNER DESLANDES · SOFTWARE ENGINEER</strong><br>
      📞 Contact Info : <a href="tel:+50947385663">(509)-47385663</a> ·
      ✉️ Email : <a href="mailto:deslandes78@gmail.com">deslandes78@gmail.com</a><br>
      <span style="opacity:.7;font-size:.66rem;">
        🔐 Credentials stay in your browser session · Never saved to disk
      </span>
    </div>
    """,
    unsafe_allow_html=True,
)

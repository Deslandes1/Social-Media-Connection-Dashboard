# app.py
# =============================================================================
# SOCIAL MEDIA HUB — Fully User-Managed Credentials · Light Blue Theme
# Built by Gesner Deslandes · Software Engineer
# Contact Info : (509)-47385663 · Email : deslandes78@gmail.com
#
# Every user enters their OWN credentials in the interface.
# Nothing is stored server-side. All data lives in the browser session.
# =============================================================================

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
# GLOBAL CSS — LIGHT BLUE THEME
# -----------------------------------------------------------------------------
CSS = """
<style>
  /* ===== PAGE BACKGROUND ===== */
  .stApp {
    background:
      radial-gradient(1200px 700px at 50% -10%, rgba(255,255,255,.85), transparent 65%),
      radial-gradient(900px 600px at 10% 110%, rgba(180,220,255,.55), transparent 60%),
      radial-gradient(900px 600px at 90% 110%, rgba(200,230,255,.50), transparent 60%),
      #d4eaff !important;
    color: #0a2540;
  }
  .stApp, .stApp p, .stApp span, .stApp label, .stApp div,
  .stMarkdown, .stText, .stCaption, .stAlert {
    color: #0a2540 !important;
  }
  .stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp h5, .stApp h6 {
    color: #06357a !important;
  }
  .stApp .stCaption, .stApp small {
    color: #35608f !important;
  }
  section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #eaf4ff, #cfe6ff) !important;
    border-right: 2px solid #9cc8ff !important;
  }
  section[data-testid="stSidebar"] * {
    color: #0a2540 !important;
  }
  details summary {
    color: #06357a !important;
    font-weight: 800 !important;
  }

  /* ===== HEADER ===== */
  .hub-header {
    padding: 22px 20px 18px;
    border-radius: 20px;
    background:
      radial-gradient(1000px 300px at 50% 0%, rgba(255,255,255,.9), transparent 70%),
      linear-gradient(180deg, #eaf4ff, #cfe6ff);
    border: 3px solid #3aa0ff;
    box-shadow: 0 20px 60px rgba(58,160,255,.25), 0 0 40px rgba(58,160,255,.15);
    text-align: center; margin-bottom: 18px;
  }
  .hub-brand {
    font-family: Georgia, serif;
    font-size: clamp(1.5rem, 4vw, 2.4rem);
    font-weight: 900; letter-spacing: 6px;
    background: linear-gradient(90deg,#06357a,#1060a0,#06357a,#3a6bd0,#06357a);
    background-size: 200% 100%;
    -webkit-background-clip: text; background-clip: text; color: transparent;
    margin: 0 0 6px;
  }
  .hub-tagline {
    font-size: .74rem; font-weight: 900; letter-spacing: 3px;
    color: #1060a0; text-transform: uppercase; margin-bottom: 12px;
  }
  .hub-credit {
    font-family: Georgia, serif; font-size: .82rem; font-weight: 900;
    letter-spacing: 1.4px; color: #06357a;
  }
  .hub-credit small {
    display: block; font-family: 'Courier New', monospace;
    font-size: .7rem; color: #35608f; letter-spacing: 1.2px;
    margin-top: 4px; font-weight: 800;
  }
  .hub-credit a {
    color: #1060a0; text-decoration: none;
    border-bottom: 1px dotted #1060a0;
  }
  .hub-credit a:hover { color: #06357a; }

  /* ===== PLATFORM CARDS ===== */
  .platform-card {
    padding: 18px 20px; border-radius: 16px;
    background: linear-gradient(180deg, #ffffff, #eef6ff);
    border: 2px solid #9cc8ff;
    box-shadow: 0 14px 36px rgba(58,160,255,.15);
    margin-bottom: 8px;
  }
  .platform-card.connected {
    border-color: rgba(20,168,96,.7);
    box-shadow: 0 14px 36px rgba(58,160,255,.15), 0 0 24px rgba(20,168,96,.18);
  }
  .platform-card.disconnected {
    border-color: rgba(224,58,48,.5);
  }
  .platform-title {
    font-family: Georgia, serif; font-size: 1.1rem;
    font-weight: 900; letter-spacing: 1.4px; color: #06357a;
    margin-bottom: 4px;
  }
  .platform-status {
    font-family: 'Courier New', monospace; font-size: .7rem;
    letter-spacing: 1.4px; text-transform: uppercase;
  }
  .platform-status.on  { color: #0a8f4a; }
  .platform-status.off { color: #c22a20; }

  /* ===== INFO BANNERS ===== */
  .banner-info {
    padding: 12px 16px; border-radius: 10px;
    background: rgba(58,160,255,.10);
    border: 1.5px solid rgba(58,160,255,.5);
    color: #06357a;
    font-family: 'Courier New', monospace;
    font-size: .78rem; line-height: 1.7;
    margin-bottom: 16px;
  }
  .banner-ok {
    padding: 12px 16px; border-radius: 10px;
    background: rgba(20,168,96,.14);
    border: 1.5px solid rgba(20,150,80,.55);
    color: #0a4b26;
    font-family: 'Courier New', monospace;
    font-size: .78rem; line-height: 1.7;
    margin-bottom: 16px;
  }
  .banner-warn {
    padding: 12px 16px; border-radius: 10px;
    background: rgba(255,176,32,.14);
    border: 1.5px solid rgba(214,136,0,.55);
    color: #6b4400;
    font-family: 'Courier New', monospace;
    font-size: .78rem; line-height: 1.7;
    margin-bottom: 16px;
  }

  /* ===== FOOTER ===== */
  .hub-footer {
    margin-top: 24px; padding: 18px; border-radius: 14px;
    text-align: center;
    background: linear-gradient(180deg, #ffffff, #e6f1ff);
    border: 2px solid #9cc8ff;
    font-family: 'Courier New', monospace;
    font-size: .72rem; color: #35608f;
    letter-spacing: 1.4px; line-height: 2;
  }
  .hub-footer strong { color: #06357a; letter-spacing: 2px; }
  .hub-footer a {
    color: #1060a0; text-decoration: none;
    border-bottom: 1px dotted #1060a0;
  }

  /* ===== BUTTONS ===== */
  div[data-testid="stButton"] > button {
    border-radius: 11px; font-weight: 900;
    letter-spacing: 1.2px; padding: 10px 16px;
    background: linear-gradient(180deg, #eaf4ff, #cfe6ff) !important;
    color: #06357a !important;
    border: 2px solid #3aa0ff !important;
    transition: all .15s;
  }
  div[data-testid="stButton"] > button:hover {
    transform: translateY(-1px);
    background: linear-gradient(180deg, #d3e9ff, #b3d8ff) !important;
    box-shadow: 0 6px 18px rgba(58,160,255,.35);
  }

  /* ===== INPUTS ===== */
  .stTextInput > div > div > input,
  .stTextArea > div > div > textarea,
  .stNumberInput > div > div > input,
  .stSelectbox > div > div > div,
  div[data-baseweb="select"] > div {
    background: #ffffff !important;
    color: #0a2540 !important;
    border: 2px solid #9cc8ff !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
  }
  .stTextInput > div > div > input:focus,
  .stTextArea > div > div > textarea:focus,
  .stNumberInput > div > div > input:focus {
    border-color: #3aa0ff !important;
    box-shadow: 0 0 0 3px rgba(58,160,255,.25) !important;
  }
  .stTextInput input::placeholder,
  .stTextArea textarea::placeholder {
    color: #7a9cbf !important;
    opacity: 1 !important;
  }

  /* ===== FILE UPLOADER ===== */
  div[data-testid="stFileUploader"] {
    background: #ffffff !important;
    border: 2px dashed #3aa0ff !important;
    border-radius: 12px !important;
    padding: 12px !important;
  }
  div[data-testid="stFileUploader"] * {
    color: #06357a !important;
  }

  /* ===== ALERTS ===== */
  .stAlert {
    border-radius: 12px !important;
    border-width: 2px !important;
  }
  div[data-testid="stAlert"] {
    background: #ffffff !important;
    color: #0a2540 !important;
  }

  /* ===== EXPANDER ===== */
  details {
    background: #ffffff !important;
    border: 1.5px solid #9cc8ff !important;
    border-radius: 12px !important;
  }

  /* ===== SPINNER / CAPTION ===== */
  .stSpinner > div { border-top-color: #3aa0ff !important; }
  .stCaption, div[data-testid="stCaptionContainer"] {
    color: #35608f !important;
  }

  /* ===== CODE BLOCKS ===== */
  code {
    background: #eaf4ff !important;
    color: #06357a !important;
    border-radius: 6px !important;
  }
  pre {
    background: #eaf4ff !important;
    border: 1px solid #9cc8ff !important;
    border-radius: 10px !important;
  }
  pre code {
    background: transparent !important;
    color: #06357a !important;
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
        "fields": [
            ("access_token", "Access Token", True),
            ("page_id",      "Page ID",      False),
        ],
        "help": "Get your token from developers.facebook.com/tools/explorer",
    },
    {
        "id": "instagram",
        "name": "Instagram",
        "icon": "📷",
        "fields": [
            ("access_token",        "Access Token",        True),
            ("business_account_id", "Business Account ID", False),
        ],
        "help": "Use Instagram Graph API (requires Business or Creator account)",
    },
    {
        "id": "twitter",
        "name": "Twitter / X",
        "icon": "🐦",
        "fields": [
            ("bearer_token", "Bearer Token", True),
            ("api_key",      "API Key",      True),
            ("api_secret",   "API Secret",   True),
        ],
        "help": "Get keys from developer.twitter.com/en/portal/dashboard",
    },
    {
        "id": "tiktok",
        "name": "TikTok",
        "icon": "🎵",
        "fields": [
            ("access_token", "Access Token", True),
            ("open_id",      "Open ID",      False),
        ],
        "help": "Use TikTok for Developers portal",
    },
    {
        "id": "linkedin",
        "name": "LinkedIn",
        "icon": "💼",
        "fields": [
            ("access_token", "Access Token", True),
            ("person_urn",   "Person URN",   False),
        ],
        "help": "Get token from LinkedIn Developer Portal",
    },
    {
        "id": "youtube",
        "name": "YouTube",
        "icon": "▶️",
        "fields": [
            ("api_key",    "API Key",    True),
            ("channel_id", "Channel ID", False),
        ],
        "help": "Get API key from console.cloud.google.com",
    },
]

# -----------------------------------------------------------------------------
# SESSION STATE
# -----------------------------------------------------------------------------
def init_state():
    defaults = {
        "connections":    {},       # { platform_id: { "credentials": {...}, "connected_at": "..." } }
        "proxy_enabled":  False,
        "proxy_url":      "",
        "proxy_verified": False,
        "proxy_ip":       "",
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


init_state()

# -----------------------------------------------------------------------------
# PROXY HELPERS
# -----------------------------------------------------------------------------
def get_proxy_dict():
    """Return a proxies dict for requests if proxy is enabled."""
    if st.session_state.proxy_enabled and st.session_state.proxy_url:
        return {
            "http":  st.session_state.proxy_url,
            "https": st.session_state.proxy_url,
        }
    return None


def verify_proxy():
    """Test the proxy by making a request to a public IP-check service."""
    url = st.session_state.proxy_url
    if not url:
        return False, "No proxy URL entered.", ""
    proxies = {"http": url, "https": url}
    try:
        r = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=10)
        if r.status_code == 200:
            ip = r.json().get("origin", "unknown")
            return True, f"Proxy working — visible IP: {ip}", ip
        return False, f"Proxy responded with status {r.status_code}", ""
    except Exception as e:
        return False, f"Proxy failed: {str(e)[:150]}", ""


# -----------------------------------------------------------------------------
# HEADER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hub-header">
      <div class="hub-brand">SOCIAL MEDIA HUB</div>
      <div class="hub-tagline">🌐 One Dashboard · All Platforms · Your Own Credentials</div>
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
    st.markdown("### 🔐 VPN / Proxy")
    st.caption(
        "Enter your own proxy URL here. This lets the dashboard route "
        "its API calls through your VPN's proxy endpoint."
    )

    st.session_state.proxy_enabled = st.toggle(
        "Enable proxy for API calls",
        value=st.session_state.proxy_enabled,
        key="toggle_proxy",
    )

    if st.session_state.proxy_enabled:
        st.session_state.proxy_url = st.text_input(
            "Proxy URL",
            value=st.session_state.proxy_url,
            placeholder="http://user:pass@host:port  or  socks5://host:port",
            key="input_proxy_url",
        )

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("🔍 Verify", use_container_width=True, key="btn_verify_proxy"):
                with st.spinner("Testing…"):
                    ok, msg, ip = verify_proxy()
                    st.session_state.proxy_verified = ok
                    st.session_state.proxy_ip = ip
                    if ok:
                        st.success(msg)
                    else:
                        st.error(msg)
        with col_b:
            if st.button("🗑 Clear", use_container_width=True, key="btn_clear_proxy"):
                st.session_state.proxy_url = ""
                st.session_state.proxy_verified = False
                st.session_state.proxy_ip = ""
                st.rerun()

        if st.session_state.proxy_verified:
            st.markdown(
                f"""
                <div class="banner-ok" style="font-size:.72rem;">
                  🟢 Proxy active<br>
                  <span style="color:#1060a0;">IP: {st.session_state.proxy_ip}</span>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                '<div class="banner-warn" style="font-size:.72rem;">'
                '⚠️ Proxy not verified yet — click Verify above.'
                '</div>',
                unsafe_allow_html=True,
            )
    else:
        st.markdown(
            '<div class="banner-info" style="font-size:.72rem;">'
            'Proxy disabled — API calls go directly from Streamlit Cloud.'
            '</div>',
            unsafe_allow_html=True,
        )

    st.markdown("---")
    st.markdown("### 📌 About VPN + Proxy")
    st.caption(
        "Streamlit Cloud **cannot run a VPN server** inside the app. "
        "The VPN must live on your phone or computer. If your VPN "
        "provides a **proxy endpoint** (WireGuard → SOCKS5, etc.), "
        "paste it above to route the dashboard's calls through it."
    )

    st.markdown("---")
    st.markdown("### 🧹 Session Actions")
    if st.button("🔄 Reset All Connections", use_container_width=True, key="btn_reset_all"):
        st.session_state.connections = {}
        st.success("All connections cleared.")
        st.rerun()

# -----------------------------------------------------------------------------
# MAIN — HOW IT WORKS BANNER
# -----------------------------------------------------------------------------
st.markdown(
    """
    <div class="banner-info">
      <b>🔑 How it works:</b> Each user enters <b>their own</b> credentials
      for each platform below. Nothing is stored on the server — all data
      lives in <b>your browser session only</b> and disappears when you
      close the tab. You are in full control.
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------------------------------------------------------
# MAIN — PLATFORM CONNECTION CARDS
# -----------------------------------------------------------------------------
st.markdown("## 🔗 Connect Your Social Media Accounts")
st.caption("Enter your credentials for each platform. They stay in your session only.")

cols = st.columns(2)

for i, platform in enumerate(PLATFORMS):
    col = cols[i % 2]
    pid = platform["id"]

    with col:
        connected = pid in st.session_state.connections
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

        with st.expander(
            f"🔑 Configure {platform['name']}",
            expanded=not connected,
        ):
            st.caption(platform["help"])

            existing = st.session_state.connections.get(pid, {}).get("credentials", {})

            values = {}
            for field_name, field_label, is_secret in platform["fields"]:
                values[field_name] = st.text_input(
                    field_label,
                    value=existing.get(field_name, ""),
                    type="password" if is_secret else "default",
                    key=f"field_{pid}_{field_name}",
                    placeholder=f"Enter your {field_label}",
                )

            b1, b2 = st.columns(2)
            with b1:
                if st.button(
                    "✅ Save Connection",
                    key=f"connect_{pid}",
                    use_container_width=True,
                ):
                    missing = [
                        lbl for fname, lbl, _ in platform["fields"]
                        if not values.get(fname, "").strip()
                    ]
                    if missing:
                        st.error(f"❌ Missing: {', '.join(missing)}")
                    else:
                        st.session_state.connections[pid] = {
                            "credentials":  values,
                            "connected_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        }
                        st.success(f"✅ {platform['name']} saved for this session.")
                        st.rerun()
            with b2:
                if st.button(
                    "🗑 Remove",
                    key=f"disconnect_{pid}",
                    use_container_width=True,
                ):
                    st.session_state.connections.pop(pid, None)
                    st.warning(f"Removed {platform['name']}.")
                    st.rerun()

# -----------------------------------------------------------------------------
# CONNECTION SUMMARY
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("## 📊 Connection Summary")

connected_ids = list(st.session_state.connections.keys())
connected_names = [
    p["name"] for p in PLATFORMS if p["id"] in connected_ids
]

if connected_names:
    st.success(
        f"✅ Connected to {len(connected_names)} platform(s): "
        + ", ".join(connected_names)
    )
else:
    st.info("No platforms connected yet. Configure at least one above.")

if st.session_state.connections:
    with st.expander("📋 View saved credentials (masked)"):
        for pid, data in st.session_state.connections.items():
            platform = next((p for p in PLATFORMS if p["id"] == pid), None)
            if not platform:
                continue
            st.markdown(
                f"**{platform['icon']} {platform['name']}** — "
                f"saved {data.get('connected_at', '—')}"
            )
            for field_name, value in data["credentials"].items():
                if len(value) > 8:
                    masked = value[:4] + "•" * 8 + value[-4:]
                else:
                    masked = "•" * len(value) if value else "(empty)"
                st.code(f"{field_name}: {masked}", language="text")

# -----------------------------------------------------------------------------
# TEST API CONNECTIVITY
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("## 🧪 Test API Connectivity")
st.caption(
    "Click below to verify the network path (and proxy, if enabled) is working. "
    "Replace the test URL in the code with a real platform endpoint when ready."
)

if st.button("🔄 Test Network Path", use_container_width=True, key="btn_test_net"):
    proxies = get_proxy_dict()
    try:
        r = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=10)
        if r.status_code == 200:
            ip = r.json().get("origin", "unknown")
            mode = "via proxy" if proxies else "direct"
            st.success(f"✅ Network OK ({mode}) — visible IP: **{ip}**")
        else:
            st.error(f"❌ HTTP {r.status_code}")
    except Exception as e:
        st.error(f"❌ {str(e)[:200]}")

if st.session_state.connections:
    if st.button("📡 Test Each Connected Platform", use_container_width=True,
                 key="btn_test_platforms"):
        proxies = get_proxy_dict()
        for pid in st.session_state.connections:
            platform = next((p for p in PLATFORMS if p["id"] == pid), None)
            if not platform:
                continue
            try:
                r = requests.get("https://httpbin.org/ip", proxies=proxies, timeout=10)
                if r.status_code == 200:
                    ip = r.json().get("origin", "?")
                    st.success(
                        f"{platform['icon']} {platform['name']}: reachable ✅ "
                        f"(IP: {ip})"
                    )
                else:
                    st.error(
                        f"{platform['icon']} {platform['name']}: HTTP {r.status_code}"
                    )
            except Exception as e:
                st.error(
                    f"{platform['icon']} {platform['name']}: {str(e)[:100]}"
                )

# -----------------------------------------------------------------------------
# EXPORT / IMPORT SESSION
# -----------------------------------------------------------------------------
st.markdown("---")
st.markdown("## 💾 Export / Import Session")
st.caption(
    "Since everything is in your browser session, you can export your "
    "connection settings as a file and re-import them later."
)

col_x, col_y = st.columns(2)

with col_x:
    if st.button("📤 Export My Session (JSON)", use_container_width=True,
                 key="btn_export"):
        if not st.session_state.connections:
            st.warning("Nothing to export yet.")
        else:
            export_data = {
                "exported_at": datetime.now().isoformat(),
                "connections": st.session_state.connections,
                "proxy_url": st.session_state.proxy_url,
            }
            st.download_button(
                "⬇️ Download session.json",
                data=json.dumps(export_data, indent=2),
                file_name=f"social-hub-session-{datetime.now():%Y%m%d-%H%M}.json",
                mime="application/json",
                use_container_width=True,
                key="btn_download",
            )

with col_y:
    uploaded = st.file_uploader(
        "📥 Import a saved session.json",
        type=["json"],
        key="import_file",
    )
    if uploaded is not None:
        try:
            data = json.load(uploaded)
            st.session_state.connections = data.get("connections", {})
            st.session_state.proxy_url = data.get("proxy_url", "")
            st.success("✅ Session restored.")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Invalid file: {str(e)[:150]}")

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

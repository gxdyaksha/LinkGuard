
import re
import ipaddress
from datetime import datetime
from urllib.parse import urlparse, unquote
from html import escape

import pandas as pd
import streamlit as st


# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="LinkGuard | Security Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ======================================================
# PROFESSIONAL UI
# ======================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --bg: #f5f7fc;
    --surface: #ffffff;
    --text: #18243a;
    --muted: #718096;
    --border: #e5eaf3;
    --primary: #315efb;
    --navy: #101b35;
}

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background: var(--bg) !important;
    color: var(--text) !important;
}

.block-container {
    max-width: 1500px;
    padding: 1.8rem 2.2rem 3rem;
}

/* Sidebar */

[data-testid="stSidebar"] {
    background: var(--navy) !important;
}

[data-testid="stSidebar"] * {
    color: #edf2ff;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    color: #c5d0e5;
}

[data-testid="stSidebar"] hr {
    border-color: #30405f;
}

.sidebar-brand {
    font-size: 29px;
    font-weight: 800;
    letter-spacing: -1px;
    color: #ffffff;
    margin-bottom: 2px;
}

.sidebar-brand span {
    color: #78a1ff;
}

.sidebar-subtitle {
    font-size: 11px;
    letter-spacing: 1.2px;
    color: #aab9d5;
    text-transform: uppercase;
    margin-bottom: 25px;
}

.sidebar-label {
    color: #8fa6ce;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin: 18px 0 10px;
}

/* Hero */

.hero {
    position: relative;
    overflow: hidden;
    background: linear-gradient(120deg, #101f42 0%, #2048bc 58%, #477cff 100%);
    border-radius: 22px;
    padding: 35px;
    margin-bottom: 28px;
    box-shadow: 0 12px 35px rgba(34, 73, 180, 0.14);
}

.hero-eyebrow {
    color: #c9d8ff;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 13px;
}

.hero-title {
    color: #ffffff !important;
    font-size: 34px;
    font-weight: 800;
    line-height: 1.25;
    letter-spacing: -1.2px;
    margin: 0 0 12px;
}

.hero-description {
    color: #e1eaff !important;
    font-size: 13px;
    line-height: 1.9;
    max-width: 760px;
    margin: 0;
}

.hero-badge {
    display: inline-block;
    margin-top: 20px;
    padding: 7px 12px;
    background: rgba(255,255,255,0.12);
    border: 1px solid rgba(255,255,255,0.22);
    border-radius: 100px;
    color: #ffffff !important;
    font-size: 11px;
    font-weight: 600;
}

/* Typography */

.section-heading {
    color: #17243b !important;
    font-size: 21px;
    font-weight: 800;
    letter-spacing: -0.5px;
    margin: 27px 0 5px;
}

.section-description {
    color: #738198 !important;
    font-size: 12px;
    line-height: 1.8;
    margin-bottom: 18px;
}

.small-label {
    color: #718096 !important;
    font-size: 11px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.7px;
}

/* Dashboard cards */

.dashboard-card {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 17px;
    padding: 21px;
    min-height: 125px;
    box-shadow: 0 3px 12px rgba(24,36,58,0.025);
}

.card-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 15px;
}

.card-label {
    color: #718096 !important;
    font-size: 12px;
    font-weight: 600;
}

.card-number {
    color: #17243b !important;
    font-size: 30px;
    font-weight: 800;
    letter-spacing: -1px;
}

.card-note {
    color: #8793a7 !important;
    font-size: 11px;
    margin-top: 5px;
}

/* Scanner panel */

.scanner-panel {
    background: #ffffff;
    border: 1px solid var(--border);
    border-radius: 19px;
    padding: 24px;
    box-shadow: 0 4px 16px rgba(24,36,58,0.025);
}

.scanner-overline {
    color: #315efb !important;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.6px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.scanner-heading {
    color: #17243b !important;
    font-size: 20px;
    font-weight: 800;
    margin-bottom: 5px;
}

.scanner-description {
    color: #718096 !important;
    font-size: 12px;
    line-height: 1.8;
    margin-bottom: 15px;
}

/* Input visibility */

[data-testid="stMain"] input {
    background: #ffffff !important;
    color: #17243b !important;
    border: 1px solid #dbe3f0 !important;
    border-radius: 10px !important;
    min-height: 45px;
}

[data-testid="stMain"] input::placeholder {
    color: #98a3b6 !important;
}

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #35435b !important;
    font-weight: 600 !important;
}

/* Buttons */

div.stButton > button,
div.stDownloadButton > button {
    border-radius: 10px !important;
    min-height: 43px;
    font-weight: 700 !important;
    transition: all 0.2s ease;
}

div.stButton > button[kind="primary"] {
    background: #315efb !important;
    border: 1px solid #315efb !important;
    color: #ffffff !important;
}

div.stButton > button[kind="primary"]:hover {
    background: #2349d4 !important;
    border-color: #2349d4 !important;
}

div.stDownloadButton > button {
    background: #ffffff !important;
    color: #315efb !important;
    border: 1px solid #d5def0 !important;
}

/* Native metric visibility */

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e5eaf3;
    border-radius: 15px;
    padding: 17px;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] p {
    color: #718096 !important;
}

[data-testid="stMetricValue"],
[data-testid="stMetricValue"] div {
    color: #17243b !important;
}

/* Result cards */

.result-panel {
    background: #ffffff;
    border: 1px solid #e5eaf3;
    border-radius: 17px;
    padding: 23px;
    margin: 12px 0;
}

.result-title {
    color: #17243b !important;
    font-size: 16px;
    font-weight: 800;
    margin-bottom: 15px;
}

.risk-badge {
    display: inline-block;
    padding: 7px 13px;
    border-radius: 30px;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 0.5px;
}

.finding-card {
    background: #ffffff;
    border: 1px solid #e5eaf3;
    border-radius: 12px;
    padding: 17px;
    margin-bottom: 10px;
}

.finding-heading {
    color: #17243b !important;
    font-size: 13px;
    font-weight: 750;
    margin-bottom: 7px;
}

.finding-description {
    color: #718096 !important;
    font-size: 12px;
    line-height: 1.8;
}

.finding-points {
    color: #315efb !important;
    font-size: 11px;
    font-weight: 700;
}

/* Feature cards */

.feature-card {
    background: #ffffff;
    border: 1px solid #e5eaf3;
    border-radius: 16px;
    padding: 22px;
    min-height: 165px;
}

.feature-number {
    color: #315efb !important;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 15px;
}

.feature-heading {
    color: #17243b !important;
    font-size: 14px;
    font-weight: 800;
    margin-bottom: 9px;
}

.feature-description {
    color: #718096 !important;
    font-size: 12px;
    line-height: 1.8;
}

/* Alerts */

[data-testid="stAlert"] {
    border-radius: 12px;
}

[data-testid="stAlert"] p {
    color: #243149 !important;
}

/* Data tables */

[data-testid="stDataFrame"] {
    background: #ffffff;
    border: 1px solid #e5eaf3;
    border-radius: 12px;
}

/* Footer */

.footer {
    text-align: center;
    padding-top: 23px;
    margin-top: 38px;
    border-top: 1px solid #e0e7f1;
    color: #7b879a !important;
    font-size: 11px;
    line-height: 2;
}

/* Responsive */

@media (max-width: 768px) {
    .block-container {
        padding: 1rem;
    }

    .hero {
        padding: 24px;
    }

    .hero-title {
        font-size: 26px;
    }

    .dashboard-card {
        padding: 15px;
    }
}
</style>
""", unsafe_allow_html=True)


# ======================================================
# SCANNER RULES
# ======================================================

SHORTENERS = {
    "bit.ly", "tinyurl.com", "t.co", "is.gd",
    "cutt.ly", "rb.gy", "shorturl.at", "rebrand.ly",
    "ow.ly", "buff.ly", "tiny.cc"
}

SUSPICIOUS_WORDS = {
    "login": 5,
    "verify": 5,
    "verification": 5,
    "password": 5,
    "account": 3,
    "secure": 3,
    "update": 3,
    "banking": 5,
    "wallet": 5,
    "crypto": 3,
    "free": 2,
    "gift": 3,
    "prize": 3,
    "claim": 3,
    "signin": 5,
    "confirm": 3,
    "suspended": 5,
    "urgent": 3,
}


# ======================================================
# SESSION STATE
# ======================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "last_result" not in st.session_state:
    st.session_state.last_result = None


# ======================================================
# URL VALIDATION
# ======================================================

def validate_url(raw_url):
    raw_url = raw_url.strip()

    if not raw_url:
        raise ValueError("Enter a URL before starting the scan.")

    if len(raw_url) > 2048:
        raise ValueError("URL is too long. Maximum length is 2048 characters.")

    if any(ord(char) < 32 for char in raw_url):
        raise ValueError("URL contains invalid control characters.")

    if any(char.isspace() for char in raw_url):
        raise ValueError("URL cannot contain spaces.")

    if raw_url.startswith("//"):
        raw_url = "https:" + raw_url
    elif not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", raw_url):
        raw_url = "https://" + raw_url

    parsed = urlparse(raw_url)

    if parsed.scheme.lower() not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs are supported.")

    if not parsed.hostname:
        raise ValueError("Invalid URL. Enter a valid domain.")

    try:
        hostname = parsed.hostname.encode("idna").decode("ascii").lower()
        port = parsed.port
    except (UnicodeError, ValueError):
        raise ValueError("The URL contains an invalid hostname or port.")

    if port is not None and not 1 <= port <= 65535:
        raise ValueError("Port must be between 1 and 65535.")

    try:
        ipaddress.ip_address(hostname)
        is_ip = True
    except ValueError:
        is_ip = False

    if not is_ip:
        labels = hostname.rstrip(".").split(".")

        for label in labels:
            if (
                not label
                or len(label) > 63
                or label.startswith("-")
                or label.endswith("-")
                or not re.fullmatch(r"[a-z0-9-]+", label)
            ):
                raise ValueError("Invalid hostname format.")

    return raw_url, parsed, hostname, is_ip


# ======================================================
# URL ANALYSIS
# ======================================================

def analyze_url(raw_url):
    original, parsed, hostname, is_ip = validate_url(raw_url)

    score = 0
    findings = []

    def add_finding(title, description, points):
        nonlocal score
        score += points
        findings.append({
            "Finding": title,
            "Description": description,
            "Points": points,
        })

    scheme = parsed.scheme.lower()
    decoded_url = unquote(original)

    if scheme == "http":
        add_finding(
            "Unencrypted HTTP",
            "The URL uses HTTP instead of HTTPS.",
            15,
        )

    if is_ip:
        add_finding(
            "IP address hostname",
            "The URL uses an IP address instead of a conventional domain name.",
            25,
        )

    if "@" in parsed.netloc:
        add_finding(
            "At-sign in URL authority",
            "The at-sign may make the actual destination hostname confusing.",
            25,
        )

    if hostname in SHORTENERS:
        add_finding(
            "URL shortener",
            "The shortened link hides its final destination.",
            15,
        )

    if "xn--" in hostname:
        add_finding(
            "Punycode hostname",
            "The hostname contains an encoded internationalized domain label.",
            20,
        )

    if len(hostname) > 50:
        add_finding(
            "Long hostname",
            "An unusually long hostname can make a destination harder to recognize.",
            10,
        )

    if len(hostname.rstrip(".").split(".")) >= 5:
        add_finding(
            "Multiple subdomains",
            "The hostname has many labels and may be harder to interpret.",
            10,
        )

    if parsed.port is not None and parsed.port not in {80, 443}:
        add_finding(
            "Non-standard port",
            f"The URL uses port {parsed.port}.",
            10,
        )

    if len(original) > 150:
        add_finding(
            "Very long URL",
            "Long URLs can obscure important parts of the destination.",
            10,
        )

    if re.search(r"%[0-9a-fA-F]{2}", original):
        add_finding(
            "Encoded characters",
            "The URL contains percent-encoded characters.",
            5,
        )

    matched_words = []

    for word, points in SUSPICIOUS_WORDS.items():
        pattern = rf"(?<![a-z0-9]){re.escape(word)}(?![a-z0-9])"

        if re.search(pattern, decoded_url, re.IGNORECASE):
            matched_words.append((word, points))

    if matched_words:
        word_score = min(20, sum(points for _, points in matched_words))
        word_names = ", ".join(word for word, _ in matched_words)

        add_finding(
            "Potentially suspicious keywords",
            f"Detected terms: {word_names}. These words alone do not prove malicious activity.",
            word_score,
        )

    if hostname.count("-") >= 4:
        add_finding(
            "Multiple hyphens",
            "Inspect the hostname carefully for possible impersonation.",
            5,
        )

    score = min(score, 100)

    if score >= 50:
        risk = "High"
    elif score >= 25:
        risk = "Medium"
    else:
        risk = "Low"

    if not findings:
        findings.append({
            "Finding": "No configured warning patterns detected",
            "Description": "No configured rules matched. This does not guarantee that the URL is safe.",
            "Points": 0,
        })

    return {
        "Scanned At": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Original URL": original,
        "Hostname": hostname,
        "Protocol": scheme.upper(),
        "Risk Score": score,
        "Risk Level": risk,
        "Findings Count": sum(1 for item in findings if item["Points"] > 0),
        "Findings": findings,
    }


# ======================================================
# REPORT HELPERS
# ======================================================

def build_dataframe(results):
    rows = []

    for result in results:
        rows.append({
            "Scanned At": result["Scanned At"],
            "URL": result["Original URL"],
            "Hostname": result["Hostname"],
            "Protocol": result["Protocol"],
            "Risk Score": result["Risk Score"],
            "Risk Level": result["Risk Level"],
            "Warnings": result["Findings Count"],
            "Findings": " | ".join(
                item["Finding"] for item in result["Findings"]
            ),
        })

    return pd.DataFrame(rows)


# ======================================================
# SIDEBAR
# ======================================================

with st.sidebar:
    st.markdown(
        '<div class="sidebar-brand">Link<span>Guard</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="sidebar-subtitle">Security Intelligence</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown(
        '<div class="sidebar-label">Platform</div>',
        unsafe_allow_html=True,
    )

    st.write("🛡️ URL Security Scanner")
    st.write("📊 Risk Analysis")
    st.write("📄 Report Generation")

    st.divider()

    st.markdown(
        '<div class="sidebar-label">System Status</div>',
        unsafe_allow_html=True,
    )

    st.success("Scanner ready")

    st.caption("Version 1.0.0")

    st.divider()

    st.markdown(
        '<div class="sidebar-label">About</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "LinkGuard identifies suspicious URL patterns using "
        "local rules. It does not open the target URL or query "
        "a live phishing database."
    )


# ======================================================
# HERO
# ======================================================

st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">URL THREAT AWARENESS PLATFORM</div>
    <div class="hero-title">Security Intelligence Dashboard</div>
    <p class="hero-description">
        Examine suspicious URLs, understand potential security indicators,
        and generate clear scan reports through a simple security dashboard.
    </p>
    <div class="hero-badge">● &nbsp; RULE-BASED SCANNING ENABLED</div>
</div>
""", unsafe_allow_html=True)


# ======================================================
# OVERVIEW
# ======================================================

history = st.session_state.history

total = len(history)
high = sum(item["Risk Level"] == "High" for item in history)
medium = sum(item["Risk Level"] == "Medium" for item in history)
low = sum(item["Risk Level"] == "Low" for item in history)

st.markdown(
    '<div class="section-heading">Security Overview</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">Monitor the results of your current session.</div>',
    unsafe_allow_html=True,
)

cards = [
    ("TOTAL SCANS", total, "URLs analyzed"),
    ("HIGH RISK", high, "High-risk classifications"),
    ("MEDIUM RISK", medium, "Needs closer inspection"),
    ("LOW RISK", low, "Fewer warning indicators"),
]

cols = st.columns(4)

for col, (label, value, note) in zip(cols, cards):
    with col:
        st.markdown(
            f"""
            <div class="dashboard-card">
                <div class="card-top">
                    <div class="card-label">{label}</div>
                </div>
                <div class="card-number">{value}</div>
                <div class="card-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ======================================================
# SCANNER
# ======================================================

st.markdown(
    '<div class="section-heading">URL Security Scanner</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">Enter the URL you want to inspect.</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    st.markdown(
        '<div class="scanner-overline">NEW SECURITY SCAN</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="scanner-heading">Analyze a website URL</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="scanner-description">'
        'The scanner checks URL structure and configured warning patterns. '
        'It does not open the destination website.'
        '</div>',
        unsafe_allow_html=True,
    )

    url_input = st.text_input(
        "Website URL",
        placeholder="https://example.com",
        key="url_input",
    )

    button_col, clear_col = st.columns([3, 1])

    with button_col:
        scan_clicked = st.button(
            "🔎  Analyze URL",
            type="primary",
            use_container_width=True,
        )

    with clear_col:
        clear_clicked = st.button(
            "Clear Input",
            use_container_width=True,
        )

if clear_clicked:
    st.session_state.url_input = ""
    st.rerun()

if scan_clicked:
    if not url_input.strip():
        st.session_state.last_result = None
        st.error("Enter a URL before starting the scan.")
    else:
        try:
            result = analyze_url(url_input)

            st.session_state.last_result = result
            st.session_state.history.insert(0, result)
            st.session_state.history = st.session_state.history[:100]

            st.success("URL analysis completed successfully.")

        except ValueError as error:
            st.session_state.last_result = None
            st.error(str(error))


# ======================================================
# RESULTS
# ======================================================

result = st.session_state.last_result

if result:
    st.markdown(
        '<div class="section-heading">Analysis Report</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">Review the risk assessment and detected indicators.</div>',
        unsafe_allow_html=True,
    )

    score_col, risk_col, warning_col = st.columns(3)

    with score_col:
        st.metric("Risk Score", f'{result["Risk Score"]} / 100')

    with risk_col:
        st.metric("Risk Classification", result["Risk Level"])

    with warning_col:
        st.metric("Warning Patterns", result["Findings Count"])

    st.progress(result["Risk Score"] / 100)

    risk_styles = {
        "Low": ("#15803d", "#dcfce7"),
        "Medium": ("#a16207", "#fef3c7"),
        "High": ("#b91c1c", "#fee2e2"),
    }

    risk_color, risk_bg = risk_styles[result["Risk Level"]]

    st.markdown(
        f"""
        <div class="result-panel">
            <div class="small-label">SCAN CLASSIFICATION</div>
            <br>
            <span class="risk-badge"
                style="color:{risk_color};background:{risk_bg};">
                {escape(result["Risk Level"].upper())} RISK
            </span>
            <br><br>
            <div class="result-title">{escape(result["Hostname"])}</div>
            <div class="finding-description">
                Protocol: {escape(result["Protocol"])} &nbsp; | &nbsp;
                Scanned: {escape(result["Scanned At"])}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if result["Risk Level"] == "High":
        st.error(
            "Multiple warning indicators were found. Verify the destination "
            "independently before interacting with it."
        )
    elif result["Risk Level"] == "Medium":
        st.warning(
            "Some warning indicators were found. Review the details below."
        )
    else:
        st.info(
            "Few configured warning indicators were found. This does not "
            "guarantee that the website is safe."
        )

    st.markdown(
        '<div class="section-heading">Detected Indicators</div>',
        unsafe_allow_html=True,
    )

    for finding in result["Findings"]:
        st.markdown(
            f"""
            <div class="finding-card">
                <div class="finding-heading">
                    {escape(finding["Finding"])}
                    <span class="finding-points" style="float:right;">
                        +{finding["Points"]} points
                    </span>
                </div>
                <div class="finding-description">
                    {escape(finding["Description"])}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    report = build_dataframe([result])

    st.download_button(
        "Download Scan Report (CSV)",
        data=report.to_csv(index=False).encode("utf-8-sig"),
        file_name="linkguard_scan_report.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ======================================================
# HISTORY
# ======================================================

st.markdown(
    '<div class="section-heading">Recent Scan History</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">Your latest scans in this browser session.</div>',
    unsafe_allow_html=True,
)

history = st.session_state.history

if history:
    history_df = build_dataframe(history)

    st.dataframe(
        history_df[
            [
                "Scanned At",
                "URL",
                "Hostname",
                "Risk Score",
                "Risk Level",
                "Warnings",
            ]
        ],
        use_container_width=True,
        hide_index=True,
    )

    export_col, clear_history_col = st.columns([3, 1])

    with export_col:
        st.download_button(
            "Export Complete History",
            data=history_df.to_csv(index=False).encode("utf-8-sig"),
            file_name="linkguard_history.csv",
            mime="text/csv",
            use_container_width=True,
        )

    with clear_history_col:
        if st.button("Clear History", use_container_width=True):
            st.session_state.history = []
            st.session_state.last_result = None
            st.rerun()
else:
    st.info("No scans yet. Run your first URL analysis above.")


# ======================================================
# FEATURES
# ======================================================

st.markdown(
    '<div class="section-heading">Platform Capabilities</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="section-description">Tools available in this version of LinkGuard.</div>',
    unsafe_allow_html=True,
)

features = [
    (
        "01",
        "Pattern Detection",
        "Examines URL structure, protocol, IP addresses, shorteners, "
        "encoding, subdomains, and selected suspicious words.",
    ),
    (
        "02",
        "Risk Assessment",
        "Combines configured indicators into a score from 0 to 100 "
        "and a Low, Medium, or High classification.",
    ),
    (
        "03",
        "Security Reporting",
        "Exports scan findings and session history to CSV files "
        "for further review.",
    ),
]

feature_cols = st.columns(3)

for col, (number, title, description) in zip(feature_cols, features):
    with col:
        st.markdown(
            f"""
            <div class="feature-card">
                <div class="feature-number">{number} / CAPABILITY</div>
                <div class="feature-heading">{title}</div>
                <div class="feature-description">{description}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


# ======================================================
# FOOTER
# ======================================================

st.markdown("""
<div class="footer">
    <strong>LinkGuard Security Intelligence</strong><br>
    Educational URL awareness tool · Version 1.0.0<br>
    Rule-based analysis only. A low risk score does not establish that a URL is safe.
    No live phishing or malware database is connected.
</div>
""", unsafe_allow_html=True)


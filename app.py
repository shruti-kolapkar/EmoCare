import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import requests
import time
from datetime import datetime

# ===== ADDITION IMPORTS =====
from streamlit.components.v1 import html

# ✅ EMAIL IMPORTS
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# ================= CONFIGURATION =================
CHANNEL_ID = "3235363"
READ_API_KEY = "ZOCWKX4HFY1CORAL"
URL = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json?api_key={READ_API_KEY}&results=50"

# ===== ESP32-CAM LIVE STREAM CONFIG =====
ESP32_CAM_URL = "http://10.251.166.85:81/stream"


# ================= ALERT BEEP FUNCTION =================
def play_beep():
    beep_html = """
    <audio autoplay>
        <source src="https://www.soundjay.com/buttons/sounds/beep-07.mp3" type="audio/mpeg">
    </audio>
    """
    st.markdown(beep_html, unsafe_allow_html=True)


# ================= EMAIL ALERT FUNCTION =================
def send_email_alert(recipient_email, patient_name, stress_level, nurse_name):

    try:
        sender_email = "sidranjane27@gmail.com"

        # ⚠️ Gmail App Password (Keep Secret)
        sender_password = "xzyh jkdc hmlm jwcq"

        message = MIMEMultipart("alternative")
        message["Subject"] = f"🚨 HIGH STRESS ALERT - Patient: {patient_name}"
        message["From"] = sender_email
        message["To"] = recipient_email

        html_body = f"""
        <html>
        <body style="font-family: Arial;">
            <h2 style="color:red;">⚠️ HIGH STRESS ALERT</h2>
            <p><b>Patient:</b> {patient_name}</p>
            <p><b>Stress Level:</b> {stress_level}%</p>
            <p><b>Nurse:</b> {nurse_name}</p>
            <p><b>Time:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <hr>
            <p>Please attend immediately.</p>
        </body>
        </html>
        """

        message.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, message.as_string())

        return True

    except Exception as e:
        st.error("❌ Email Failed: " + str(e))
        return False


# ================= UI CONFIGURATION =================
st.set_page_config(page_title="Stress-Sync Pro | Medical Dashboard",
                   layout="wide", page_icon="🧬")

# ADVANCED CUSTOM CSS FOR UI ENHANCEMENT
st.markdown("""
    <style>
    /* Dark Theme Background */
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); color: white; }

    /* Custom Card Styling */
    div[data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }

    /* Metrics Highlighting */
    div[data-testid="stMetricValue"] { color: #38bdf8 !important; font-weight: 700; }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] { background-color: #0f172a !important; border-right: 1px solid #334155; }

    /* Status Badge */
    .status-badge {
        padding: 5px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
        background: rgba(34, 197, 94, 0.2);
        color: #4ade80;
        border: 1px solid #4ade80;
    }
    </style>
    """, unsafe_allow_html=True)


# ================= DATA PROCESSING =================
def get_data():
    try:
        response = requests.get(URL, timeout=5)
        data = response.json()
        df = pd.DataFrame(data['feeds'])

        field_map = {
            'field1': 'BPM', 'field2': 'Temp', 'field3': 'GSR_Raw',
            'field4': 'GSR_Delta', 'field5': 'Stress',
            'field6': 'HRV', 'field7': 'Resp'
        }

        df.rename(columns=field_map, inplace=True)

        for col in field_map.values():
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['created_at'] = pd.to_datetime(df['created_at']).dt.tz_convert('Asia/Kolkata')
        return df

    except:
        return pd.DataFrame()


# ================= SIDEBAR & NAVIGATION =================
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2966/2966327.png", width=80)
    st.title("System Control")
    st.info(f"**Device ID:** ESP32_TRK_01\n\n**Channel:** {CHANNEL_ID}")
    st.divider()

    st.write("### ⚙️ Threshold Settings")
    hr_limit = st.slider("BPM Alert Threshold", 60, 150, 100)
    stress_limit = st.slider("Stress Alert Threshold", 40, 100, 75)

    # ✅ EXACT DROPDOWN UI LIKE YOUR SCREENSHOT
    with st.expander("👩‍⚕️ Nurse Alert System"):

        patient_name = st.text_input("Patient Name", value="Jake Paul")
        nurse_name = st.text_input("Nurse Name", value="Aishwarya")
        nurse_email = st.text_input("Nurse Email", value="aaryafalle@gmail.com")
        nurse_phone = st.text_input("Nurse Phone (SMS)", value="8999035781")

        st.write("**Alert Method Preferences:**")
        col_email, col_sms = st.columns(2)

        with col_email:
            enable_email = st.checkbox("📧 Email Alerts", value=True)

        with col_sms:
            enable_sms = st.checkbox("📱 SMS Alerts", value=False)

        enable_alerts = st.toggle("Enable Remote Alerts", value=True)

        alert_cooldown = st.slider("Alert Cooldown (minutes)", 1, 60, 5)

    st.write("### 🕒 Last Sync")
    st.write(datetime.now().strftime("%H:%M:%S"))

    if st.button("Force Manual Refresh"):
        st.rerun()


# ================= MAIN DASHBOARD =================
data = get_data()

if not data.empty:
    latest = data.iloc[-1]
    prev = data.iloc[-2] if len(data) > 1 else latest

    ALERT_TRIGGERED = False

    # ================= STRESS ALERT + EMAIL =================
    if latest['Stress'] >= stress_limit:
        ALERT_TRIGGERED = True

        if enable_alerts:

            if "last_alert_time" not in st.session_state:
                st.session_state.last_alert_time = 0

            current_time = time.time()
            cooldown_seconds = alert_cooldown * 60

            if current_time - st.session_state.last_alert_time > cooldown_seconds:

                if enable_email:
                    send_email_alert(
                        nurse_email,
                        patient_name,
                        int(latest['Stress']),
                        nurse_name
                    )
                    st.toast("📩 Nurse Email Alert Sent!", icon="🚨")

                if enable_sms:
                    st.toast("📱 SMS Alert (Twilio not configured)", icon="⚠️")

                st.session_state.last_alert_time = current_time

    # ================= HEADER SECTION =================
    head_left, head_right = st.columns([3, 1])

    with head_left:
        st.markdown(
            f"<h1>Bio-Metric Intelligence <span class='status-badge'>LIVE FEED</span></h1>",
            unsafe_allow_html=True)

    with head_right:
        st.markdown(f"**Last Update:** {latest['created_at'].strftime('%H:%M:%S')}")

    # ================= KPI ROW =================
    st.write("")
    kpi1, kpi2, kpi3, kpi4 = st.columns(4)

    kpi1.metric("❤️ Heart Rate", f"{latest['BPM']} BPM", f"{latest['BPM']-prev['BPM']} bpm")
    kpi2.metric("🌡️ Body Temp", f"{latest['Temp']}°C", f"{round(latest['Temp']-prev['Temp'], 1)}°C")
    kpi3.metric("🌬️ Respiration", f"{latest['Resp']} RPM")
    kpi4.metric("📈 HRV Stability", f"{latest['HRV']}ms")

    st.divider()

    # ================= LIVE CAMERA =================
    
    #st.subheader("📹 Live Patient Monitoring")
    #html(f"""
     #   <iframe src="{ESP32_CAM_URL}"
     ##   width="100%" height="420"
     #   frameborder="0" allowfullscreen></iframe>
    #""")
    
    # ================= ROW 2: ANALYSIS =================
    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.subheader("📊 Vital Signs Trend Analysis")
        fig = px.line(
            data, x='created_at', y=['BPM', 'Stress', 'Resp'],
            color_discrete_sequence=["#38bdf8", "#fb7185", "#34d399"],
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_side:
        st.subheader("🧠 Current Mental Load")

        if ALERT_TRIGGERED:
            st.error("🚨 HIGH STRESS DETECTED — Nurse Alert Triggered")
            play_beep()

        stress_score = latest['Stress']

        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=stress_score,
            gauge={'axis': {'range': [0, 100]}}
        ))

        st.plotly_chart(fig_gauge, use_container_width=True)

    # ================= ROW 3 =================
    st.divider()
    bot_l, bot_r = st.columns([1, 1])

    with bot_l:
        st.subheader("⚡ Electrodermal Activity (GSR)")
        fig_gsr = px.area(data, x='created_at', y='GSR_Raw',
                          color_discrete_sequence=['#38bdf8'])
        st.plotly_chart(fig_gsr, use_container_width=True)

    with bot_r:
        st.subheader("📋 Recent Bio-Logs")
        st.dataframe(
            data[['created_at', 'BPM', 'Stress', 'HRV', 'Resp']].tail(8),
            use_container_width=True,
            hide_index=True
        )

else:
    st.warning("🔄 Connecting to ThingSpeak Cloud... Please ensure device is transmitting.")

# ================= AUTO REFRESH =================
time.sleep(15)
st.rerun()
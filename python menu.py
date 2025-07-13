import streamlit as st

# ---- CONFIG (MUST BE FIRST STREAMLIT COMMAND) ----
st.set_page_config(
    page_title="Unified Social Media Toolkit", 
    page_icon="🌐", 
    layout="centered",
    initial_sidebar_state="expanded"
)

from twilio.rest import Client
import urllib.parse
import tweepy
import smtplib
from email.mime.text import MIMEText
import pywhatkit as kit
import requests
from PIL import Image
import base64


def set_background(image_file):
    """
    This function sets the background of a Streamlit app to an image specified by the given image file.
    """
    with open(image_file, "rb") as f:
        img_data = f.read()
    b64_encoded = base64.b64encode(img_data).decode()
    style = f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{b64_encoded});
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
    """
    st.markdown(style, unsafe_allow_html=True)



st.markdown("""
    <style>
    .card {
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
        background-color: rgba(255, 255, 255, 0.9);
        margin-bottom: 20px;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 10px 24px;
        border: none;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    .sidebar .sidebar-content {
        background-color: rgba(255, 255, 255, 0.9);
    }
    h1, h2, h3 {
        color: #2c3e50;
    }
    </style>
""", unsafe_allow_html=True)

# ---- HEADER ----
st.title("🌐 Unified Social Media Toolkit")
st.markdown("""
    <div style="background-color: rgba(46, 204, 113, 0.7); padding: 15px; border-radius: 10px; margin-bottom: 20px;">
        <h3 style="color: white; text-align: center;">Connect with your audience across all platforms</h3>
    </div>
""", unsafe_allow_html=True)


TWILIO_SID = "Enter your TWILIO SID "
TWILIO_TOKEN = "Enter your TWILIO Token"
TWILIO_PHONE = "Enter your TWILIO phone"

TWITTER_API_KEY = "xxxxxxxxx"
TWITTER_API_SECRET = "xxxxxxxx"
TWITTER_ACCESS_TOKEN = "xxxxxxx"
TWITTER_ACCESS_SECRET = "xxxxxxxx"

EMAIL_FROM = "Enter your email"
EMAIL_PASS = "Enter your email pass"

# ---- MENU ----
menu = st.sidebar.selectbox("📂 Select Tool", [
    "📩 SMS Sender",
    "📞 Voice Call",
    "📸 Instagram Message",
    "🐦 Twitter Poster",
    "📧 Email Sender",
    "💬 WhatsApp Sender",
    "🔗 LinkedIn Auto Poster"
])


st.sidebar.markdown("""
    <div style="padding: 10px; background-color: #2ecc71; border-radius: 5px; margin-bottom: 20px;">
        <h3 style="color: white; text-align: center;">Dashboard</h3>
    </div>
""", unsafe_allow_html=True)

# ---- SMS Sender ----
if menu == "📩 SMS Sender":
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📩 Send SMS using Twilio")
        phone = st.text_input("Recipient Phone Number", "+91")
        message = st.text_area("Message")
        
        if st.button("Send SMS", key="sms_button"):
            try:
                client = Client(TWILIO_SID, TWILIO_TOKEN)
                msg = client.messages.create(body=message, from_=TWILIO_PHONE, to=phone)
                st.success(f"✅ SMS sent! SID: {msg.sid}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# ---- Voice Call ----
elif menu == "📞 Voice Call":
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📞 Make Voice Call using Twilio")
        call_to = st.text_input("Phone Number", "+91")
        voice_msg = st.text_area("Voice Message", "Hello! This is a test call.")
        
        if st.button("Make Call", key="call_button"):
            try:
                client = Client(TWILIO_SID, TWILIO_TOKEN)
                encoded_msg = urllib.parse.quote(f"<Response><Say>{voice_msg}</Say></Response>")
                url = f"http://twimlets.com/echo?Twiml={encoded_msg}"
                call = client.calls.create(to=call_to, from_=TWILIO_PHONE, url=url)
                st.success(f"✅ Call started! SID: {call.sid}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# ---- Instagram Message (Simulated) ----
elif menu == "📸 Instagram Message":
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📸 Simulated Instagram Message")
        st.warning("Instagram API is restricted. This is a simulation.")
        user = st.text_input("Instagram Username")
        msg = st.text_area("Message")
        
        if st.button("Simulate Send", key="ig_button"):
            if user and msg:
                st.success(f"✅ Simulated sending message to @{user}")
            else:
                st.warning("Please fill in all fields.")
        st.markdown('</div>', unsafe_allow_html=True)

# ---- Twitter Poster ----
elif menu == "🐦 Twitter Poster":
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("🐦 Post Tweet")
        tweet = st.text_area("Enter your tweet", max_chars=280)
        
        if st.button("Post Tweet", key="tweet_button"):
            try:
                auth = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET)
                auth.set_access_token(TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET)
                api = tweepy.API(auth)
                api.verify_credentials()
                api.update_status(tweet)
                st.success("✅ Tweet posted!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# ---- Email Sender ----
elif menu == "📧 Email Sender":
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("📧 Send Email via Gmail SMTP")
        to = st.text_input("Recipient Email")
        subject = st.text_input("Subject")
        body = st.text_area("Message Body")
        
        if st.button("Send Email", key="email_button"):
            try:
                msg = MIMEText(body)
                msg['Subject'] = subject
                msg['From'] = EMAIL_FROM
                msg['To'] = to

                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(EMAIL_FROM, EMAIL_PASS)
                    server.sendmail(EMAIL_FROM, to, msg.as_string())

                st.success("✅ Email sent successfully.")
            except Exception as e:
                st.error(f"❌Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# ---- WhatsApp Sender ----
elif menu == "💬 WhatsApp Sender":
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("💬 Send WhatsApp Message using PyWhatKit")
        phone = st.text_input("Phone Number", "+91")
        message = st.text_area("Message")
        
        if st.button("Send WhatsApp Now", key="whatsapp_button"):
            try:
                kit.sendwhatmsg_instantly(phone_no=phone, message=message, wait_time=10, tab_close=True)
                st.success("✅ WhatsApp message sent.")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# ---- LinkedIn Poster ----
elif menu == "🔗 LinkedIn Auto Poster":
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.header("🔗 Auto Post on LinkedIn")
        access_token = st.text_input("Access Token", type="password")
        linkedin_urn = st.text_input("LinkedIn URN (e.g., urn:li:person:xxxx)")
        linkedin_msg = st.text_area("Post Content", "Excited to share my new project!")
        
        if st.button("Post to LinkedIn", key="linkedin_button"):
            try:
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "X-Restli-Protocol-Version": "2.0.0",
                    "Content-Type": "application/json"
                }

                post_data = {
                    "author": linkedin_urn,
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {
                                "text": linkedin_msg
                            },
                            "shareMediaCategory": "NONE"
                        }
                    },
                    "visibility": {
                        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                    }
                }

                res = requests.post('https://api.linkedin.com/v2/ugcPosts', headers=headers, json=post_data)
                if res.status_code == 201:
                    st.success("✅ Posted successfully to LinkedIn!")
                else:
                    st.error(f"❌ Failed. Status Code: {res.status_code}")
                    st.code(res.text)
            except Exception as e:
                st.error(f"❌ Error: {e}")
        st.markdown('</div>', unsafe_allow_html=True)

# ---- FOOTER ----
st.markdown("""
    <div style="text-align: center; padding: 20px; margin-top: 30px; background-color: rgba(44, 62, 80, 0.7); border-radius: 10px;">
        <p style="color: white;">© 2023 Unified Social Media Toolkit | Made with Streamlit</p>
    </div>
""", unsafe_allow_html=True)
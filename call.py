import streamlit as st
from twilio.rest import Client

ACCOUNT_SID = " ENTER YOUR ACCOUNT_SID"
AUTH_TOKEN = " ENTER YOUR AUTH_TOKEN"
TWILIO_PHONE = "‪‬ENTER YOUR TWILIO_PHONE"

st.set_page_config(page_title="📞 Twilio Communication", page_icon="📡", layout="centered")
st.title("📡 Twilio Communication App")

st.sidebar.header("🛠 Choose Action")
action = st.sidebar.selectbox("Select Action", ["Send SMS", "Make Call"])

to_number = st.text_input("📞 Recipient Phone Number (with country code)", "+91")

if action == "Send SMS":
    st.subheader("✉ Send an SMS")
    message_body = st.text_area("Your Message", "Hello from Python via Twilio! 🐍")

    if st.button("📤 Send SMS"):
        if not to_number.strip() or not message_body.strip():
            st.warning("⚠ Please enter both the phone number and message.")
        else:
            try:
                client = Client(ACCOUNT_SID, AUTH_TOKEN)
                message = client.messages.create(
                    body=message_body,
                    from_=TWILIO_PHONE,
                    to=to_number
                )
                st.success(f"✅ SMS sent successfully! Message SID: {message.sid}")
            except Exception as e:
                st.error(f"❌ Failed to send message: {e}")

elif action == "Make Call":
    st.subheader("📞 Make a Voice Call")
    voice_message = st.text_area("🗣 What should the call say?", "Hello! This is a test call using Python.")

    if st.button("📲 Call Now"):
        if not to_number.strip() or not voice_message.strip():
            st.warning("⚠ Please enter both the phone number and voice message.")
        else:
            try:
                client = Client(ACCOUNT_SID, AUTH_TOKEN)

                                fallback_twiml_url = "http://demo.twilio.com/docs/voice.xml"

                call = client.calls.create(
                    to=to_number,
                    from_=TWILIO_PHONE,
                    url=fallback_twiml_url
                )
                st.success(f"✅ Call initiated! Call SID: {call.sid}")
            except Exception as e:
                st.error(f"❌ Failed to initiate call: {e}")

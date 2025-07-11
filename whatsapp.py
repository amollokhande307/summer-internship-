import streamlit as st
import pywhatkit as kit
import datetime
import time

st.set_page_config(page_title="WhatsApp Message Sender", layout="centered")

st.title("WhatsApp Message Sender")
st.markdown("Send a message via WhatsApp using Python and Streamlit")


with st.form("whatsapp_form"):
    phone_number = st.text_input("Enter Phone Number (with country code)", "+91")
    message = st.text_area("Enter Your Message")
    send_now = st.checkbox("Send now (waits for browser)")
    submit_button = st.form_submit_button(label="Send WhatsApp Message")

if submit_button:
    if phone_number and message:
        try:
            st.info("Opening WhatsApp Web in your browser...")

            
            now = datetime.datetime.now()
            hour = now.hour
            minute = now.minute + 2  # Wait 2 minutes for WhatsApp Web to load

            if send_now:
                
                kit.sendwhatmsg_instantly(phone_no=phone_number, message=message, wait_time=15)
            else:
                

                kit.sendwhatmsg(phone_no=phone_number, message=message, time_hour=hour, time_min=minute)

            st.success("✅ Message scheduled/sent successfully!")
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter both the phone number and message.")

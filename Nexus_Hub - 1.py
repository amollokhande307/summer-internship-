import streamlit as st
import os
import smtplib
import ssl
import requests
from urllib.parse import urlparse
import psutil
from datetime import datetime
import time
import pywhatkit as kit
from twilio.rest import Client
import json
import base64
import google.generativeai as genai
from bs4 import BeautifulSoup
import re
import paramiko

# --- AWS & Gesture Control Imports ---
import boto3
from botocore.exceptions import ClientError, WaiterError


# --- Page Configuration ---
st.set_page_config(
    page_title="Nexus Hub",
    page_icon="🚀",
    layout="wide",
)

# ----------------- AWS CONFIG -----------------
# WARNING: Storing credentials directly in code is a security risk.
# It is better to use IAM roles or environment variables in production.
# Removed AWS Access Key and Secret Key
aws_access_key = "YOUR_AWS_ACCESS_KEY"
aws_secret_key = "YOUR_AWS_SECRET_KEY"
region = "ap-south-1"
# Removed S3 bucket name
bucket_name = "your-s3-bucket-name"

# EC2 Configs
# Removed EC2 key names
ec2_key1 = "your_ec2_key_name_1"
ec2_key2 = "your_ec2_key_name_2"
# Removed AMI IDs
ami1 = "your-ami-id-1"
ami2 = "your-ami-id-2"
# Removed Security Group IDs
sg1 = "your-security-group-id-1"
sg2 = "your-security-group-id-2"

# --- Custom CSS for Styling ---
st.markdown(
    """
    <style>
    body {
        font-family: 'Inter', sans-serif;
    }
    .main .block-container {
        padding-top: 2rem;
    }
    .st-emotion-cache-1f1911r a, .st-emotion-cache-fyb103 a, .st-emotion-cache-1f1911r button, .st-emotion-cache-fyb103 button {
        color: #f0f0f0 !important;
    }
    .card {
        background-color: #1f2937;
        padding: 1.5rem;
        border-radius: 0.75rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .dashboard-title {
        color: #f0f0f0;
        font-size: 2.25rem;
        font-weight: 700;
        padding-bottom: 1rem;
        border-bottom: 1px solid #4b5563;
        margin-bottom: 2rem;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar Menu ---
st.sidebar.markdown('<h2 class="text-xl font-bold text-gray-100">Nexus Hub</h2>', unsafe_allow_html=True)
st.sidebar.markdown("---")

if 'page' not in st.session_state:
    st.session_state.page = 'home'

if st.sidebar.button("🏠 Home"):
    st.session_state.page = 'home'

# --- System Tools Section ---
st.sidebar.markdown("### ⚙️ System Tools")
if st.sidebar.button("💾 RAM Monitor"):
    st.session_state.page = 'ram'

# --- Communication Tools Section ---
st.sidebar.markdown("### 📞 Communication Tools")
if st.sidebar.button("💬 WhatsApp Sender"):
    st.session_state.page = 'whatsapp'
if st.sidebar.button("🎙️ Twilio Voice Caller"):
    st.session_state.page = 'call'
if st.sidebar.button("📱 Twilio SMS Sender"):
    st.session_state.page = 'sms'
if st.sidebar.button("📧 Email Sender"):
    st.session_state.page = 'email'

# --- Web & Location Tools ---
st.sidebar.markdown("### 🌐 Web & Location")
if st.sidebar.button("🌐 Website Downloader"):
    st.session_state.page = 'website_download'
if st.sidebar.button("📍 Live Location"):
    st.session_state.page = 'live_location'
if st.sidebar.button("🌍 IP & Location"):
    st.session_state.page = 'ip_info'
if st.sidebar.button("🗺️ Directions"):
    st.session_state.page = 'directions'
if st.sidebar.button("📸 Camera Capture"):
    st.session_state.page = 'photo'

# --- AI & Data Tools ---
st.sidebar.markdown("### 🧠 AI & Data Tools")
if st.sidebar.button("🛒 Store Finder (Simulated)"):
    st.session_state.page = 'store_finder'
if st.sidebar.button("📦 Product Recommender (Simulated)"):
    st.session_state.page = 'product_recommender'
if st.sidebar.button("🏦 Bank Manager AI"):
    st.session_state.page = 'bank_manager_ai'
if st.sidebar.button("📈 Stock Market Predictor"):
    st.session_state.page = 'stock_predictor'

# --- Remote Management ---
st.sidebar.markdown("### 🖥️ Remote Management")
if st.sidebar.button("🐧 Linux SSH Terminal"):
    st.session_state.page = 'linux_terminal'
if st.sidebar.button("🐳 Docker Control Panel"):
    st.session_state.page = 'docker_panel'

# --- AWS Cloud Tools ---
st.sidebar.markdown("### ☁️ AWS Cloud Tools")
if st.sidebar.button("🚀 EC2 Manager"):
    st.session_state.page = 'ec2_manager'
if st.sidebar.button("📤 S3 Uploader"):
    st.session_state.page = 's3_uploader'


# --- Main Content Area ---
st.markdown('<h1 class="dashboard-title">Nexus Hub</h1>', unsafe_allow_html=True)

# --- Home Page ---
if st.session_state.page == 'home':
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2>Welcome to Your Nexus Hub</h2>', unsafe_allow_html=True)
    st.markdown('<p>Use the categorized menu on the left to navigate through the various tools and services.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- RAM Monitor Page ---
elif st.session_state.page == 'ram':
    st.header("💾 System RAM Monitor")
    
    def get_memory_info():
        memory = psutil.virtual_memory()
        return {
            'total': memory.total / (1024**3),
            'used': memory.used / (1024**3),
            'available': memory.available / (1024**3),
            'percentage': memory.percent
        }

    memory_info = get_memory_info()
    st.markdown(f"""
    - **Total RAM:** {memory_info['total']:.2f} GB
    - **Used Memory:** {memory_info['used']:.2f} GB  
    - **Available Memory:** {memory_info['available']:.2f} GB
    - **Usage Percentage:** {memory_info['percentage']:.1f}%
    """)
    st.progress(memory_info['percentage'] / 100)
    
    if memory_info['percentage'] < 50:
        st.success("✅ Memory usage is healthy.")
    elif memory_info['percentage'] < 80:
        st.warning("⚠️ Memory usage is moderate.")
    else:
        st.error("🚨 Memory usage is high!")

# --- WhatsApp Sender Page ---
elif st.session_state.page == 'whatsapp':
    st.header("💬 WhatsApp Message Sender")
    st.warning("This requires WhatsApp Web to be open and logged in on your system.")
    
    with st.form("whatsapp_form"):
        phone_number = st.text_input("Enter Phone Number (with country code, e.g., +91...)", "+91")
        message = st.text_area("Enter Your Message")
        submit_button = st.form_submit_button(label="Send WhatsApp Message")

    if submit_button:
        if phone_number and message:
            try:
                st.info("Attempting to open WhatsApp Web...")
                kit.sendwhatmsg_instantly(phone_no=phone_number, message=message, wait_time=20)
                st.success("✅ Message sent/scheduled successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("Please enter both a phone number and a message.")

# --- Twilio Voice Caller Page ---
elif st.session_state.page == 'call':
    st.header("🎙️ Twilio Voice Caller")
    
    # Removed Twilio Account SID and Auth Token
    ACCOUNT_SID = st.text_input("Twilio Account SID", "your_twilio_account_sid")
    AUTH_TOKEN = st.text_input("Twilio Auth Token", "your_twilio_auth_token", type="password")
    TWILIO_PHONE = st.text_input("Your Twilio Phone Number", "your_twilio_phone_number")
    
    to_number = st.text_input("Recipient Phone Number", "+91")

    if st.button("📞 Call Now"):
        if not all([ACCOUNT_SID, AUTH_TOKEN, TWILIO_PHONE, to_number]):
            st.warning("Please fill in all Twilio credentials and the recipient number.")
        else:
            try:
                client = Client(ACCOUNT_SID, AUTH_TOKEN)
                call = client.calls.create(
                    to=to_number,
                    from_=TWILIO_PHONE,
                    url="http://demo.twilio.com/docs/voice.xml" # Demo TwiML
                ) 
                st.success(f"✅ Call initiated! SID: {call.sid}")
            except Exception as e:
                st.error(f"❌ Failed to initiate call: {e}")

# --- Twilio SMS Sender Page ---
elif st.session_state.page == 'sms':
    st.header("📱 Twilio SMS Sender")

    # Removed Twilio Account SID and Auth Token
    ACCOUNT_SID = st.text_input("Twilio Account SID", "your_twilio_account_sid")
    AUTH_TOKEN = st.text_input("Twilio Auth Token", "your_twilio_auth_token", type="password")
    TWILIO_PHONE = st.text_input("Your Twilio Phone Number", "your_twilio_phone_number")

    to_number = st.text_input("Recipient Phone Number", "+91")
    message_body = st.text_area("Your Message", "Hello from a Streamlit app via Twilio! 🐍")

    if st.button("Send SMS"):
        if not all([ACCOUNT_SID, AUTH_TOKEN, TWILIO_PHONE, to_number, message_body]):
            st.warning("Please fill in all fields.")
        else:
            try:
                client = Client(ACCOUNT_SID, AUTH_TOKEN)
                message = client.messages.create(
                    body=message_body,
                    from_=TWILIO_PHONE,
                    to=to_number
                )
                st.success(f"✅ SMS sent successfully! SID: {message.sid}")
            except Exception as e:
                st.error(f"❌ Failed to send message: {e}")

# --- Email Sender Page ---
elif st.session_state.page == 'email':
    st.header("📧 Email Sender")
    st.info("Uses Gmail's SMTP server. You may need to enable 'Less secure app access' or use an App Password in your Google account.")
    
    # Removed Gmail Address and App Password
    From = st.text_input("Your Gmail Address", "your_gmail_address@gmail.com")
    password = st.text_input("Your Gmail App Password", "your_app_password", type="password")
    To = st.text_input("Recipient's Email Address")
    Sub = st.text_input("Subject")
    msg = st.text_area("Message")

    if st.button("Send Email"):
        if not all([From, password, To, Sub, msg]):
            st.warning("Please fill in all fields.")
        else:
            text = f"Subject: {Sub}\n\n{msg}"
            try:
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()
                    server.login(From, password=password)
                    server.sendmail(from_addr=From, to_addrs=To, msg=text)
                st.success("✅ Email sent successfully!")
            except Exception as e:
                st.error(f"❌ Failed to send email: {e}")

# --- Website Downloader Page ---
elif st.session_state.page == 'website_download':
    st.header("🌐 Website Source Downloader")
    
    url = st.text_input("🔗 Enter Website URL", placeholder="https://example.com")
    
    if st.button("📥 Download HTML"):
        if not url:
            st.warning("Please enter a valid URL.")
        else:
            try:
                response = requests.get(url)
                response.raise_for_status()
                parsed_url = urlparse(url)
                filename = f"{parsed_url.netloc.replace('.', '_')}.html"
                st.download_button(
                    label="📄 Download as .html File",
                    data=response.text,
                    file_name=filename,
                    mime="text/html"
                )
            except Exception as e:
                st.error(f"❌ Failed to download website: {e}")

# --- Live Location Page ---
elif st.session_state.page == 'live_location':
    st.header("📍 Live Location Viewer")
    st.warning("This requires a secure HTTPS connection and browser permission.")
    html_code = """
    <div id="location-output" style="padding: 1em; border: 1px solid #ccc; border-radius: 5px;">
        Click the button to get your live location...
    </div>
    <script>
    function getLocation() {
      const output = document.getElementById("location-output");
      if (!navigator.geolocation) {
        output.innerHTML = "Geolocation is not supported by your browser.";
        return;
      }
      output.innerHTML = "Fetching location...";
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const lat = position.coords.latitude.toFixed(6);
          const lon = position.coords.longitude.toFixed(6);
          output.innerHTML = `<p><b>Latitude:</b> ${lat}</p><p><b>Longitude:</b> ${lon}</p>
                              <a href="https://www.google.com/maps?q=$${lat},${lon}" target="_blank">View on Google Maps</a>`;
        },
        (error) => { output.innerHTML = `Error: ${error.message}`; }
      );
    }
    // Automatically trigger after a delay to allow component to render
    setTimeout(getLocation, 1000);
    </script>
    """
    st.components.v1.html(html_code, height=150)

# --- IP Info Page ---
elif st.session_state.page == 'ip_info':
    st.header("🌍 Public IP and Location Info")
    if st.button("Get My IP Info"):
        try:
            # Removed ipinfo.io API token
            response = requests.get('https://ipinfo.io/json?token=your_ipinfo_api_token').json()
            st.success(f"Your IP is **{response.get('ip')}** in **{response.get('city')}, {response.get('region')}, {response.get('country')}**.")
        except Exception as e:
            st.error(f"Could not fetch IP info: {e}")

# --- Directions Page ---
elif st.session_state.page == 'directions':
    st.header("🗺️ Get Directions on Google Maps")
    from_loc = st.text_input("📍 From:", "Start Location")
    to_loc = st.text_input("🎯 To:", "Destination")
    if st.button("Open in Google Maps"):
        if from_loc and to_loc:
            # Removed hard-coded locations from the URL
            maps_url = f"https://www.google.com/maps/dir/{from_loc}/{to_loc}"
            st.markdown(f'<a href="{maps_url}" target="_blank">Click here to open directions</a>', unsafe_allow_html=True)
        else:
            st.warning("Please enter both locations.")

# --- Camera Capture Page ---
elif st.session_state.page == 'photo':
    st.header("📸 Camera Capture")
    img_file_buffer = st.camera_input("Take a picture")
    if img_file_buffer:
        st.image(img_file_buffer, caption="Your captured photo.")
        st.download_button(label="Download Image", data=img_file_buffer.getvalue(), file_name="capture.jpg", mime="image/jpeg")

# --- Store Finder Page (Simulated) ---
elif st.session_state.page == 'store_finder':
    st.header("🛒 Store Finder (Simulated)")
    if st.button("Find Stores Near Me"):
        with st.spinner("Simulating search..."):
            time.sleep(1)
        st.success("Found 3 stores near you!")
        st.table([{"Name": "More Megastore", "Distance": "1.2 km"}, {"Name": "Big Bazaar", "Distance": "1.5 km"}, {"Name": "Reliance Fresh", "Distance": "2.1 km"}])

# --- Product Recommender Page (Simulated) ---
elif st.session_state.page == 'product_recommender':
    st.header("📦 Product Recommender (Simulated)")
    if st.button("Get Recommendation"):
        with st.spinner("Analyzing behavior..."):
            time.sleep(1)
        st.success("✨ Recommended for you: **Smart Fitness Watch** ✨")

# --- Bank Manager AI Page ---
elif st.session_state.page == 'bank_manager_ai':
    st.header("🏦 Bank Manager AI (Gemini)")
    # Removed Google Gemini API Key
    GOOGLE_API_KEY = st.text_input("Enter your Google Gemini API Key", type="password")
    if GOOGLE_API_KEY:
        try:
            genai.configure(api_key=GOOGLE_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            user_input = st.text_input("Ask anything about loans:")
            if user_input:
                with st.spinner("Thinking..."):
                    response = model.generate_content(f"Act as a helpful bank manager. {user_input}")
                    st.markdown(response.text)
        except Exception as e:
            st.error(f"Error with Gemini AI: {e}")
    else:
        st.warning("Please provide a Gemini API key to use this feature.")

# --- Stock Market Predictor Page ---
elif st.session_state.page == 'stock_predictor':
    st.header("📈 Stock Market Predictor (Conceptual)")
    st.info("This is a conceptual feature. Full implementation requires financial data APIs.")
    stock_query = st.text_input("Enter stock symbol (e.g., 'TCS', 'RELIANCE'):")
    if st.button("Get Stock Info"):
        st.success(f"Prediction for **{stock_query}**: Likely to go up. (Simulated)")

# --- Linux SSH Terminal Page ---
elif st.session_state.page == 'linux_terminal':
    st.header("🐧 Linux SSH Terminal")
    with st.form("ssh_form"):
        hostname = st.text_input("Host IP")
        username = st.text_input("Username", "ec2-user")
        password = st.text_input("Password", type="password")
        command = st.text_input("Command", "ls -l")
        submitted = st.form_submit_button("Run Command")
    if submitted:
        if not all([hostname, username, password, command]):
            st.warning("Please fill in all SSH credentials and a command.")
        else:
            with st.spinner("Connecting and executing..."):
                try:
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    ssh.connect(hostname, port=22, username=username, password=password)
                    stdin, stdout, stderr = ssh.exec_command(command)
                    output = stdout.read().decode()
                    error = stderr.read().decode()
                    ssh.close()
                    if output: st.code(output, language="bash")
                    if error: st.error(error)
                except Exception as e:
                    st.error(f"❌ SSH Connection Failed: {e}")

# --- Docker Control Panel Page ---
elif st.session_state.page == 'docker_panel':
    st.header("🐳 Docker Control Panel (via SSH)")
    with st.expander("🔐 SSH Configuration", expanded=True):
        ssh_host = st.text_input("Docker Host IP")
        ssh_user = st.text_input("Docker Host Username")
        ssh_password = st.text_input("Docker Host Password", type="password")
    
    def ssh_command(command):
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(ssh_host, port=22, username=ssh_user, password=ssh_password)
            stdin, stdout, stderr = client.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            client.close()
            return f"❌ Error:\n{error}" if error else output or "✅ Command executed successfully."
        except Exception as e:
            return f"🚨 Connection failed: {e}"

    if ssh_host and ssh_user and ssh_password:
        choice = st.selectbox("Select Docker Operation", ["List All Containers", "List Running Containers", "List Images", "Launch New Container"])
        if choice == "List All Containers":
            st.code(ssh_command("docker ps -a"))
        elif choice == "List Running Containers":
            st.code(ssh_command("docker ps"))
        elif choice == "List Images":
            st.code(ssh_command("docker images"))
        elif choice == "Launch New Container":
            with st.form("launch_container_form"):
                name = st.text_input("Container Name")
                image = st.text_input("Docker Image (e.g., ubuntu:latest)")
                submitted = st.form_submit_button("Launch Container")
                if submitted:
                    st.code(ssh_command(f"docker run -dit --name {name} {image}"))
    else:
        st.info("Please enter SSH credentials to manage Docker.")

# --- EC2 MANAGER ---
elif st.session_state.page == 'ec2_manager':
    st.header("🚀 AWS EC2 Manager")
    ec2_client = boto3.client("ec2", region_name=region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    if "instance_id" not in st.session_state: 
        st.session_state.instance_id = None

    def launch_ec2_instance():
        try:
            response = ec2_client.run_instances(
                ImageId=ami1, InstanceType="t2.micro", KeyName=ec2_key1,
                MaxCount=1, MinCount=1, SecurityGroupIds=[sg1],
                TagSpecifications=[{'ResourceType': 'instance', 'Tags': [{'Key': 'Name', 'Value': 'MyStreamlitInstance'}]}]
            )
            instance_id = response["Instances"][0]["InstanceId"]
            waiter = ec2_client.get_waiter("instance_running")
            waiter.wait(InstanceIds=[instance_id])
            st.success(f"Instance launched: {instance_id}")
            return instance_id
        except (ClientError, WaiterError) as e:
            st.error(e)
            return None

    def get_public_ip(instance_id):
        try:
            desc = ec2_client.describe_instances(InstanceIds=[instance_id])
            return desc["Reservations"][0]["Instances"][0].get("PublicIpAddress")
        except ClientError as e:
            st.error(f"Error getting public IP: {e}")
            return None

    def terminate_ec2_instance(instance_id):
        try:
            ec2_client.terminate_instances(InstanceIds=[instance_id])
            waiter = ec2_client.get_waiter("instance_terminated")
            waiter.wait(InstanceIds=[instance_id])
            st.success(f"Instance {instance_id} terminated.")
            return True
        except (ClientError, WaiterError) as e:
            st.error(f"Error terminating instance: {e}")
            return False

    if st.button("🚀 Launch New EC2 Instance"):
        with st.spinner("Launching..."):
            st.session_state.instance_id = launch_ec2_instance()

    if st.session_state.instance_id:
        st.info(f"Managing Instance ID: {st.session_state.instance_id}")
        if st.button("🔍 Get Public IP"):
            ip = get_public_ip(st.session_state.instance_id)
            if ip:
                st.success(f"Public IP: {ip}")
            else:
                st.warning("Public IP not assigned yet.")
        if st.button("🛑 Terminate This Instance"):
            if terminate_ec2_instance(st.session_state.instance_id):
                st.session_state.instance_id = None
                st.rerun()

# --- S3 UPLOADER ---
elif st.session_state.page == 's3_uploader':
    st.header("📤 AWS S3 Uploader")
    s3_client = boto3.client("s3", region_name=region, aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key)
    uploaded_file = st.file_uploader("📁 Choose a file to upload to S3")
    if uploaded_file:
        if st.button(f"Upload '{uploaded_file.name}' to S3"):
            with st.spinner("Uploading..."):
                try:
                    s3_client.upload_fileobj(uploaded_file, bucket_name, uploaded_file.name)
                    st.success(f"✅ File '{uploaded_file.name}' uploaded to bucket '{bucket_name}'")
                except ClientError as e:
                    st.error(f"❌ Upload Error: {e}")
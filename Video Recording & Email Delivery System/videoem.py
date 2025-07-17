from flask import Flask, request, render_template, jsonify
import smtplib
import ssl
import os
from email.message import EmailMessage
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024
app.config['ALLOWED_EXTENSIONS'] = {'webm', 'mp4', 'mov', 'avi'}
app.config['SENDER_EMAIL'] = 'Enter your Email'
app.config['SENDER_PASSWORD'] = 'Enter your pass'

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if 'video' not in request.files or 'email' not in request.form:
        return jsonify({"error": "Missing video file or email"}), 400
    
    video_file = request.files['video']
    recipient_email = request.form['email']
    
    if video_file.filename == '':
        return jsonify({"error": "No selected file"}), 400
        
    if not allowed_file(video_file.filename):
        return jsonify({"error": "Invalid file type"}), 400
    
    filename = secure_filename(video_file.filename)
    temp_path = os.path.join('temp_uploads', filename)
    
    os.makedirs('temp_uploads', exist_ok=True)
    
    try:
        video_file.save(temp_path)
        
        email_msg = EmailMessage()
        email_msg["Subject"] = "Your Video Attachment"
        email_msg["From"] = app.config['SENDER_EMAIL']
        email_msg["To"] = recipient_email
        email_msg.set_content("Please find your video attached.")

        with open(temp_path, "rb") as f:
            file_data = f.read()
            file_type = filename.rsplit('.', 1)[1].lower()
            email_msg.add_attachment(file_data, maintype="video", subtype=file_type, filename=filename)

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(app.config['SENDER_EMAIL'], app.config['SENDER_PASSWORD'])
            server.send_message(email_msg)
            
        return jsonify({"success": "Video sent successfully"}), 200
        
    except Exception as e:
        return jsonify({"error": f"Failed to process request: {str(e)}"}), 500
        
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

if __name__ == "__main__":
    app.run(debug=True)
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from dotenv import load_dotenv
import cloudinary
import cloudinary.uploader
import requests

# ✅ Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Required for flash messages

# ✅ Cloudinary configuration
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)

# ✅ Relay Webhook URL
RELAY_WEBHOOK_URL = os.getenv("RELAY_WEBHOOK_URL")


# ✅ Show landing page
@app.route('/')
def index():
    return render_template('index.html')


# ✅ Upload resume route
@app.route('/upload_resume', methods=['GET', 'POST'])
def upload_resume():
    if request.method == 'POST':
        name = request.form.get('name')
        resume_file = request.files.get('resume_file')

        if not resume_file:
            flash("No file uploaded!")
            return redirect(url_for('upload_resume'))

        try:
            # ✅ Upload resume to Cloudinary
            result = cloudinary.uploader.upload(resume_file, folder="resumes")
            resume_url = result['secure_url']

            # ✅ Send data to Relay Webhook
            payload = {
                "name": name,
                "resume_url": resume_url
            }

            response = requests.post(RELAY_WEBHOOK_URL, json=payload)
            response.raise_for_status()  # Raise error if failed

            flash("✅ Resume uploaded and sent successfully!")
            # You can change to `url_for('success')` if you want
            return redirect(url_for('upload_resume'))

        except Exception as e:
            print("Upload or webhook failed:", e)
            flash("❌ Something went wrong. Please try again.")
            return redirect(url_for('upload_resume'))

    return render_template('upload_resume.html')


# ✅ Optional success page
@app.route('/success')
def success():
    return render_template('success.html')


# ✅ Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)

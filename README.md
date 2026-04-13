# 🤖 Aurify — AI-Powered Resume Screener
### IBM AI/ML Project: *Development of an AI-Powered Resume Screener for Automated Candidate Shortlisting*



**Team Name:** AutoBrain  
**Team Members:** Fathima Sahala K, Sreeharini J, Sreya S, Aiswarya S, Girik Sagar, Adhithyan P S, Fahad M K  
**Live App:** [aurify-resume-screenerai.onrender.com](https://aurify-resume-screenerai.onrender.com)

---

## 📌 Problem Statement

Recruiters spend hours manually reading resumes — a process that is slow, inconsistent, and subjective. This project was built as part of the **IBM AI/ML curriculum** to solve that using automation and AI. The goal: automatically evaluate how well a candidate's resume matches a given job description, eliminating the manual first-pass screening entirely.

---

## 💡 Solution Overview

Aurify is a full-stack web application where a user uploads a resume (PDF) and a job description. The system then:
1. Stores the files securely in the cloud
2. Passes them through an AI workflow
3. Returns a compatibility score or feedback — instantly

No manual review. No delay. Just results.

---

## 🏗️ Architecture & Tech Stack

```
User (Browser)
     │
     ▼
 HTML/CSS Frontend
     │  (form submit — name + resume PDF)
     ▼
Flask Backend (Python)         ← handles routing, file intake, integrations
     │
     ├──▶ Cloudinary            ← stores the uploaded resume PDF securely
     │         └── returns a public file URL
     │
     └──▶ Relay (Webhook)       ← triggers the AI screening workflow
               └── AI analyzes resume vs job description
                         └── returns compatibility result
```

---

## 🔧 Backend — Detailed Breakdown

The backend is the brain of this project. It is built with **Flask (Python)** and handles everything between the user's form submission and the AI result.

### File: `app.py`

#### 1. Environment Configuration
All sensitive credentials (API keys, webhook URLs) are loaded from a `.env` file using `python-dotenv`. This keeps secrets out of the code.

```python
load_dotenv()
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET')
)
RELAY_WEBHOOK_URL = os.getenv("RELAY_WEBHOOK_URL")
```

#### 2. Resume Upload Route — `/upload_resume` (POST)
This is the core backend route. When the form is submitted:

**Step 1 — Receive the file**
```python
name = request.form.get('name')
resume_file = request.files.get('resume_file')
```

**Step 2 — Upload to Cloudinary**  
The PDF is uploaded to Cloudinary's cloud storage under a `resumes/` folder. Cloudinary returns a secure public URL.
```python
result = cloudinary.uploader.upload(resume_file, folder="resumes")
resume_url = result['secure_url']
```

**Step 3 — Trigger Relay Webhook**  
The candidate's name and the Cloudinary URL are sent as a JSON payload to the Relay webhook endpoint. This is what kicks off the AI analysis.
```python
payload = { "name": name, "resume_url": resume_url }
response = requests.post(RELAY_WEBHOOK_URL, json=payload)
```

**Step 4 — Flash feedback to user**  
Flask's `flash()` system sends a success or error message back to the HTML template.
```python
flash("✅ Resume uploaded and sent successfully!")
```

#### 3. Error Handling
All operations are wrapped in a `try/except` block. If Cloudinary upload fails or the Relay webhook returns an error, the user sees a clear error message instead of a crash.

---

## 🔗 Relay — The AI Workflow Engine

**Relay** is a no-code/low-code automation platform (similar to Make or Zapier) that was introduced as part of the IBM AI/ML course. In this project, Relay acts as the bridge between the uploaded resume and the AI model.

### How it works:
1. Flask sends a **webhook POST request** to a Relay trigger URL with the resume's Cloudinary link
2. Relay receives this and starts an automated workflow
3. The workflow fetches the resume, passes it along with a job description to an **AI/LLM model**
4. The AI evaluates compatibility and generates a score or feedback
5. Results can be sent back to the app, stored, or forwarded to a recruiter

### Why Relay?
- No need to write custom AI pipeline code
- Visual workflow builder — easy to modify the screening logic
- Connects easily to LLMs (like Claude or GPT) and other tools
- Webhook-based trigger integrates cleanly with the Flask backend

---

## ☁️ Cloudinary — File Storage

Cloudinary handles secure PDF storage so resumes aren't stored on the server itself (which would be unreliable on free hosting). Each upload generates a permanent, accessible URL that gets passed to Relay for AI processing.

---

## 🚀 Running Locally

### 1. Clone the repo and install dependencies
```bash
pip install flask python-dotenv cloudinary requests
```

### 2. Create your `.env` file
```env
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret
RELAY_WEBHOOK_URL=your_relay_webhook_url
```
- Get Cloudinary credentials from [cloudinary.com](https://cloudinary.com) → Dashboard
- Get Relay webhook URL from your Relay workflow's trigger settings

### 3. Folder structure
```
project/
├── app.py
├── .env
└── templates/
    ├── index.html
    ├── upload_resume.html
    └── success.html
```

### 4. Start the server
```bash
python app.py
```
Then open: `http://localhost:5000`

---

## 📂 Project Files

| File | Description |
|------|-------------|
| `app.py` | Flask backend — routing, upload logic, webhook integration |
| `templates/upload_resume.html` | Resume upload form (HTML/CSS) |
| `templates/index.html` | Landing page |
| `ResumeScreener.ipynb` | Main AI/ML notebook |
| `sample_resumes/` | Example resume PDFs for testing |
| `job_description.txt` | Sample job description input |
| `resume_screening_results.csv` | Output compatibility scores |

**Drive links:**
- [Screenshots](https://drive.google.com/drive/folders/18jRCtHFXSvOHZaZWX1a6O1dKjF_eZ49-)
- [Project files](https://drive.google.com/drive/folders/1DXGT51GpwIAIwNFipMTUTTzb9PSC4JBn?usp=drive_link)

---

## 🎯 Use Cases

- **HR Automation** — Screen hundreds of resumes in minutes
- **Campus Recruitment** — Match students to roles at scale
- **Resume Quality Feedback** — Help candidates improve their resumes
- **Objective Shortlisting** — Remove unconscious bias from early screening

---

## 📄 License

This project is licensed under the **MIT License**.

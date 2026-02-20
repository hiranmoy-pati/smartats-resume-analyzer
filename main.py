from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import HTMLResponse, FileResponse
from PyPDF2 import PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import re, uuid, os

app = FastAPI()

APP_NAME = "SmartATS by Hiranmoy"

SKILLS_DB = {
    "python": ["python"],
    "data analysis": ["pandas", "numpy"],
    "machine learning": ["machine learning", "ml"],
    "web development": ["html", "css", "javascript", "fastapi"],
    "database": ["mysql", "postgresql", "sqlite"],
    "cloud": ["aws", "docker"]
}

JOB_ROLES = {
    "Backend Developer": ["python", "web development", "database"],
    "Data Analyst": ["python", "data analysis"],
    "Cloud Engineer": ["cloud", "database"]
}

# ---------- HELPERS ----------

def extract_text(file):
    reader = PdfReader(file)
    text = ""
    for p in reader.pages:
        if p.extract_text():
            text += p.extract_text()
    return text.lower()

def extract_skills(text):
    found = []
    for skill, words in SKILLS_DB.items():
        for w in words:
            if re.search(rf"\b{w}\b", text):
                found.append(skill)
                break
    return list(set(found))

def ats_score(skills):
    return int(len(skills) / len(SKILLS_DB) * 100)

def jd_match(resume_skills, jd_text):
    jd_skills = extract_skills(jd_text.lower())
    if not jd_skills:
        return 0
    return int(len(set(resume_skills) & set(jd_skills)) / len(jd_skills) * 100)

def suggestions(found, missing):
    tips = []
    if "python" not in found:
        tips.append("Add Python projects to improve ATS score.")
    if "cloud" in missing:
        tips.append("Cloud skills increase backend job chances.")
    if len(found) < 3:
        tips.append("Add more technical keywords.")
    return tips

def generate_pdf(rid, data):
    filename = f"report_{rid}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    y = 800

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, APP_NAME)
    y -= 40

    c.setFont("Helvetica", 12)
    for k, v in data.items():
        c.drawString(50, y, f"{k}: {v}")
        y -= 20

    c.save()
    return filename

# ---------- ROUTES ----------

@app.get("/", response_class=HTMLResponse)
def home():
    with open("index.html", encoding="utf-8") as f:
        return f.read()

@app.post("/analyze")
async def analyze(
    file: UploadFile = File(...),
    job_description: str = Form("")
):
    text = extract_text(file.file)
    skills = extract_skills(text)

    ats = ats_score(skills)
    missing = list(set(SKILLS_DB.keys()) - set(skills))
    jd_score = jd_match(skills, job_description)
    tips = suggestions(skills, missing)

    rid = str(uuid.uuid4())

    pdf = generate_pdf(rid, {
        "ATS Score": f"{ats}%",
        "JD Match": f"{jd_score}%",
        "Skills Found": ", ".join(skills),
        "Missing Skills": ", ".join(missing),
        "Suggestions": "; ".join(tips)
    })

    return {
        "ats_score": ats,
        "jd_match_score": jd_score,
        "skills_found": skills,
        "missing_skills": missing,
        "suggestions": tips,
        "pdf": f"/download/{rid}"
    }

@app.get("/download/{rid}")
def download(rid: str):
    return FileResponse(f"report_{rid}.pdf", filename="SmartATS_Report.pdf")
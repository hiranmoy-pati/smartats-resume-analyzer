# SmartATS by Hiranmoy 🚀

SmartATS is a **rule-based Applicant Tracking System (ATS)** that analyzes resumes without using AI models.

It simulates real recruiter ATS logic using **regex, scoring rules, and job description matching**.

---

## 🔍 Features

- 📄 Resume upload (PDF)
- 🧠 Skill extraction using Regex
- 📊 ATS score calculation
- 📌 Missing skills detection
- 🎯 Job Description vs Resume match
- 💡 Resume improvement suggestions
- 📈 Skill visualization (Chart.js)
- 📥 Downloadable ATS PDF report
- 🏷️ Branded UI – *SmartATS by Hiranmoy*

---

## 🛠 Tech Stack

- **Backend:** Python, FastAPI
- **Frontend:** HTML, CSS, JavaScript
- **PDF Parsing:** PyPDF2
- **PDF Report:** ReportLab
- **Visualization:** Chart.js

---

## ▶️ How to Run Locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload

# AI Security Log Analyser

An AI-powered web tool that automatically analyses security logs, 
identifies MITRE ATT&CK techniques, rates severity, and generates 
structured incident reports.

## Features
- Upload any Sysmon or Windows Event log file via web interface
- AI-powered threat analysis using LLaMA 3.3
- Automatic MITRE ATT&CK technique identification
- IOC extraction (IPs, file paths, registry keys, commands)
- Severity rating (Critical / High / Medium / Low)
- Structured JSON report saved automatically
- Clean, professional dark-mode UI

## How To Run
1. Clone the repo
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install flask groq python-dotenv`
5. Add your Groq API key to `.env`: `GROQ_API_KEY=your-key-here`
6. Run: `python3 app.py`
7. Open browser at: `http://127.0.0.1:5000`

## Tech Stack
Python · Flask · Groq API · LLaMA 3.3 · MITRE ATT&CK · HTML/CSS/JS

## Versions
- v0.1 — AI security Q&A assistant
- v0.2 — Automated log analysis with report saving
- v0.3 — Analyse any log file via command line
- v0.4 — Structured JSON output with IOC extraction
- v1.0 — Full web interface ✅

## Sample Output
<img width="498" height="661" alt="Screenshot 2026-04-21 at 10 38 40 AM" src="https://github.com/user-attachments/assets/2a90fe69-f778-40b6-b9c5-5d13a9515bd5" />

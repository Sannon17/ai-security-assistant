import os
import json
from flask import Flask, request, jsonify, render_template
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyse', methods=['POST'])
def analyse():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    log_content = file.read().decode('utf-8')
    log_filename = file.filename

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert SOC analyst and incident responder.
                    Analyse the provided security logs and respond ONLY with a JSON object.
                    No extra text, no markdown, no explanation — just the raw JSON.
                    
                    Use exactly this structure:
                    {
                        "summary": "Plain English summary of what happened",
                        "severity": "Critical | High | Medium | Low",
                        "mitre_techniques": [
                            {
                                "id": "T1059.001",
                                "name": "PowerShell",
                                "tactic": "Execution",
                                "description": "Why this technique was identified"
                            }
                        ],
                        "indicators_of_compromise": [
                            "List of specific IOCs found: IPs, file paths, registry keys, commands"
                        ],
                        "immediate_actions": [
                            "Action 1",
                            "Action 2",
                            "Action 3"
                        ],
                        "analyst_notes": "Any additional context or recommendations"
                    }"""
                },
                {
                    "role": "user",
                    "content": f"Analyse these security logs:\n\n{log_content}"
                }
            ]
        )

        raw = response.choices[0].message.content

        try:
            report_data = json.loads(raw)
        except json.JSONDecodeError:
            clean = raw.replace("```json", "").replace("```", "").strip()
            report_data = json.loads(clean)

        report_data["log_file"] = log_filename
        report_data["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Save JSON report
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open(f"report_{timestamp}.json", "w") as f:
            json.dump(report_data, f, indent=2)

        return jsonify(report_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
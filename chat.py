import os
import sys
import json
from groq import Groq
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Accept any log file as input
if len(sys.argv) < 2:
    print("Usage: python3 chat.py <logfile>")
    print("Example: python3 chat.py sample.log")
    sys.exit(1)

log_file = sys.argv[1]

if not os.path.exists(log_file):
    print(f"Error: File '{log_file}' not found.")
    sys.exit(1)

with open(log_file, "r") as f:
    log_content = f.read()

print(f"Analysing {log_file}...\n")

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

# Parse the JSON
try:
    report_data = json.loads(raw)
except json.JSONDecodeError:
    # Sometimes AI adds markdown backticks - strip them
    clean = raw.replace("```json", "").replace("```", "").strip()
    report_data = json.loads(clean)

# Add metadata
report_data["log_file"] = log_file
report_data["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# Print formatted report to screen
print("=== AI THREAT ANALYSIS REPORT ===\n")
print(f"📁 Log File:  {report_data['log_file']}")
print(f"🕐 Generated: {report_data['generated_at']}")
print(f"🚨 Severity:  {report_data['severity']}")
print(f"\n📋 SUMMARY:\n{report_data['summary']}")

print(f"\n🎯 MITRE ATT&CK TECHNIQUES ({len(report_data['mitre_techniques'])} identified):")
for t in report_data['mitre_techniques']:
    print(f"  • {t['id']} — {t['name']} [{t['tactic']}]")
    print(f"    {t['description']}")

print(f"\n🔍 INDICATORS OF COMPROMISE:")
for ioc in report_data['indicators_of_compromise']:
    print(f"  • {ioc}")

print(f"\n⚡ IMMEDIATE ACTIONS:")
for i, action in enumerate(report_data['immediate_actions'], 1):
    print(f"  {i}. {action}")

print(f"\n📝 ANALYST NOTES:\n{report_data['analyst_notes']}")

# Save JSON report
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
json_filename = f"report_{timestamp}.json"
with open(json_filename, "w") as f:
    json.dump(report_data, f, indent=2)

print(f"\n✅ JSON report saved to: {json_filename}")
print("=== END OF REPORT ===")
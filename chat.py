import os
import sys
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
            When given security logs, you:
            1. Summarise what happened in plain English
            2. List every MITRE ATT&CK technique you identify with the TTP ID
            3. Rate the severity (Low / Medium / High / Critical)
            4. List the top 3 immediate actions the analyst should take
            Keep your response structured and concise."""
        },
        {
            "role": "user",
            "content": f"Analyse these security logs and provide a threat report:\n\n{log_content}"
        }
    ]
)

report = response.choices[0].message.content

# Print to screen
print("=== AI THREAT ANALYSIS REPORT ===\n")
print(report)
print("\n=== END OF REPORT ===")

# Save to file automatically
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
filename = f"report_{timestamp}.txt"

with open(filename, "w") as f:
    f.write(f"AI THREAT ANALYSIS REPORT\n")
    f.write(f"Log File Analysed: {log_file}\n")
    f.write(f"Generated: {timestamp}\n")
    f.write(f"{'='*40}\n\n")
    f.write(report)

print(f"\n✅ Report saved to: {filename}")
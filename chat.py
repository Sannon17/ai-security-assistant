import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

question = input("Ask your security assistant: ")

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {
            "role": "system",
            "content": """You are an expert cybersecurity analyst assistant. 
            You help with threat analysis, MITRE ATT&CK mapping, vulnerability 
            assessment, Sysmon log analysis, and incident response. 
            Give clear, structured, actionable answers."""
        },
        {
            "role": "user",
            "content": question
        }
    ]
)

print("\nSecurity Assistant says:\n")
print(response.choices[0].message.content)
# Groq library import kar rahe hain
from groq import Groq

# Groq API key — groq.com se leni hai
API_KEY = ""

# Client banao
client = Groq(api_key=API_KEY)

# Gemini ki jagah Groq ka Llama3 use karenge
response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",  # free model
    messages=[
        {
            "role": "user",
            "content": "Hello! Ek line mein batao aap kaun ho."
        }
    ]
)

# Answer print karo
print("AI ka jawab:")
print(response.choices[0].message.content)
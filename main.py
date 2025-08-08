import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1" 
)

def ask_travel_assistant(user_input):
    prompt = f"You are a travel assistant. Answer the following question:\n\n{user_input}"

    response = client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {"role": "system", "content": "You are a helpful travel assistant."},
        {"role": "user", "content": prompt}
    ],
    temperature=0.7,
    max_tokens=400
    )

    
    return response.choices[0].message.content

# Run the assistant
print("🧳 Welcome to Travel Assistant! Ask me anything travel-related.")
while True:
    user_question = input("You: ")
    if user_question.lower() in ["exit", "quit"]:
        break
    answer = ask_travel_assistant(user_question)
    print("Assistant:", answer)

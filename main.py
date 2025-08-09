import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API key from environment
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)


# Toggle between modes: "zero-shot" or "one-shot"
PROMPT_MODE = "one-shot"  # change to "zero-shot" if needed

def ask_travel_assistant(user_input):
    if PROMPT_MODE == "zero-shot":
        # Directly ask without examples
        prompt = user_input
    elif PROMPT_MODE == "one-shot":
        # Provide one example before asking
        one_shot_example = """
        User: I want to visit Paris for 3 days. Suggest a travel itinerary.
        Assistant: Sure! Here's a 3-day itinerary for Paris:
        Day 1: Visit Eiffel Tower, Louvre Museum, and Seine River cruise.
        Day 2: Explore Montmartre, Sacré-Cœur, and local cafés.
        Day 3: Versailles Palace day trip and evening shopping at Champs-Élysées.
        """
        prompt = f"{one_shot_example}\nUser: {user_input}\nAssistant:"

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

if __name__ == "__main__":
    user_query = input("🧳 Welcome to Travel Assistant! Ask me anything travel-related.")
    answer = ask_travel_assistant(user_query)
    print("\nAssistant:", answer)

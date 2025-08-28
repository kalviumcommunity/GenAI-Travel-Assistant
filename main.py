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

# Toggle between modes: "zero-shot", "one-shot", "multi-shot"
PROMPT_MODE = "multi-shot"  # change to "zero-shot" or "one-shot" if needed

def ask_travel_assistant(user_input):
    if PROMPT_MODE == "zero-shot":
        # Direct query
        prompt = user_input

    elif PROMPT_MODE == "one-shot":
        # One example only
        one_shot_example = """
        User: I want to visit Paris for 3 days. Suggest a travel itinerary.
        Assistant: Sure! Here's a 3-day itinerary for Paris:
        Day 1: Visit Eiffel Tower, Louvre Museum, and Seine River cruise.
        Day 2: Explore Montmartre, Sacré-Cœur, and local cafés.
        Day 3: Versailles Palace day trip and evening shopping at Champs-Élysées.
        """
        prompt = f"{one_shot_example}\nUser: {user_input}\nAssistant:"

    elif PROMPT_MODE == "multi-shot":
        # Multiple examples provided before asking
        multi_shot_examples = """
        User: I want to visit Paris for 3 days. Suggest a travel itinerary.
        Assistant: Sure! Here's a 3-day itinerary for Paris:
        Day 1: Visit Eiffel Tower, Louvre Museum, and Seine River cruise.
        Day 2: Explore Montmartre, Sacré-Cœur, and local cafés.
        Day 3: Versailles Palace day trip and evening shopping at Champs-Élysées.

        User: Plan a 2-day trip to Rome.
        Assistant: Here's a 2-day itinerary for Rome:
        Day 1: Colosseum, Roman Forum, and Trevi Fountain.
        Day 2: Vatican City, Sistine Chapel, and St. Peter's Basilica.

        User: I want to explore New York for 4 days.
        Assistant: Here's a 4-day itinerary for New York City:
        Day 1: Times Square, Central Park, and Broadway show.
        Day 2: Statue of Liberty, Ellis Island, and Wall Street.
        Day 3: Metropolitan Museum of Art, Fifth Avenue shopping, and Empire State Building.
        Day 4: Brooklyn Bridge walk and Dumbo area exploration.
        """
        prompt = f"{multi_shot_examples}\nUser: {user_input}\nAssistant:"

    # API call
    response = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful travel assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content

if __name__ == "__main__":
    user_query = input("🧳 Welcome to Travel Assistant! Ask me anything travel-related: ")
    answer = ask_travel_assistant(user_query)
    print("\nAssistant:", answer)

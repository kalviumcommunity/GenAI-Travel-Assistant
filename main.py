import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file (requires GROQ_API_KEY)
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"  # Groq's OpenAI-compatible endpoint
)

# ✅ Set the mode & temperature manually here
MODE = "cot"            # Options: "zero-shot", "one-shot", "multi-shot", "dynamic", "cot"
TEMPERATURE = 0.7       # 0.0 = deterministic, 1.0 = creative/random

def build_messages(user_input: str, mode: str):
    """Return a messages[] array appropriate to the selected prompting mode."""
    system_msg = {
        "role": "system",
        "content": (
            "You are a helpful travel assistant. Provide accurate, practical plans with local tips, "
            "travel times when relevant, and realistic pacing."
        )
    }

    if mode == "zero-shot":
        return [system_msg, {"role": "user", "content": user_input}]

    if mode == "one-shot":
        example_q = "I am visiting Paris for 3 days. What should I do?"
        example_a = (
            "Here's a 3-day itinerary for Paris:\n"
            "Day 1: Eiffel Tower, Louvre, Seine cruise.\n"
            "Day 2: Montmartre, Sacré-Cœur, café-hopping.\n"
            "Day 3: Versailles day trip; evening in Le Marais."
        )
        return [
            system_msg,
            {"role": "user", "content": example_q},
            {"role": "assistant", "content": example_a},
            {"role": "user", "content": user_input},
        ]

    if mode == "multi-shot":
        examples = [
            ("I want to visit Paris for 3 days. Suggest a travel itinerary.",
             "Here's a 3-day itinerary for Paris:\n"
             "Day 1: Eiffel Tower, Louvre, Seine cruise.\n"
             "Day 2: Montmartre, Sacré-Cœur, café-hopping.\n"
             "Day 3: Versailles; Champs-Élysées evening."),
            ("Plan a 2-day trip to Rome.",
             "2-day Rome plan:\n"
             "Day 1: Colosseum, Roman Forum, Trevi Fountain.\n"
             "Day 2: Vatican Museums, Sistine Chapel, St. Peter's Basilica."),
            ("I want to explore New York for 4 days.",
             "4-day NYC plan:\n"
             "Day 1: Times Square, Central Park, Broadway show.\n"
             "Day 2: Statue of Liberty, Ellis Island, Wall Street.\n"
             "Day 3: The Met, Fifth Avenue, Empire State Building.\n"
             "Day 4: Brooklyn Bridge & DUMBO walk.")
        ]
        msgs = [system_msg]
        for q, a in examples:
            msgs.append({"role": "user", "content": q})
            msgs.append({"role": "assistant", "content": a})
        msgs.append({"role": "user", "content": user_input})
        return msgs

    if mode == "dynamic":
        text = user_input.lower()
        if "budget" in text:
            context = "Prioritize budget stays, free/cheap attractions, public transport, street food."
        elif "luxury" in text:
            context = "Prioritize 5-star hotels, fine dining, private tours, exclusive experiences."
        elif "family" in text or "kids" in text or "children" in text:
            context = "Prioritize family-friendly activities, shorter commute times, safety, and kid-friendly food."
        elif "solo" in text:
            context = "Prioritize safety, hostels/social tours, walkable areas, and flexible pacing."
        else:
            context = "Provide a balanced, practical itinerary with realistic timing."
        prompt = (
            f"User request: {user_input}\n"
            f"Context: {context}\n"
            "Return a day-wise plan with local tips and brief why-it-works notes."
        )
        return [system_msg, {"role": "user", "content": prompt}]

    if mode == "cot":
        cot_system = {
            "role": "system",
            "content": (
                "You are a meticulous travel planner. Plan internally first, but only output the final result. "
                "Do NOT include internal notes or step-by-step reasoning. "
                "Output must be concise and well-structured."
            )
        }
        user_prompt = (
            "Task: Create a realistic, day-wise itinerary matching the user's request.\n"
            "Output FORMAT (exactly these sections):\n"
            "Itinerary:\n"
            "- Day 1: ...\n"
            "- Day 2: ...\n"
            "(Continue days as needed)\n"
            "Budget: (currency + low–high per person, excluding flights)\n"
            "Rationale (brief):\n"
            "- 1 short bullet\n"
            "- 1 short bullet\n"
            "- 1 short bullet\n"
            "\nUser request: " + user_input + "\n"
            "Remember: do not reveal internal reasoning; provide only the final itinerary, budget, and brief rationale."
        )
        return [cot_system, system_msg, {"role": "user", "content": user_prompt}]

    return [system_msg, {"role": "user", "content": user_input}]  # fallback

def ask_travel_assistant(user_input: str, mode: str):
    messages = build_messages(user_input, mode)
    resp = client.chat.completions.create(
        model="llama3-70b-8192",
        messages=messages,
        temperature=TEMPERATURE, 
        max_tokens=700,
    )
    return resp.choices[0].message.content

if __name__ == "__main__":
    print(f"🧳 Welcome to AI-Travel Assistant")
    print(f"Mode = {MODE}, Temperature = {TEMPERATURE}\n")
    user_query = input("Ask your travel question: ")
    answer = ask_travel_assistant(user_query, MODE)
    print("\nAssistant:\n" + answer)

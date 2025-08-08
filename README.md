# GenAI Travel Assistant

A conversational assistant that helps users plan personalized trips based on interests, weather, and budget. The assistant answers natural language prompts, retrieves local travel guides, and returns structured trip plans.

## ✨ Features

| Feature            | Description                                                                 |
|--------------------|-----------------------------------------------------------------------------|
| Prompting          | Users ask in natural language (e.g., "Plan a 3-day trip to Himachal with a low budget and snow activities") |
| Retrieval (RAG)    | Retrieves travel guides (PDFs, text, markdown) using Retrieval-Augmented Generation |
| Structured Output  | Returns trip plan as JSON: destination, activities, weather, packing list, estimated cost |
| Function Calling   | Fetches real-time weather/location details via API calls                    |

## 🛠️ Tech Stack

- **Language Model:** OpenAI GPT-4o / GPT-4 (function calling support)
- **RAG:** LangChain + FAISS or ChromaDB
- **Weather API:** OpenWeatherMap (Free tier)
- **Server:** Python (Streamlit or FastAPI)
- **Data:** Local markdown/PDF files on destinations

## 🏗️ How It Works

1. **User Prompt:** User describes their trip requirements in natural language.
2. **RAG Retrieval:** System fetches relevant travel guides from local files.
3. **Function Calling:** Calls weather API for real-time forecasts.
4. **Structured Output:** Returns a detailed trip plan (destination, activities, weather, packing list, estimated cost).

## 🚀 Example Prompt

```
Plan a 3-day trip to Himachal with a low budget and snow activities
```

## 📦 Output Example

```json
{
    "destination": "Himachal Pradesh",
    "activities": ["Skiing", "Snowboarding", "Local sightseeing"],
    "weather": "Snowy, -2°C to 5°C",
    "packing_list": ["Warm clothes", "Snow boots", "Gloves"],
    "estimated_cost": "$150"
}
```











 
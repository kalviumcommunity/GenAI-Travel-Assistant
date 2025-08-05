# 🧳 GenAI Travel Assistant

A conversational AI travel planner that helps users design smart, personalized trips using natural language. It leverages the power of LLMs (GPT-4), Retrieval-Augmented Generation (RAG), structured output, and function calling to create travel itineraries with real-time data like weather, budgets, and packing lists.

---

## ✨ Features

- 💬 **Natural Prompting**  
  Ask questions like “Plan a budget 3-day trip to Goa in December” or “What should I pack for trekking in Himachal?”

- 🔍 **RAG (Retrieval-Augmented Generation)**  
  Retrieves travel info from locally stored guides using vector search (FAISS or ChromaDB)

- 📊 **Structured Output**  
  Returns trip plan as a well-defined JSON object: destination, activities, weather, budget, packing list

- 🔧 **Function Calling**  
  Calls external APIs (like OpenWeatherMap) to fetch live weather data for the destination

---

## 🧠 How It Works

1. **Prompting** – User inputs a travel request
2. **RAG** – Assistant searches relevant travel documents for context
3. **Function Calling** – Gets real-time weather info using an external API
4. **Structured Output** – Generates a clean, structured trip plan as a JSON object

---

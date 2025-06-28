# ✈️ Trip Planner Agent – AI Assistant for Booking Flights & Hotels

The **Trip Planner Agent** is an intelligent AI-powered assistant that helps users seamlessly plan trips by booking **flights** and **hotels** through natural language interaction. It leverages OpenAI models, LangChain, LangGraph, and Streamlit to orchestrate a multi-step agent workflow, offering a smooth, conversational travel planning experience.

---

## 🚀 Features

- 🧠 **Agentic Workflow** using LangGraph to handle multi-step tasks
- 🏨 **Hotel Booking** based on user city and date preferences
- ✈️ **Flight Search** based on origin, destination, and travel date
- 💬 **WhatsApp-style Chat UI** built with Streamlit for an intuitive user experience
- 🔗 Integrates external APIs (e.g., Amadeus or dummy data layer for flight/hotel)
- 🔄 Maintains context across user turns and tasks
- 🕒 Auto-scroll and message history within the UI

---

## 🛠️ Tech Stack

- **Python 3.10+**
- [LangGraph](https://www.langgraph.dev/) – for stateful multi-agent execution
- [LangChain](https://www.langchain.com/) – for chaining LLM-based tasks
- [Streamlit](https://streamlit.io/) – front-end UI
- [Amadeus API](https://developers.amadeus.com/) or mock APIs – for real-time hotel & flight data
- **OpenAI / Azure OpenAI API** – for LLM responses

---

## 📸 Demo
  
![Screenshot 2025-06-28 163038](https://github.com/user-attachments/assets/ca840b5f-5e13-4da2-b01e-934ca53d2e8f)

*A sleek, scrollable chat interface with fixed input like WhatsApp*

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/Trip-Planner-Agent.git
cd Trip-Planner-Agent
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt

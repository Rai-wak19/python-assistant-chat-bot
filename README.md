# AI Study Assistant

A simple and interactive AI-powered study assistant built with [Streamlit](https://streamlit.io/) and the [Google GenAI SDK](https://github.com/google/genai-python). 

This application uses the **Gemini 2.5 Flash** model and features **tool calling** capabilities. It can chat with you and automatically search through a database of study notes when asked relevant questions.

## Features

- **Interactive Chat Interface**: A clean, conversational UI built with Streamlit.
- **Powered by Gemini 2.5 Flash**: Utilizes the latest Gemini models for fast and intelligent responses.
- **Tool Calling Integration**: The assistant is equipped with a `search_notes` tool that it can autonomously trigger to fetch information from your study notes.
- **Session History**: Maintains conversation context across the chat session.

## Prerequisites

- Python 3.9+
- A Google Gemini API Key

## Setup & Installation

1. **Clone or download this repository.**
2. **Navigate to the project directory:**
   ```bash
   cd ai-study-assistant
   ```

3. **Install the dependencies:**
   It is recommended to use a virtual environment.
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables:**
   Create a `.env` file in the root directory (or update the existing one) and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   ```

## Running the Application

Start the Streamlit application by running the following command in your terminal:

```bash
streamlit run app.py
```

This will launch the app in your default web browser (usually at `http://localhost:8501`).

## How it Works

- `app.py`: Contains the Streamlit frontend, managing the chat UI and session state.
- `assistant.py`: Contains the core logic for the Gemini integration. It defines the `search_notes` tool, handles the tool-calling loop, and communicates with the Gemini API to provide answers.

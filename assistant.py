import os
from pathlib import Path
# pyrefly: ignore [missing-import]
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path, override=True)

def get_client() -> genai.Client:
    """
    Initializes and returns the Gemini client using either the environment variable
    or Streamlit secrets (useful when hosted on Streamlit Community Cloud).
    """
    load_dotenv(dotenv_path=env_path, override=True)
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        try:
            import streamlit as st
            if "GEMINI_API_KEY" in st.secrets:
                api_key = st.secrets["GEMINI_API_KEY"]
                os.environ["GEMINI_API_KEY"] = api_key
        except Exception:
            pass

    if not api_key:
        raise ValueError("GEMINI_API_KEY is missing. Please set it in your .env file or Streamlit secrets.")
    return genai.Client(
        api_key=api_key,
        http_options=types.HttpOptions(api_version="v1beta"),
    )

# 1. Define the tool (Python function)
def search_notes(query: str) -> str:
    """
    Searches the user's study notes for the given query.
    
    Args:
        query: The topic to search for in the notes (e.g., 'operating systems', 'transformers').
    """
    # Sample database stored in a simple dictionary for now
    notes_db = {
        "operating systems": "Operating Systems concepts include deadlock, paging, and processes.",
        "transformers": "Transformers use self-attention, encoders, and decoders."
    }
    
    # Simple search: convert to lowercase and check if query is in the keys
    query_lower = query.lower()
    
    # Error handling: check if we found a match, else return empty state message
    for topic, notes in notes_db.items():
        if query_lower in topic or topic in query_lower:
            return notes
            
    return f"No notes found for query: '{query}'. Let the user know."

def get_basic_llm_response(prompt: str) -> str:
    """
    Sends a prompt to the LLM and handles the tool-calling flow if the LLM requests it.
    """
    try:
        client = get_client()

        # 2. Configure the tool with Gemini
        # We pass our Python function in the `tools` list.
        # The SDK automatically converts its signature and docstring into a tool schema.
        config = types.GenerateContentConfig(
            system_instruction="You are a helpful AI Study Assistant. You can search the user's study notes using the search_notes tool. If the user asks a general question, use your general knowledge to answer it.",
            tools=[search_notes],
            http_options=types.HttpOptions(api_version="v1beta"),
        )
        
        # 3. First API call: User question -> Gemini
        # We use a list for `contents` so we can maintain conversation history.
        contents = [
            types.Content(role="user", parts=[types.Part.from_text(text=prompt)])
        ]
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=config,
        )
        
        # 4. Check if Gemini wants to call a tool
        if response.function_calls:
            # We append the model's response (which contains the tool request) to our history
            contents.append(response.candidates[0].content)
            
            # The model can request multiple tools at once, so we process all of them
            tool_responses = []
            for tool_call in response.function_calls:
                # 5. Python executes the tool
                tool_name = tool_call.name
                tool_args = tool_call.args
                
                print(f"\n[Tool Call Requested] Name: {tool_name}, Args: {tool_args}")
                
                if tool_name == "search_notes":
                    try:
                        # Error handling for invalid/missing tool arguments
                        query = tool_args.get("query")
                        if not query:
                            tool_result = "Error: Missing 'query' argument."
                        else:
                            # Execute our local Python function
                            tool_result = search_notes(query)
                    except Exception as e:
                        tool_result = f"Error executing tool: {str(e)}"
                else:
                    # Error handling for unknown tools
                    tool_result = f"Error: Unknown tool '{tool_name}'."
                
                print(f"[Tool Result] {tool_result}\n")
                
                # Format the tool execution result to send back to Gemini
                tool_responses.append(
                    types.Part.from_function_response(
                        name=tool_name,
                        response={"result": tool_result}
                    )
                )
            
            # 6. Send the tool result back to Gemini
            # We append the tool results to our history as a user message
            contents.append(
                types.Content(role="user", parts=tool_responses)
            )
            
            # Make the second API call so Gemini can read the results and generate the final answer
            final_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=config,
            )
            return final_response.text

        # If Gemini didn't want to call a tool, just return its initial text answer
        return response.text

    except Exception as e:
        # Error handling for Gemini API errors
        return f"Error communicating with Gemini: {str(e)}"

import streamlit as st
from assistant import get_basic_llm_response

# Basic Page Configuration
st.set_page_config(page_title="AI Study Assistant", page_icon="📚")

st.title("📚 AI Study Assistant")
st.write("Welcome! I'm here to help you study.")

# Initialize chat history in Streamlit session state
# Session state is a dictionary that persists across reruns of the script
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display existing chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input for the user
if prompt := st.chat_input("Ask a question..."):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get the LLM response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_basic_llm_response(prompt)
            st.markdown(response)
    
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

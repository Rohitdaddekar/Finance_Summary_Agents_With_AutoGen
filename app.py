import streamlit as st
from agents.command_agent import CommandAgent
from agents.rag_agent import RAGAgent
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

# Initialize agents
command_agent = CommandAgent("CommandAgent")
rag_agent = RAGAgent("RAGAgent")

def main():
    st.set_page_config(page_title="AI Agent Interface", layout="centered")

    # Streamlit app title and description
    st.title("AI Agent Finance Account Summary Generator")
    st.write(
        "This application allows you to interact with two AI agents: \n"
        "1. CommandAgent: Handles user commands.\n"
        "2. RAGAgent: Generates SQL queries, executes them, and provides results.\n"
    )

    # Input section for user command
    user_command = st.text_input("Enter your command (e.g., 'Give me account summary'):")

    # Button to process the command
    if st.button("Get Summary"):
        if user_command.strip():
            with st.spinner("Processing your request..."):
                # Pass the command to the CommandAgent
                response = command_agent.handle_request(user_command, rag_agent)

            # Display the final summary response
            st.success("Summary generated successfully!")
            st.text_area("Response from Command Agent:", value=response, height=200)
        else:
            st.error("Please enter a valid command.")

if __name__ == "__main__":
    main()

from agents.command_agent import CommandAgent
from agents.rag_agent import RAGAgent
import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

def main():
    # Initialize agents
    command_agent = CommandAgent("CommandAgent")
    rag_agent = RAGAgent("RAGAgent")

    # Simulate interactive user input
    user_command = input("Enter your command: ")

    # CommandAgent handles the request and interacts with RAGAgent
    response = command_agent.handle_request(user_command, rag_agent)

    # Print the final response
    print("Final Summary from Command Agent:")
    print(response)

if __name__ == "__main__":
    main()

from autogen.agentchat import UserProxyAgent

class CommandAgent(UserProxyAgent):
    def __init__(self, name):
        super().__init__(
            name=name,
            code_execution_config={
                "use_docker": False  # Disable Docker execution
            },
        )

    def handle_request(self, command, rag_agent):
        """
        Handle user commands dynamically and forward them to the RAGAgent.
        """
        # Forward any command to the RAGAgent
        try:
            print(f"Processing command: '{command}'")
            response = rag_agent.generate_summary(command)
            return response
        except Exception as e:
            return f"Error processing the command: {str(e)}"

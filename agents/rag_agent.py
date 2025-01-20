import os
import sqlite3
import pandas as pd
from autogen import AssistantAgent, OpenAIWrapper
from groq_config import GROQ_CONFIG
import re

class RAGAgent(AssistantAgent):
    def __init__(self, name, db_path="finance.db"):
        # Initialize OpenAIWrapper with Groq configuration
        self.model_client = OpenAIWrapper(config_list=GROQ_CONFIG)

        super().__init__(
            name=name,
            system_message="You are a SQL expert. Generate SQL queries to retrieve and summarize account data.",
            llm_config={"config_list": GROQ_CONFIG},  # Pass Groq config directly
        )
        self.db_path = db_path


    def generate_summary(self, user_input):
        """
        Generate a SQL query dynamically based on user input, execute it, and return a summary.
        """
        try:
            # Step 1: Generate SQL query dynamically
            query = self.generate_dynamic_query(user_input)

            # Step 2: Execute the query on the database
            result = self.execute_query(query)

            # Step 3: Summarize the query result
            return self.summarize_result(result, user_input)
        except Exception as e:
            return f"Error processing the command: {str(e)}"



    def generate_dynamic_query(self, user_input):
        """
        Generate a SQL query using the LLM model based on user input.
        """
        prompt = f"""
        Based on the database schema:
        1. accounts(account_id, account_holder, account_type, balance)
        - account_type: Indicates the type of account. Examples: 'Savings', 'Checking'.
        2. transactions(transaction_id, account_id, transaction_date, amount, transaction_type)
        3. aggregates(account_id, total_transactions, total_credits, total_debits, avg_transaction_amount)

        Generate a SQL query that matches the user input: "{user_input}".
        Match synonyms like "saving" to "Savings". Return only the query.
        """
        # Call the LLM using the 'create' method
        response = self.model_client.create(messages=[{"role": "user", "content": prompt}])
        raw_content = response.choices[0].message.content.strip()

        # Extract only the SQL query using regex
        sql_match = re.search(r"SELECT.*?;", raw_content, re.DOTALL | re.IGNORECASE)
        if sql_match:
            return sql_match.group(0).strip()
        else:
            raise ValueError("No valid SQL query found in the model's response.")



    def execute_query(self, query):
        """
        Execute the generated SQL query on the SQLite database.
        """
        try:
            conn = sqlite3.connect(self.db_path)
            df = pd.read_sql_query(query, conn)
            conn.close()
            return df
        except Exception as e:
            return f"Error executing query: {str(e)}"

    def summarize_result(self, result, user_input):
        """
        Summarize the query result into a readable and contextually relevant format.
        """
        if isinstance(result, pd.DataFrame):
            # Convert the DataFrame to a string representation
            result_text = result.to_string(index=False)

            # Use LLM to craft a user-friendly response
            prompt = f"""
            The user asked: "{user_input}"
            The database returned the following result:
            {result_text}

            Generate a natural language response to summarize the result in a helpful and user-friendly manner.
            """
            response = self.model_client.create(messages=[{"role": "user", "content": prompt}])
            return response.choices[0].message.content.strip()

        else:
            # Handle errors gracefully
            return f"Error: {result}"


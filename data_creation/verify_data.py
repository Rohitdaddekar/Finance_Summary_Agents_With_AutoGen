import pandas as pd
import sqlite3

def view_data_with_pandas():
    conn = sqlite3.connect('finance.db')

    # Fetch Accounts
    accounts_df = pd.read_sql_query("SELECT * FROM accounts", conn)
    print("Accounts Table:")
    print(accounts_df)

    # Fetch Transactions
    transactions_df = pd.read_sql_query("SELECT * FROM transactions", conn)
    print("\nTransactions Table:")
    print(transactions_df)

    conn.close()

if __name__ == "__main__":
    view_data_with_pandas()

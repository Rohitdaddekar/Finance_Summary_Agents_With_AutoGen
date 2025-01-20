import random
from faker import Faker
import sqlite3


def compute_aggregates():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Compute aggregates for each account
    cursor.execute("""
    INSERT INTO aggregates (account_id, total_transactions, total_credits, total_debits, avg_transaction_amount)
    SELECT
        account_id,
        COUNT(transaction_id) AS total_transactions,
        SUM(CASE WHEN amount > 0 THEN amount ELSE 0 END) AS total_credits,
        SUM(CASE WHEN amount < 0 THEN -amount ELSE 0 END) AS total_debits,
        AVG(ABS(amount)) AS avg_transaction_amount
    FROM transactions
    GROUP BY account_id
    """)

    print("Aggregates computed and inserted successfully.")
    conn.commit()
    conn.close()


if __name__ == "__main__":
    # Compute aggregates after generating data
    compute_aggregates()
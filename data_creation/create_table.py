import sqlite3

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Create Accounts Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    account_id INTEGER PRIMARY KEY,
    account_holder TEXT,
    account_type TEXT,
    balance REAL
)
""")

# Create Transactions Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY,
    account_id INTEGER,
    transaction_date TEXT,
    amount REAL,
    transaction_type TEXT,
    FOREIGN KEY (account_id) REFERENCES accounts (account_id)
)
""")

# Create the aggregates table
cursor.execute("""
CREATE TABLE IF NOT EXISTS aggregates (
    account_id INTEGER PRIMARY KEY,
    total_transactions INTEGER,
    total_credits REAL,
    total_debits REAL,
    avg_transaction_amount REAL,
    FOREIGN KEY (account_id) REFERENCES accounts (account_id)
)
""")

print("Database and tables created successfully.")
conn.commit()
conn.close()

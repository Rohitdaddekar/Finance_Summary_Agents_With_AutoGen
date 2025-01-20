import random
from faker import Faker
import sqlite3

fake = Faker()

# Connect to database
conn = sqlite3.connect('finance.db')
cursor = conn.cursor()

# Generate and insert sample accounts
account_types = ['Savings', 'Checking']
accounts = [
    (i, fake.name(), random.choice(account_types), round(random.uniform(500, 5000), 2))
    for i in range(1, 101)  # Generate 100 accounts
]
cursor.executemany("INSERT INTO accounts VALUES (?, ?, ?, ?)", accounts)

# Generate and insert sample transactions
transactions = []
for account_id in range(1, 101):
    for _ in range(random.randint(5, 15)):  # 5-15 transactions per account
        transaction_type = random.choice(['Credit', 'Debit'])
        amount = round(random.uniform(10, 1000), 2)
        transactions.append((
            len(transactions) + 1,  # Unique transaction ID
            account_id,
            fake.date_between(start_date='-2y', end_date='today').isoformat(),
            amount if transaction_type == 'Credit' else -amount,
            transaction_type
        ))
cursor.executemany("INSERT INTO transactions VALUES (?, ?, ?, ?, ?)", transactions)

print("Sample data inserted successfully.")

conn.commit()
conn.close()

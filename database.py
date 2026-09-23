import sqlite3
connection = sqlite3.connect("sacco.db")
cursor = connection.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS members (
    member_id TEXT PRIMARY KEY,
    full_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    registration_date TEXT NOT NULL
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS savings (
    savings_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    amount REAL NOT NULL,
    transaction_date TEXT NOT NULL,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS loans (
    loan_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id TEXT NOT NULL,
    loan_amount REAL NOT NULL,
    application_date TEXT NOT NULL,
    status TEXT NOT NULL,
    approval_date TEXT,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS loan_repayments (
    repayment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    loan_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    repayment_date TEXT NOT NULL,
    FOREIGN KEY (loan_id) REFERENCES loans(loan_id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    member_id TEXT NOT NULL,
    transaction_type TEXT NOT NULL,
    amount REAL NOT NULL,
    transaction_date TEXT NOT NULL,
    description TEXT,
    FOREIGN KEY (member_id) REFERENCES members(member_id)
)
""")
connection.commit()
connection.close()



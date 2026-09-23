import sqlite3
from datetime import date
def deposit():
    member_id = input("Enter Member ID: ").strip()

    try:
        amount = float(input("Enter deposit amount: "))

        if amount <= 0:
            print("Deposit amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid amount.")
        return

    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM members WHERE member_id = ?",
        (member_id,)
    )

    member = cursor.fetchone()

    if not member:
        print("Member not found.")
        connection.close()
        return

    transaction_date = date.today().isoformat()

    cursor.execute("""
        INSERT INTO savings
        (member_id, transaction_type, amount, transaction_date)
        VALUES (?, ?, ?, ?)
    """, (member_id, "Deposit", amount, transaction_date))

    cursor.execute("""
        INSERT INTO transactions
        (member_id, transaction_type, amount, transaction_date, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        member_id,
        "Deposit",
        amount,
        transaction_date,
        "Savings deposit"
    ))

    connection.commit()
    connection.close()

    print("Deposit successful.")

def withdraw():
    member_id = input("Enter Member ID: ").strip()

    try:
        amount = float(input("Enter withdrawal amount: "))

        if amount <= 0:
            print("Withdrawal amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid amount.")
        return

    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM members WHERE member_id = ?",
        (member_id,)
    )

    member = cursor.fetchone()

    if not member:
        print("Member not found.")
        connection.close()
        return

    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN transaction_type = 'Deposit' THEN amount ELSE 0 END), 0)
            -
            COALESCE(SUM(CASE WHEN transaction_type = 'Withdrawal' THEN amount ELSE 0 END), 0)
        FROM savings
        WHERE member_id = ?
    """, (member_id,))

    balance = cursor.fetchone()[0]

    if amount > balance:
        print("Insufficient savings balance.")
        connection.close()
        return

    transaction_date = date.today().isoformat()

    cursor.execute("""
        INSERT INTO savings
        (member_id, transaction_type, amount, transaction_date)
        VALUES (?, ?, ?, ?)
    """, (member_id, "Withdrawal", amount, transaction_date))

    cursor.execute("""
        INSERT INTO transactions
        (member_id, transaction_type, amount, transaction_date, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        member_id,
        "Withdrawal",
        amount,
        transaction_date,
        "Savings withdrawal"
    ))

    connection.commit()
    connection.close()

    print("Withdrawal successful.")

def check_balance():
    member_id = input("Enter Member ID: ").strip()

    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM members WHERE member_id = ?",
        (member_id,)
    )

    member = cursor.fetchone()

    if not member:
        print("Member not found.")
        connection.close()
        return

    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN transaction_type = 'Deposit' THEN amount ELSE 0 END), 0)
            -
            COALESCE(SUM(CASE WHEN transaction_type = 'Withdrawal' THEN amount ELSE 0 END), 0)
        FROM savings
        WHERE member_id = ?
    """, (member_id,))

    balance = cursor.fetchone()[0]

    connection.close()

    print("\n========== SAVINGS BALANCE ==========")
    print("Member ID:", member_id)
    print("Member Name:", member[1])
    print("Savings Balance:", balance)

def savings_history():
    member_id = input("Enter Member ID: ").strip()

    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    # Check whether the member exists
    cursor.execute(
        "SELECT * FROM members WHERE member_id = ?",
        (member_id,)
    )

    member = cursor.fetchone()

    if not member:
        print("Member not found.")
        connection.close()
        return

    # Get all savings transactions for the member
    cursor.execute("""
        SELECT transaction_type, amount, transaction_date
        FROM savings
        WHERE member_id = ?
        ORDER BY savings_id
    """, (member_id,))

    transactions = cursor.fetchall()

    connection.close()

    if not transactions:
        print("No savings transactions found.")
        return

    print("\n========== SAVINGS HISTORY ==========")
    print("Member ID:", member_id)
    print("Member Name:", member[1])
    print("-------------------------------------")

    for transaction in transactions:
        print("Transaction Type:", transaction[0])
        print("Amount:", transaction[1])
        print("Date:", transaction[2])
        print("-------------------------------------")

def total_savings():
    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(CASE WHEN transaction_type = 'Deposit' THEN amount ELSE 0 END), 0)
            -
            COALESCE(SUM(CASE WHEN transaction_type = 'Withdrawal' THEN amount ELSE 0 END), 0)
        FROM savings
    """)

    total = cursor.fetchone()[0]

    connection.close()

    print("\n========== TOTAL SACCO SAVINGS ==========")
    print("Total SACCO Savings:", total)







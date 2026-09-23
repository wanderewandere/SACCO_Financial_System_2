import sqlite3
from datetime import date

def apply_loan():
    member_id = input("Enter Member ID: ").strip()

    try:
        loan_amount = float(input("Enter Loan Amount: "))

        if loan_amount <= 0:
            print("Loan amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid loan amount.")
        return

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

    application_date = date.today().isoformat()

    # Insert the loan application
    cursor.execute("""
        INSERT INTO loans
        (member_id, loan_amount, application_date, status)
        VALUES (?, ?, ?, ?)
    """, (
        member_id,
        loan_amount,
        application_date,
        "Pending"
    ))

    connection.commit()
    connection.close()

    print("Loan application submitted successfully.")

def view_loans():
    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT loan_id, member_id, loan_amount, application_date, status
        FROM loans
        ORDER BY loan_id
    """)

    loans = cursor.fetchall()

    connection.close()

    if not loans:
        print("No loan applications found.")
        return

    print("\n========== LOAN APPLICATIONS ==========")

    for loan in loans:
        print("Loan ID:", loan[0])
        print("Member ID:", loan[1])
        print("Loan Amount:", loan[2])
        print("Application Date:", loan[3])
        print("Status:", loan[4])
        print("--------------------------------------")

def approve_or_reject_loan():
    try:
        loan_id = int(input("Enter Loan ID: "))

    except ValueError:
        print("Please enter a valid Loan ID.")
        return

    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    # Find the loan
    cursor.execute(
        "SELECT * FROM loans WHERE loan_id = ?",
        (loan_id,)
    )

    loan = cursor.fetchone()

    if not loan:
        print("Loan not found.")
        connection.close()
        return

    # Check whether the loan has already been processed
    if loan[4] != "Pending":
        print("This loan has already been processed.")
        connection.close()
        return

    decision = input(
        "Enter decision (approve/reject): "
    ).strip().lower()

    if decision == "approve":
        status = "Approved"
        approval_date = date.today().isoformat()

        cursor.execute("""
            UPDATE loans
            SET status = ?, approval_date = ?
            WHERE loan_id = ?
        """, (status, approval_date, loan_id))

        print("Loan approved successfully.")

    elif decision == "reject":
        status = "Rejected"

        cursor.execute("""
            UPDATE loans
            SET status = ?
            WHERE loan_id = ?
        """, (status, loan_id))

        print("Loan rejected.")

    else:
        print("Invalid decision. Please enter approve or reject.")
        connection.close()
        return

    connection.commit()
    connection.close()

def make_repayment():
    try:
        loan_id = int(input("Enter Loan ID: "))

    except ValueError:
        print("Please enter a valid Loan ID.")
        return

    try:
        repayment_amount = float(input("Enter repayment amount: "))

        if repayment_amount <= 0:
            print("Repayment amount must be greater than zero.")
            return

    except ValueError:
        print("Please enter a valid repayment amount.")
        return

    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    # Find the loan
    cursor.execute(
        "SELECT * FROM loans WHERE loan_id = ?",
        (loan_id,)
    )

    loan = cursor.fetchone()

    if not loan:
        print("Loan not found.")
        connection.close()
        return

    # Check whether the loan is approved
    if loan[4] != "Approved":
        print("Only approved loans can receive repayments.")
        connection.close()
        return

    # Calculate total repayments already made
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM loan_repayments
        WHERE loan_id = ?
    """, (loan_id,))

    total_repaid = cursor.fetchone()[0]

    # Calculate the outstanding balance
    outstanding_balance = loan[2] - total_repaid

    # Check whether repayment is greater than the outstanding balance
    if repayment_amount > outstanding_balance:
        print("Repayment exceeds the outstanding loan balance.")
        connection.close()
        return

    repayment_date = date.today().isoformat()

    # Record the repayment
    cursor.execute("""
        INSERT INTO loan_repayments
        (loan_id, amount, repayment_date)
        VALUES (?, ?, ?)
    """, (
        loan_id,
        repayment_amount,
        repayment_date
    ))

    # Also record it in the general transactions table
    cursor.execute("""
        INSERT INTO transactions
        (member_id, transaction_type, amount, transaction_date, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        loan[1],
        "Loan Repayment",
        repayment_amount,
        repayment_date,
        "Loan repayment"
    ))

    connection.commit()
    connection.close()

    print("Loan repayment recorded successfully.")
# STEP 6.41 - Check outstanding loan balance
def check_loan_balance():
    try:
        loan_id = int(input("Enter Loan ID: "))

    except ValueError:
        print("Please enter a valid Loan ID.")
        return

    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    # Find the loan
    cursor.execute(
        "SELECT * FROM loans WHERE loan_id = ?",
        (loan_id,)
    )

    loan = cursor.fetchone()

    if not loan:
        print("Loan not found.")
        connection.close()
        return

    # Calculate total repayments
    cursor.execute("""
        SELECT COALESCE(SUM(amount), 0)
        FROM loan_repayments
        WHERE loan_id = ?
    """, (loan_id,))

    total_repaid = cursor.fetchone()[0]

    # Calculate outstanding balance
    outstanding_balance = loan[2] - total_repaid

    connection.close()

    print("\n========== LOAN BALANCE ==========")
    print("Loan ID:", loan[0])
    print("Member ID:", loan[1])
    print("Original Loan Amount:", loan[2])
    print("Total Repaid:", total_repaid)
    print("Outstanding Balance:", outstanding_balance)
    print("Loan Status:", loan[4])
# STEP 6.42 - View loan repayment history
def repayment_history():
    try:
        loan_id = int(input("Enter Loan ID: "))

    except ValueError:
        print("Please enter a valid Loan ID.")
        return

    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    # Check whether the loan exists
    cursor.execute(
        "SELECT * FROM loans WHERE loan_id = ?",
        (loan_id,)
    )

    loan = cursor.fetchone()

    if not loan:
        print("Loan not found.")
        connection.close()
        return

    # Get all repayments for the loan
    cursor.execute("""
        SELECT repayment_id, amount, repayment_date
        FROM loan_repayments
        WHERE loan_id = ?
        ORDER BY repayment_id
    """, (loan_id,))

    repayments = cursor.fetchall()

    connection.close()

    if not repayments:
        print("No repayments found for this loan.")
        return

    print("\n========== LOAN REPAYMENT HISTORY ==========")
    print("Loan ID:", loan_id)
    print("Member ID:", loan[1])
    print("--------------------------------------------")

    for repayment in repayments:
        print("Repayment ID:", repayment[0])
        print("Amount:", repayment[1])
        print("Date:", repayment[2])
        print("--------------------------------------------")
# STEP 6.43 - Calculate total loans issued
def total_loans_issued():
    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(loan_amount), 0)
        FROM loans
        WHERE status = 'Approved'
    """)

    total = cursor.fetchone()[0]

    connection.close()

    print("\n========== TOTAL LOANS ISSUED ==========")
    print("Total Loans Issued:", total)
# STEP 6.44 - Calculate total outstanding loans
def total_outstanding_loans():
    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(SUM(loan_amount), 0)
            -
            COALESCE((
                SELECT SUM(amount)
                FROM loan_repayments
            ), 0)
        FROM loans
        WHERE status = 'Approved'
    """)

    total_outstanding = cursor.fetchone()[0]

    connection.close()

    print("\n========== TOTAL OUTSTANDING LOANS ==========")
    print("Total Outstanding Loans:", total_outstanding)
# STEP 6.45 - Loan repayment report
def loan_repayment_report():
    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            loan_repayments.repayment_id,
            loan_repayments.loan_id,
            loans.member_id,
            loan_repayments.amount,
            loan_repayments.repayment_date
        FROM loan_repayments
        INNER JOIN loans
        ON loan_repayments.loan_id = loans.loan_id
        ORDER BY loan_repayments.repayment_id
    """)

    repayments = cursor.fetchall()

    connection.close()

    if not repayments:
        print("No loan repayments found.")
        return

    print("\n========== LOAN REPAYMENT REPORT ==========")

    for repayment in repayments:
        print("Repayment ID:", repayment[0])
        print("Loan ID:", repayment[1])
        print("Member ID:", repayment[2])
        print("Amount Repaid:", repayment[3])
        print("Repayment Date:", repayment[4])
        print("------------------------------------------")
# STEP 6.46 - Loan outstanding balance report
def loan_outstanding_report():
    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            loans.loan_id,
            loans.member_id,
            loans.loan_amount,
            COALESCE(SUM(loan_repayments.amount), 0)
        FROM loans
        LEFT JOIN loan_repayments
        ON loans.loan_id = loan_repayments.loan_id
        WHERE loans.status = 'Approved'
        GROUP BY loans.loan_id
        ORDER BY loans.loan_id
    """)

    loans = cursor.fetchall()

    connection.close()

    if not loans:
        print("No approved loans found.")
        return

    print("\n========== LOAN OUTSTANDING BALANCE REPORT ==========")

    for loan in loans:
        loan_id = loan[0]
        member_id = loan[1]
        loan_amount = loan[2]
        total_repaid = loan[3]

        outstanding_balance = loan_amount - total_repaid

        print("Loan ID:", loan_id)
        print("Member ID:", member_id)
        print("Original Loan Amount:", loan_amount)
        print("Total Repaid:", total_repaid)
        print("Outstanding Balance:", outstanding_balance)
        print("-----------------------------------------------")





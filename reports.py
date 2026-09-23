import sqlite3
# STEP 6.47 - Member list report
def member_list_report():
    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT member_id, full_name, phone, email, registration_date
        FROM members
        ORDER BY member_id
    """)

    members = cursor.fetchall()

    connection.close()

    if not members:
        print("No members registered.")
        return

    print("\n========== MEMBER LIST REPORT ==========")

    for member in members:
        print("Member ID:", member[0])
        print("Full Name:", member[1])
        print("Phone:", member[2])
        print("Email:", member[3])
        print("Registration Date:", member[4])
        print("----------------------------------------")
# STEP 6.48 - Individual financial statement
def individual_financial_statement():
    member_id = input("Enter Member ID: ").strip()

    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    # Find the member
    cursor.execute(
        "SELECT * FROM members WHERE member_id = ?",
        (member_id,)
    )

    member = cursor.fetchone()

    if not member:
        print("Member not found.")
        connection.close()
        return

    print("\n========== INDIVIDUAL FINANCIAL STATEMENT ==========")
    print("Member ID:", member[0])
    print("Full Name:", member[1])
    print("Phone:", member[2])
    print("Email:", member[3])
    print("Registration Date:", member[4])

    # Calculate savings balance
    cursor.execute("""
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN transaction_type = 'Deposit' THEN amount
                        ELSE 0
                    END
                ), 0
            )
            -
            COALESCE(
                SUM(
                    CASE
                        WHEN transaction_type = 'Withdrawal' THEN amount
                        ELSE 0
                    END
                ), 0
            )
        FROM savings
        WHERE member_id = ?
    """, (member_id,))

    savings_balance = cursor.fetchone()[0]

    print("\nSavings Balance:", savings_balance)

    # Get loans
    cursor.execute("""
        SELECT loan_id, loan_amount, status
        FROM loans
        WHERE member_id = ?
        ORDER BY loan_id
    """, (member_id,))

    loans = cursor.fetchall()

    if not loans:
        print("\nNo loans found.")
    else:
        print("\n---------- LOAN INFORMATION ----------")

        for loan in loans:
            loan_id = loan[0]
            loan_amount = loan[1]
            status = loan[2]

        print("Loan ID:", loan_id)
        print("Loan Amount:", loan_amount)
        print("Status:", status)

        if status == "Approved":
            # Calculate repayments for this loan
            cursor.execute("""
                           SELECT COALESCE(SUM(amount), 0)
                           FROM loan_repayments
                           WHERE loan_id = ?
                           """, (loan_id,))

            total_repaid = cursor.fetchone()[0]

            outstanding = loan_amount - total_repaid

            print("Total Repaid:", total_repaid)
            print("Outstanding Balance:", outstanding)

        else:
            print("Total Repaid: 0")
            print("Outstanding Balance: 0")

        print("--------------------------------------")
# STEP 6.49 - Total savings report
def total_savings_report():
    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COALESCE(
                SUM(
                    CASE
                        WHEN transaction_type = 'Deposit' THEN amount
                        ELSE 0
                    END
                ), 0
            )
            -
            COALESCE(
                SUM(
                    CASE
                        WHEN transaction_type = 'Withdrawal' THEN amount
                        ELSE 0
                    END
                ), 0
            )
        FROM savings
    """)

    total_savings = cursor.fetchone()[0]

    connection.close()

    print("\n========== TOTAL SAVINGS REPORT ==========")
    print("Total SACCO Savings:", total_savings)
# STEP 6.50 - Total loans issued report
def total_loans_issued_report():
    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(loan_amount), 0)
        FROM loans
        WHERE status = 'Approved'
    """)

    total_loans = cursor.fetchone()[0]

    connection.close()

    print("\n========== TOTAL LOANS ISSUED REPORT ==========")
    print("Total Loans Issued:", total_loans)
# STEP 6.51 - Outstanding loans report
def outstanding_loans_report():
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
        print("No outstanding loans found.")
        return

    print("\n========== OUTSTANDING LOANS REPORT ==========")

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
        print("---------------------------------------------")
# STEP 6.52 - Loan repayment report
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
# STEP 6.53 - Transaction report
def transaction_report():
    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            transaction_id,
            member_id,
            transaction_type,
            amount,
            transaction_date,
            description
        FROM transactions
        ORDER BY transaction_id
    """)

    transactions = cursor.fetchall()

    connection.close()

    if not transactions:
        print("No transactions found.")
        return

    print("\n========== TRANSACTION REPORT ==========")

    for transaction in transactions:
        print("Transaction ID:", transaction[0])
        print("Member ID:", transaction[1])
        print("Transaction Type:", transaction[2])
        print("Amount:", transaction[3])
        print("Transaction Date:", transaction[4])
        print("Description:", transaction[5])
        print("---------------------------------------")

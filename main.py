import members
import savings
import loans
import reports
# STEP 6.55 - Member management menu
def member_menu():
    while True:
        print("\n========== MEMBER MANAGEMENT ==========")
        print("1. Register Member")
        print("2. View Members")
        print("3. Search Member")
        print("4. Update Member")
        print("5. Delete Member")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            members.register_member()

        elif choice == "2":
            members.view_members()

        elif choice == "3":
            members.search_member()

        elif choice == "4":
            members.update_member()

        elif choice == "5":
            members.delete_member()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")

# STEP 6.57 - Savings management menu
def savings_menu():
    while True:
        print("\n========== SAVINGS MANAGEMENT ==========")
        print("1. Make Deposit")
        print("2. Make Withdrawal")
        print("3. Check Savings Balance")
        print("4. View Savings History")
        print("5. View Total SACCO Savings")
        print("6. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            savings.deposit()

        elif choice == "2":
            savings.withdraw()

        elif choice == "3":
            savings.check_balance()

        elif choice == "4":
            savings.savings_history()

        elif choice == "5":
            savings.total_savings()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")

# STEP 6.58 - Loan management menu
def loan_menu():
    while True:
        print("\n========== LOAN MANAGEMENT ==========")
        print("1. Apply for Loan")
        print("2. View Loan Applications")
        print("3. Approve or Reject Loan")
        print("4. Make Loan Repayment")
        print("5. Check Loan Balance")
        print("6. View Repayment History")
        print("7. View Total Loans Issued")
        print("8. View Total Outstanding Loans")
        print("9. View Loan Repayment Report")
        print("10. View Outstanding Loan Report")
        print("11. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            loans.apply_loan()

        elif choice == "2":
            loans.view_loans()

        elif choice == "3":
            loans.approve_or_reject_loan()

        elif choice == "4":
            loans.make_repayment()

        elif choice == "5":
            loans.check_loan_balance()

        elif choice == "6":
            loans.repayment_history()

        elif choice == "7":
            loans.total_loans_issued()

        elif choice == "8":
            loans.total_outstanding_loans()

        elif choice == "9":
            loans.loan_repayment_report()

        elif choice == "10":
            loans.loan_outstanding_report()

        elif choice == "11":
            break

        else:
            print("Invalid choice. Please try again.")

# STEP 6.59 - Reports menu
def reports_menu():
    while True:
        print("\n========== REPORTS ==========")
        print("1. Member List Report")
        print("2. Individual Financial Statement")
        print("3. Total Savings Report")
        print("4. Total Loans Issued Report")
        print("5. Outstanding Loans Report")
        print("6. Loan Repayment Report")
        print("7. Transaction Report")
        print("8. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            reports.member_list_report()

        elif choice == "2":
            reports.individual_financial_statement()

        elif choice == "3":
            reports.total_savings_report()

        elif choice == "4":
            reports.total_loans_issued_report()

        elif choice == "5":
            reports.outstanding_loans_report()

        elif choice == "6":
            reports.loan_repayment_report()

        elif choice == "7":
            reports.transaction_report()

        elif choice == "8":
            break

        else:
            print("Invalid choice. Please try again.")

# STEP 6.60 - Main menu
def main_menu():
    while True:
        print("\n==============================================")
        print("     SACCO FINANCIAL MANAGEMENT SYSTEM")
        print("==============================================")
        print("1. Member Management")
        print("2. Savings Management")
        print("3. Loan Management")
        print("4. Reports")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            member_menu()

        elif choice == "2":
            savings_menu()

        elif choice == "3":
            loan_menu()

        elif choice == "4":
            reports_menu()

        elif choice == "5":
            print("Thank you for using the SACCO Financial Management System.")
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")



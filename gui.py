import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
from datetime import date


# =========================================================
# MEMBER MANAGEMENT
# =========================================================

def register_member_gui():
    member_window = tk.Toplevel(window)
    member_window.title("Register Member")
    member_window.geometry("500x500")

    tk.Label(
        member_window,
        text="REGISTER MEMBER",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(member_window, text="Member ID").pack()
    member_id_entry = tk.Entry(member_window, width=30)
    member_id_entry.pack(pady=8)

    tk.Label(member_window, text="Full Name").pack()
    name_entry = tk.Entry(member_window, width=30)
    name_entry.pack(pady=8)

    tk.Label(member_window, text="Phone").pack()
    phone_entry = tk.Entry(member_window, width=30)
    phone_entry.pack(pady=8)

    tk.Label(member_window, text="Email").pack()
    email_entry = tk.Entry(member_window, width=30)
    email_entry.pack(pady=8)

    def save_member():
        member_id = member_id_entry.get().strip()
        full_name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()

        if not member_id or not full_name or not phone or not email:
            messagebox.showerror("Error", "All fields are required.")
            return

        registration_date = date.today().isoformat()

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO members
                (member_id, full_name, phone, email, registration_date)
                VALUES (?, ?, ?, ?, ?)
            """, (
                member_id,
                full_name,
                phone,
                email,
                registration_date
            ))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Member registered successfully."
            )

            member_id_entry.delete(0, tk.END)
            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)

        except sqlite3.IntegrityError:
            messagebox.showerror(
                "Error",
                "Member ID already exists."
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        member_window,
        text="Register",
        width=25,
        command=save_member
    ).pack(pady=20)

    tk.Button(
        member_window,
        text="Back",
        width=25,
        command=member_window.destroy
    ).pack()


def view_members_gui():
    view_window = tk.Toplevel(window)
    view_window.title("View Members")
    view_window.geometry("800x450")

    tk.Label(
        view_window,
        text="REGISTERED MEMBERS",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    columns = (
        "Member ID",
        "Full Name",
        "Phone",
        "Email",
        "Registration Date"
    )

    tree = ttk.Treeview(
        view_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=140)

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    try:
        connection = sqlite3.connect("sacco.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                member_id,
                full_name,
                phone,
                email,
                registration_date
            FROM members
            ORDER BY member_id
        """)

        members = cursor.fetchall()
        connection.close()

        for member in members:
            tree.insert("", tk.END, values=member)

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            str(error)
        )

    tk.Button(
        view_window,
        text="Back",
        width=20,
        command=view_window.destroy
    ).pack(pady=10)


def search_member_gui():
    search_window = tk.Toplevel(window)
    search_window.title("Search Member")
    search_window.geometry("500x400")

    tk.Label(
        search_window,
        text="SEARCH MEMBER",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        search_window,
        text="Enter Member ID"
    ).pack()

    member_id_entry = tk.Entry(
        search_window,
        width=30
    )
    member_id_entry.pack(pady=10)

    result_label = tk.Label(
        search_window,
        text="",
        font=("Arial", 11),
        justify="left"
    )
    result_label.pack(pady=20)

    def search():
        member_id = member_id_entry.get().strip()

        if not member_id:
            messagebox.showerror(
                "Error",
                "Please enter a Member ID."
            )
            return

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    member_id,
                    full_name,
                    phone,
                    email,
                    registration_date
                FROM members
                WHERE member_id = ?
            """, (member_id,))

            member = cursor.fetchone()
            connection.close()

            if member:
                result_label.config(
                    text=
                    "Member ID: " + member[0] +
                    "\nFull Name: " + member[1] +
                    "\nPhone: " + member[2] +
                    "\nEmail: " + member[3] +
                    "\nRegistration Date: " + member[4]
                )
            else:
                result_label.config(
                    text="Member not found."
                )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        search_window,
        text="Search",
        width=25,
        command=search
    ).pack(pady=10)

    tk.Button(
        search_window,
        text="Back",
        width=25,
        command=search_window.destroy
    ).pack(pady=10)


def update_member_gui():
    update_window = tk.Toplevel(window)
    update_window.title("Update Member")
    update_window.geometry("500x500")

    tk.Label(
        update_window,
        text="UPDATE MEMBER",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(update_window, text="Member ID").pack()
    member_id_entry = tk.Entry(update_window, width=30)
    member_id_entry.pack(pady=8)

    tk.Label(update_window, text="New Full Name").pack()
    name_entry = tk.Entry(update_window, width=30)
    name_entry.pack(pady=8)

    tk.Label(update_window, text="New Phone").pack()
    phone_entry = tk.Entry(update_window, width=30)
    phone_entry.pack(pady=8)

    tk.Label(update_window, text="New Email").pack()
    email_entry = tk.Entry(update_window, width=30)
    email_entry.pack(pady=8)

    def load_member():
        member_id = member_id_entry.get().strip()

        if not member_id:
            messagebox.showerror(
                "Error",
                "Please enter a Member ID."
            )
            return

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT full_name, phone, email
                FROM members
                WHERE member_id = ?
            """, (member_id,))

            member = cursor.fetchone()
            connection.close()

            if not member:
                messagebox.showerror(
                    "Not Found",
                    "Member not found."
                )
                return

            name_entry.delete(0, tk.END)
            phone_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)

            name_entry.insert(0, member[0])
            phone_entry.insert(0, member[1])
            email_entry.insert(0, member[2])

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def update():
        member_id = member_id_entry.get().strip()
        full_name = name_entry.get().strip()
        phone = phone_entry.get().strip()
        email = email_entry.get().strip()

        if not member_id or not full_name or not phone or not email:
            messagebox.showerror(
                "Error",
                "All fields are required."
            )
            return

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE members
                SET full_name = ?,
                    phone = ?,
                    email = ?
                WHERE member_id = ?
            """, (
                full_name,
                phone,
                email,
                member_id
            ))

            connection.commit()

            if cursor.rowcount == 0:
                connection.close()
                messagebox.showerror(
                    "Not Found",
                    "Member not found."
                )
                return

            connection.close()

            messagebox.showinfo(
                "Success",
                "Member details updated successfully."
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        update_window,
        text="Load Member",
        width=25,
        command=load_member
    ).pack(pady=10)

    tk.Button(
        update_window,
        text="Update Member",
        width=25,
        command=update
    ).pack(pady=10)

    tk.Button(
        update_window,
        text="Back",
        width=25,
        command=update_window.destroy
    ).pack(pady=10)


def delete_member_gui():
    delete_window = tk.Toplevel(window)
    delete_window.title("Delete Member")
    delete_window.geometry("500x350")

    tk.Label(
        delete_window,
        text="DELETE MEMBER",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        delete_window,
        text="Enter Member ID"
    ).pack()

    member_id_entry = tk.Entry(
        delete_window,
        width=30
    )
    member_id_entry.pack(pady=10)

    def delete_member():
        member_id = member_id_entry.get().strip()

        if not member_id:
            messagebox.showerror(
                "Error",
                "Please enter a Member ID."
            )
            return

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT full_name
                FROM members
                WHERE member_id = ?
            """, (member_id,))

            member = cursor.fetchone()

            if not member:
                connection.close()
                messagebox.showerror(
                    "Not Found",
                    "Member not found."
                )
                return

            confirm = messagebox.askyesno(
                "Confirm Delete",
                "Are you sure you want to delete "
                + member[0] + "?"
            )

            if not confirm:
                connection.close()
                return

            cursor.execute("""
                DELETE FROM members
                WHERE member_id = ?
            """, (member_id,))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Member deleted successfully."
            )

            member_id_entry.delete(0, tk.END)

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        delete_window,
        text="Delete Member",
        width=25,
        command=delete_member
    ).pack(pady=20)

    tk.Button(
        delete_window,
        text="Back",
        width=25,
        command=delete_window.destroy
    ).pack()


def member_management():
    member_window = tk.Toplevel(window)
    member_window.title("Member Management")
    member_window.geometry("500x450")

    title = tk.Label(
        member_window,
        text="MEMBER MANAGEMENT",
        font=("Arial", 16, "bold")
    )
    title.pack(pady=20)

    tk.Button(
        member_window,
        text="Register Member",
        width=30,
        command=register_member_gui
    ).pack(pady=8)

    tk.Button(
        member_window,
        text="View Members",
        width=30,
        command=view_members_gui
    ).pack(pady=8)

    tk.Button(
        member_window,
        text="Search Member",
        width=30,
        command=search_member_gui
    ).pack(pady=8)

    tk.Button(
        member_window,
        text="Update Member",
        width=30,
        command=update_member_gui
    ).pack(pady=8)

    tk.Button(
        member_window,
        text="Delete Member",
        width=30,
        command=delete_member_gui
    ).pack(pady=8)

    tk.Button(
        member_window,
        text="Back",
        width=30,
        command=member_window.destroy
    ).pack(pady=8)


# =========================================================
# SAVINGS MANAGEMENT
# =========================================================

def deposit_gui():
    deposit_window = tk.Toplevel(window)
    deposit_window.title("Deposit Savings")
    deposit_window.geometry("500x400")

    tk.Label(
        deposit_window,
        text="DEPOSIT SAVINGS",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(deposit_window, text="Member ID").pack()
    member_id_entry = tk.Entry(deposit_window, width=30)
    member_id_entry.pack(pady=8)

    tk.Label(deposit_window, text="Deposit Amount").pack()
    amount_entry = tk.Entry(deposit_window, width=30)
    amount_entry.pack(pady=8)

    def make_deposit():
        member_id = member_id_entry.get().strip()
        amount_text = amount_entry.get().strip()

        if not member_id or not amount_text:
            messagebox.showerror(
                "Error",
                "All fields are required."
            )
            return

        try:
            amount = float(amount_text)

            if amount <= 0:
                messagebox.showerror(
                    "Error",
                    "Deposit amount must be greater than zero."
                )
                return

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid amount."
            )
            return

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT full_name
                FROM members
                WHERE member_id = ?
            """, (member_id,))

            member = cursor.fetchone()

            if not member:
                connection.close()
                messagebox.showerror(
                    "Not Found",
                    "Member not found."
                )
                return

            transaction_date = date.today().isoformat()

            cursor.execute("""
                INSERT INTO savings
                (
                    member_id,
                    transaction_type,
                    amount,
                    transaction_date
                )
                VALUES (?, ?, ?, ?)
            """, (
                member_id,
                "Deposit",
                amount,
                transaction_date
            ))

            cursor.execute("""
                INSERT INTO transactions
                (
                    member_id,
                    transaction_type,
                    amount,
                    transaction_date,
                    description
                )
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

            messagebox.showinfo(
                "Success",
                "Deposit recorded successfully."
            )

            member_id_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        deposit_window,
        text="Deposit",
        width=25,
        command=make_deposit
    ).pack(pady=20)

    tk.Button(
        deposit_window,
        text="Back",
        width=25,
        command=deposit_window.destroy
    ).pack()


def withdraw_gui():
    withdraw_window = tk.Toplevel(window)
    withdraw_window.title("Withdraw Savings")
    withdraw_window.geometry("500x400")

    tk.Label(
        withdraw_window,
        text="WITHDRAW SAVINGS",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(withdraw_window, text="Member ID").pack()
    member_id_entry = tk.Entry(withdraw_window, width=30)
    member_id_entry.pack(pady=8)

    tk.Label(withdraw_window, text="Withdrawal Amount").pack()
    amount_entry = tk.Entry(withdraw_window, width=30)
    amount_entry.pack(pady=8)

    def make_withdrawal():
        member_id = member_id_entry.get().strip()
        amount_text = amount_entry.get().strip()

        if not member_id or not amount_text:
            messagebox.showerror(
                "Error",
                "All fields are required."
            )
            return

        try:
            amount = float(amount_text)

            if amount <= 0:
                messagebox.showerror(
                    "Error",
                    "Withdrawal amount must be greater than zero."
                )
                return

        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid amount."
            )
            return

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT full_name
                FROM members
                WHERE member_id = ?
            """, (member_id,))

            member = cursor.fetchone()

            if not member:
                connection.close()
                messagebox.showerror(
                    "Not Found",
                    "Member not found."
                )
                return

            cursor.execute("""
                SELECT COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'Deposit'
                                THEN amount
                            WHEN transaction_type = 'Withdrawal'
                                THEN -amount
                            ELSE 0
                        END
                    ),
                    0
                )
                FROM savings
                WHERE member_id = ?
            """, (member_id,))

            balance = cursor.fetchone()[0]

            if amount > balance:
                connection.close()
                messagebox.showerror(
                    "Insufficient Funds",
                    "Withdrawal amount is greater than "
                    "the member's savings balance."
                )
                return

            transaction_date = date.today().isoformat()

            cursor.execute("""
                INSERT INTO savings
                (
                    member_id,
                    transaction_type,
                    amount,
                    transaction_date
                )
                VALUES (?, ?, ?, ?)
            """, (
                member_id,
                "Withdrawal",
                amount,
                transaction_date
            ))

            cursor.execute("""
                INSERT INTO transactions
                (
                    member_id,
                    transaction_type,
                    amount,
                    transaction_date,
                    description
                )
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

            new_balance = balance - amount

            messagebox.showinfo(
                "Success",
                "Withdrawal recorded successfully.\n\n"
                "Remaining Balance: " + str(new_balance)
            )

            member_id_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        withdraw_window,
        text="Withdraw",
        width=25,
        command=make_withdrawal
    ).pack(pady=20)

    tk.Button(
        withdraw_window,
        text="Back",
        width=25,
        command=withdraw_window.destroy
    ).pack()


def check_balance_gui():
    balance_window = tk.Toplevel(window)
    balance_window.title("Check Savings Balance")
    balance_window.geometry("500x400")

    tk.Label(
        balance_window,
        text="CHECK SAVINGS BALANCE",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(balance_window, text="Member ID").pack()

    member_id_entry = tk.Entry(
        balance_window,
        width=30
    )
    member_id_entry.pack(pady=10)

    result_label = tk.Label(
        balance_window,
        text="",
        font=("Arial", 12),
        justify="left"
    )
    result_label.pack(pady=20)

    def check_balance():
        member_id = member_id_entry.get().strip()

        if not member_id:
            messagebox.showerror(
                "Error",
                "Please enter a Member ID."
            )
            return

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT full_name
                FROM members
                WHERE member_id = ?
            """, (member_id,))

            member = cursor.fetchone()

            if not member:
                connection.close()
                messagebox.showerror(
                    "Not Found",
                    "Member not found."
                )
                return

            cursor.execute("""
                SELECT COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'Deposit'
                                THEN amount
                            WHEN transaction_type = 'Withdrawal'
                                THEN -amount
                            ELSE 0
                        END
                    ),
                    0
                )
                FROM savings
                WHERE member_id = ?
            """, (member_id,))

            balance = cursor.fetchone()[0]

            connection.close()

            result_label.config(
                text=
                "Member ID: " + member_id +
                "\nMember Name: " + member[0] +
                "\nSavings Balance: " + str(balance)
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        balance_window,
        text="Check Balance",
        width=25,
        command=check_balance
    ).pack(pady=10)

    tk.Button(
        balance_window,
        text="Back",
        width=25,
        command=balance_window.destroy
    ).pack(pady=10)


def savings_history_gui():
    history_window = tk.Toplevel(window)
    history_window.title("Savings History")
    history_window.geometry("700x450")

    tk.Label(
        history_window,
        text="SAVINGS HISTORY",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    search_frame = tk.Frame(history_window)
    search_frame.pack(pady=5)

    tk.Label(
        search_frame,
        text="Member ID:"
    ).pack(side="left", padx=5)

    member_id_entry = tk.Entry(
        search_frame,
        width=20
    )
    member_id_entry.pack(side="left", padx=5)

    columns = (
        "Savings ID",
        "Transaction Type",
        "Amount",
        "Date"
    )

    tree = ttk.Treeview(
        history_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=150)

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    def search_history():
        member_id = member_id_entry.get().strip()

        if not member_id:
            messagebox.showerror(
                "Error",
                "Please enter a Member ID."
            )
            return

        for item in tree.get_children():
            tree.delete(item)

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    savings_id,
                    transaction_type,
                    amount,
                    transaction_date
                FROM savings
                WHERE member_id = ?
                ORDER BY savings_id
            """, (member_id,))

            records = cursor.fetchall()
            connection.close()

            if not records:
                messagebox.showinfo(
                    "No Records",
                    "No savings records found for this member."
                )
                return

            for record in records:
                tree.insert(
                    "",
                    tk.END,
                    values=record
                )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        search_frame,
        text="Search",
        command=search_history
    ).pack(side="left", padx=5)

    tk.Button(
        history_window,
        text="Back",
        width=20,
        command=history_window.destroy
    ).pack(pady=10)


def total_savings_gui():
    total_window = tk.Toplevel(window)
    total_window.title("Total SACCO Savings")
    total_window.geometry("500x350")

    tk.Label(
        total_window,
        text="TOTAL SACCO SAVINGS",
        font=("Arial", 16, "bold")
    ).pack(pady=30)

    result_label = tk.Label(
        total_window,
        text="",
        font=("Arial", 14)
    )
    result_label.pack(pady=30)

    try:
        connection = sqlite3.connect("sacco.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COALESCE(
                SUM(
                    CASE
                        WHEN transaction_type = 'Deposit'
                            THEN amount
                        WHEN transaction_type = 'Withdrawal'
                            THEN -amount
                        ELSE 0
                    END
                ),
                0
            )
            FROM savings
        """)

        total = cursor.fetchone()[0]
        connection.close()

        result_label.config(
            text="Total SACCO Savings: " + str(total)
        )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            str(error)
        )

    tk.Button(
        total_window,
        text="Back",
        width=20,
        command=total_window.destroy
    ).pack(pady=20)


def savings_management():
    savings_window = tk.Toplevel(window)
    savings_window.title("Savings Management")
    savings_window.geometry("500x450")

    tk.Label(
        savings_window,
        text="SAVINGS MANAGEMENT",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Button(
        savings_window,
        text="Deposit Savings",
        width=30,
        command=deposit_gui
    ).pack(pady=8)

    tk.Button(
        savings_window,
        text="Withdraw Savings",
        width=30,
        command=withdraw_gui
    ).pack(pady=8)

    tk.Button(
        savings_window,
        text="Check Balance",
        width=30,
        command=check_balance_gui
    ).pack(pady=8)

    tk.Button(
        savings_window,
        text="Savings History",
        width=30,
        command=savings_history_gui
    ).pack(pady=8)

    tk.Button(
        savings_window,
        text="Total SACCO Savings",
        width=30,
        command=total_savings_gui
    ).pack(pady=8)

    tk.Button(
        savings_window,
        text="Back",
        width=30,
        command=savings_window.destroy
    ).pack(pady=8)


# =========================================================
# LOAN MANAGEMENT
# =========================================================

def apply_loan_gui():
    loan_window = tk.Toplevel(window)
    loan_window.title("Apply for Loan")
    loan_window.geometry("500x450")

    tk.Label(
        loan_window,
        text="APPLY FOR LOAN",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(loan_window, text="Member ID").pack()
    member_id_entry = tk.Entry(loan_window, width=30)
    member_id_entry.pack(pady=8)

    tk.Label(loan_window, text="Loan Amount").pack()
    amount_entry = tk.Entry(loan_window, width=30)
    amount_entry.pack(pady=8)

    def submit_application():
        member_id = member_id_entry.get().strip()
        amount_text = amount_entry.get().strip()

        if not member_id or not amount_text:
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                messagebox.showerror(
                    "Error",
                    "Loan amount must be greater than zero."
                )
                return
        except ValueError:
            messagebox.showerror(
                "Error",
                "Please enter a valid loan amount."
            )
            return

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT full_name
                FROM members
                WHERE member_id = ?
            """, (member_id,))

            member = cursor.fetchone()

            if not member:
                connection.close()
                messagebox.showerror("Not Found", "Member not found.")
                return

            application_date = date.today().isoformat()

            cursor.execute("""
                INSERT INTO loans
                (
                    member_id,
                    loan_amount,
                    application_date,
                    status
                )
                VALUES (?, ?, ?, ?)
            """, (
                member_id,
                amount,
                application_date,
                "Pending"
            ))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Loan application submitted successfully.\n\n"
                "Member: " + member[0] +
                "\nLoan Amount: " + str(amount) +
                "\nStatus: Pending"
            )

            member_id_entry.delete(0, tk.END)
            amount_entry.delete(0, tk.END)

        except sqlite3.Error as error:
            messagebox.showerror("Database Error", str(error))

    tk.Button(
        loan_window,
        text="Submit Application",
        width=25,
        command=submit_application
    ).pack(pady=20)

    tk.Button(
        loan_window,
        text="Back",
        width=25,
        command=loan_window.destroy
    ).pack()


# ---------------------------------------------------------
# STAGE 16 - VIEW LOANS
# ---------------------------------------------------------

def view_loans_gui():
    view_window = tk.Toplevel(window)
    view_window.title("View Loans")
    view_window.geometry("950x500")

    tk.Label(
        view_window,
        text="LOAN RECORDS",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    columns = (
        "Loan ID",
        "Member ID",
        "Member Name",
        "Loan Amount",
        "Application Date",
        "Status",
        "Approval Date"
    )

    tree = ttk.Treeview(
        view_window,
        columns=columns,
        show="headings"
    )

    widths = {
        "Loan ID": 70,
        "Member ID": 90,
        "Member Name": 160,
        "Loan Amount": 110,
        "Application Date": 120,
        "Status": 100,
        "Approval Date": 120
    }

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=widths[column])

    scrollbar = ttk.Scrollbar(
        view_window,
        orient="vertical",
        command=tree.yview
    )
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(10, 0),
        pady=10
    )

    scrollbar.pack(
        side="right",
        fill="y",
        pady=10,
        padx=(0, 10)
    )

    try:
        connection = sqlite3.connect("sacco.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                l.loan_id,
                l.member_id,
                m.full_name,
                l.loan_amount,
                l.application_date,
                l.status,
                COALESCE(l.approval_date, '')
            FROM loans l
            INNER JOIN members m
                ON l.member_id = m.member_id
            ORDER BY l.loan_id
        """)

        loans = cursor.fetchall()
        connection.close()

        for loan in loans:
            tree.insert("", tk.END, values=loan)

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            str(error)
        )

    tk.Button(
        view_window,
        text="Back",
        width=20,
        command=view_window.destroy
    ).pack(pady=10)


# ---------------------------------------------------------
# STAGE 17 - APPROVE / REJECT LOAN
# ---------------------------------------------------------

def approve_or_reject_loan_gui():
    decision_window = tk.Toplevel(window)
    decision_window.title("Approve / Reject Loan")
    decision_window.geometry("550x500")

    tk.Label(
        decision_window,
        text="APPROVE / REJECT LOAN",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        decision_window,
        text="Enter Loan ID"
    ).pack()

    loan_id_entry = tk.Entry(
        decision_window,
        width=30
    )
    loan_id_entry.pack(pady=8)

    details_label = tk.Label(
        decision_window,
        text="",
        font=("Arial", 11),
        justify="left"
    )
    details_label.pack(pady=15)

    def load_loan():
        loan_id_text = loan_id_entry.get().strip()

        if not loan_id_text:
            messagebox.showerror(
                "Error",
                "Please enter a Loan ID."
            )
            return

        try:
            loan_id = int(loan_id_text)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Loan ID must be a number."
            )
            return

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    l.loan_id,
                    l.member_id,
                    m.full_name,
                    l.loan_amount,
                    l.application_date,
                    l.status,
                    COALESCE(l.approval_date, '')
                FROM loans l
                INNER JOIN members m
                    ON l.member_id = m.member_id
                WHERE l.loan_id = ?
            """, (loan_id,))

            loan = cursor.fetchone()
            connection.close()

            if not loan:
                details_label.config(text="Loan not found.")
                return

            details_label.config(
                text=
                "Loan ID: " + str(loan[0]) +
                "\nMember ID: " + loan[1] +
                "\nMember Name: " + loan[2] +
                "\nLoan Amount: " + str(loan[3]) +
                "\nApplication Date: " + loan[4] +
                "\nStatus: " + loan[5] +
                "\nApproval Date: " + (loan[6] or "Not applicable")
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def approve_loan():
        change_loan_status("Approved")

    def reject_loan():
        change_loan_status("Rejected")

    def change_loan_status(new_status):
        loan_id_text = loan_id_entry.get().strip()

        if not loan_id_text:
            messagebox.showerror(
                "Error",
                "Please enter a Loan ID."
            )
            return

        try:
            loan_id = int(loan_id_text)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Loan ID must be a number."
            )
            return

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT status
                FROM loans
                WHERE loan_id = ?
            """, (loan_id,))

            loan = cursor.fetchone()

            if not loan:
                connection.close()
                messagebox.showerror(
                    "Not Found",
                    "Loan not found."
                )
                return

            current_status = loan[0]

            if current_status != "Pending":
                connection.close()
                messagebox.showerror(
                    "Cannot Change",
                    "Only pending loans can be approved or rejected."
                )
                return

            if new_status == "Approved":
                approval_date = date.today().isoformat()

                cursor.execute("""
                    UPDATE loans
                    SET status = ?,
                        approval_date = ?
                    WHERE loan_id = ?
                """, (
                    "Approved",
                    approval_date,
                    loan_id
                ))
            else:
                cursor.execute("""
                    UPDATE loans
                    SET status = ?,
                        approval_date = NULL
                    WHERE loan_id = ?
                """, (
                    "Rejected",
                    loan_id
                ))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Success",
                "Loan has been " + new_status.lower() + " successfully."
            )

            details_label.config(text="")
            loan_id_entry.delete(0, tk.END)

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        decision_window,
        text="Load Loan",
        width=25,
        command=load_loan
    ).pack(pady=8)

    tk.Button(
        decision_window,
        text="Approve Loan",
        width=25,
        command=approve_loan
    ).pack(pady=8)

    tk.Button(
        decision_window,
        text="Reject Loan",
        width=25,
        command=reject_loan
    ).pack(pady=8)

    tk.Button(
        decision_window,
        text="Back",
        width=25,
        command=decision_window.destroy
    ).pack(pady=8)


# ---------------------------------------------------------
# STAGE 18 - MAKE LOAN REPAYMENT
# ---------------------------------------------------------

def make_loan_repayment_gui():
    repayment_window = tk.Toplevel(window)
    repayment_window.title("Make Loan Repayment")
    repayment_window.geometry("550x550")

    tk.Label(
        repayment_window,
        text="MAKE LOAN REPAYMENT",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        repayment_window,
        text="Loan ID"
    ).pack()

    loan_id_entry = tk.Entry(
        repayment_window,
        width=30
    )
    loan_id_entry.pack(pady=8)

    tk.Label(
        repayment_window,
        text="Repayment Amount"
    ).pack()

    amount_entry = tk.Entry(
        repayment_window,
        width=30
    )
    amount_entry.pack(pady=8)

    details_label = tk.Label(
        repayment_window,
        text="",
        font=("Arial", 11),
        justify="left"
    )
    details_label.pack(pady=15)

    def load_loan():
        loan_id_text = loan_id_entry.get().strip()

        if not loan_id_text:
            messagebox.showerror(
                "Error",
                "Please enter a Loan ID."
            )
            return

        try:
            loan_id = int(loan_id_text)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Loan ID must be a number."
            )
            return

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    l.member_id,
                    m.full_name,
                    l.loan_amount,
                    l.status
                FROM loans l
                INNER JOIN members m
                    ON l.member_id = m.member_id
                WHERE l.loan_id = ?
            """, (loan_id,))

            loan = cursor.fetchone()

            if not loan:
                connection.close()
                messagebox.showerror(
                    "Not Found",
                    "Loan not found."
                )
                return

            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM loan_repayments
                WHERE loan_id = ?
            """, (loan_id,))

            repaid = cursor.fetchone()[0]
            balance = max(0, loan[2] - repaid)

            connection.close()

            details_label.config(
                text=
                "Member ID: " + loan[0] +
                "\nMember Name: " + loan[1] +
                "\nLoan Amount: " + str(loan[2]) +
                "\nStatus: " + loan[3] +
                "\nAmount Repaid: " + str(repaid) +
                "\nOutstanding Balance: " + str(balance)
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    def make_repayment():
        loan_id_text = loan_id_entry.get().strip()
        amount_text = amount_entry.get().strip()

        if not loan_id_text or not amount_text:
            messagebox.showerror(
                "Error",
                "Loan ID and repayment amount are required."
            )
            return

        try:
            loan_id = int(loan_id_text)
            amount = float(amount_text)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter a valid Loan ID and repayment amount."
            )
            return

        if amount <= 0:
            messagebox.showerror(
                "Error",
                "Repayment amount must be greater than zero."
            )
            return

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    member_id,
                    loan_amount,
                    status
                FROM loans
                WHERE loan_id = ?
            """, (loan_id,))

            loan = cursor.fetchone()

            if not loan:
                connection.close()
                messagebox.showerror(
                    "Not Found",
                    "Loan not found."
                )
                return

            member_id = loan[0]
            loan_amount = loan[1]
            status = loan[2]

            if status != "Approved":
                connection.close()
                messagebox.showerror(
                    "Cannot Repay",
                    "Repayments can only be made for approved loans."
                )
                return

            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM loan_repayments
                WHERE loan_id = ?
            """, (loan_id,))

            amount_repaid = cursor.fetchone()[0]
            outstanding = loan_amount - amount_repaid

            if outstanding <= 0:
                connection.close()
                messagebox.showinfo(
                    "Loan Cleared",
                    "This loan has already been fully repaid."
                )
                return

            if amount > outstanding:
                connection.close()
                messagebox.showerror(
                    "Invalid Amount",
                    "Repayment cannot be greater than the "
                    "outstanding loan balance.\n\n"
                    "Outstanding Balance: " + str(outstanding)
                )
                return

            repayment_date = date.today().isoformat()

            cursor.execute("""
                INSERT INTO loan_repayments
                (
                    loan_id,
                    amount,
                    repayment_date
                )
                VALUES (?, ?, ?)
            """, (
                loan_id,
                amount,
                repayment_date
            ))

            cursor.execute("""
                INSERT INTO transactions
                (
                    member_id,
                    transaction_type,
                    amount,
                    transaction_date,
                    description
                )
                VALUES (?, ?, ?, ?, ?)
            """, (
                member_id,
                "Loan Repayment",
                amount,
                repayment_date,
                "Loan repayment for Loan ID " + str(loan_id)
            ))

            connection.commit()
            connection.close()

            new_balance = outstanding - amount

            messagebox.showinfo(
                "Success",
                "Loan repayment recorded successfully.\n\n"
                "Amount Paid: " + str(amount) +
                "\nRemaining Balance: " + str(new_balance)
            )

            amount_entry.delete(0, tk.END)
            load_loan()

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        repayment_window,
        text="Load Loan",
        width=25,
        command=load_loan
    ).pack(pady=8)

    tk.Button(
        repayment_window,
        text="Make Repayment",
        width=25,
        command=make_repayment
    ).pack(pady=8)

    tk.Button(
        repayment_window,
        text="Back",
        width=25,
        command=repayment_window.destroy
    ).pack(pady=8)


# ---------------------------------------------------------
# STAGE 19 - CHECK LOAN BALANCE
# ---------------------------------------------------------

def check_loan_balance_gui():
    balance_window = tk.Toplevel(window)
    balance_window.title("Check Loan Balance")
    balance_window.geometry("550x450")

    tk.Label(
        balance_window,
        text="CHECK LOAN BALANCE",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Label(
        balance_window,
        text="Loan ID"
    ).pack()

    loan_id_entry = tk.Entry(
        balance_window,
        width=30
    )
    loan_id_entry.pack(pady=10)

    result_label = tk.Label(
        balance_window,
        text="",
        font=("Arial", 12),
        justify="left"
    )
    result_label.pack(pady=25)

    def check_balance():
        loan_id_text = loan_id_entry.get().strip()

        if not loan_id_text:
            messagebox.showerror(
                "Error",
                "Please enter a Loan ID."
            )
            return

        try:
            loan_id = int(loan_id_text)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Loan ID must be a number."
            )
            return

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    l.member_id,
                    m.full_name,
                    l.loan_amount,
                    l.status
                FROM loans l
                INNER JOIN members m
                    ON l.member_id = m.member_id
                WHERE l.loan_id = ?
            """, (loan_id,))

            loan = cursor.fetchone()

            if not loan:
                connection.close()
                messagebox.showerror(
                    "Not Found",
                    "Loan not found."
                )
                return

            cursor.execute("""
                SELECT COALESCE(SUM(amount), 0)
                FROM loan_repayments
                WHERE loan_id = ?
            """, (loan_id,))

            repaid = cursor.fetchone()[0]
            connection.close()

            if loan[3] == "Approved":
                outstanding = max(0, loan[2] - repaid)
            else:
                outstanding = 0

            result_label.config(
                text=
                "Loan ID: " + str(loan_id) +
                "\nMember ID: " + loan[0] +
                "\nMember Name: " + loan[1] +
                "\nLoan Amount: " + str(loan[2]) +
                "\nStatus: " + loan[3] +
                "\nAmount Repaid: " + str(repaid) +
                "\nOutstanding Balance: " + str(outstanding)
            )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        balance_window,
        text="Check Balance",
        width=25,
        command=check_balance
    ).pack(pady=10)

    tk.Button(
        balance_window,
        text="Back",
        width=25,
        command=balance_window.destroy
    ).pack(pady=10)


# ---------------------------------------------------------
# STAGE 20 - REPAYMENT HISTORY
# ---------------------------------------------------------

def repayment_history_gui():
    history_window = tk.Toplevel(window)
    history_window.title("Repayment History")
    history_window.geometry("800x500")

    tk.Label(
        history_window,
        text="LOAN REPAYMENT HISTORY",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    search_frame = tk.Frame(history_window)
    search_frame.pack(pady=5)

    tk.Label(
        search_frame,
        text="Loan ID:"
    ).pack(side="left", padx=5)

    loan_id_entry = tk.Entry(
        search_frame,
        width=20
    )
    loan_id_entry.pack(side="left", padx=5)

    columns = (
        "Repayment ID",
        "Loan ID",
        "Member ID",
        "Member Name",
        "Amount",
        "Repayment Date"
    )

    tree = ttk.Treeview(
        history_window,
        columns=columns,
        show="headings"
    )

    widths = {
        "Repayment ID": 100,
        "Loan ID": 80,
        "Member ID": 90,
        "Member Name": 150,
        "Amount": 100,
        "Repayment Date": 130
    }

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=widths[column])

    scrollbar = ttk.Scrollbar(
        history_window,
        orient="vertical",
        command=tree.yview
    )
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(10, 0),
        pady=10
    )

    scrollbar.pack(
        side="right",
        fill="y",
        pady=10,
        padx=(0, 10)
    )

    def search_history():
        loan_id_text = loan_id_entry.get().strip()

        if not loan_id_text:
            messagebox.showerror(
                "Error",
                "Please enter a Loan ID."
            )
            return

        try:
            loan_id = int(loan_id_text)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Loan ID must be a number."
            )
            return

        for item in tree.get_children():
            tree.delete(item)

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT
                    r.repayment_id,
                    r.loan_id,
                    l.member_id,
                    m.full_name,
                    r.amount,
                    r.repayment_date
                FROM loan_repayments r
                INNER JOIN loans l
                    ON r.loan_id = l.loan_id
                INNER JOIN members m
                    ON l.member_id = m.member_id
                WHERE r.loan_id = ?
                ORDER BY r.repayment_id
            """, (loan_id,))

            records = cursor.fetchall()
            connection.close()

            if not records:
                messagebox.showinfo(
                    "No Records",
                    "No repayment records found for this loan."
                )
                return

            for record in records:
                tree.insert(
                    "",
                    tk.END,
                    values=record
                )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        search_frame,
        text="Search",
        command=search_history
    ).pack(side="left", padx=5)

    tk.Button(
        history_window,
        text="Back",
        width=20,
        command=history_window.destroy
    ).pack(pady=10)


def loan_management():
    loan_menu_window = tk.Toplevel(window)
    loan_menu_window.title("Loan Management")
    loan_menu_window.geometry("500x500")

    tk.Label(
        loan_menu_window,
        text="LOAN MANAGEMENT",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Button(
        loan_menu_window,
        text="Apply for Loan",
        width=30,
        command=apply_loan_gui
    ).pack(pady=8)

    tk.Button(
        loan_menu_window,
        text="View Loans",
        width=30,
        command=view_loans_gui
    ).pack(pady=8)

    tk.Button(
        loan_menu_window,
        text="Approve / Reject Loan",
        width=30,
        command=approve_or_reject_loan_gui
    ).pack(pady=8)

    tk.Button(
        loan_menu_window,
        text="Make Loan Repayment",
        width=30,
        command=make_loan_repayment_gui
    ).pack(pady=8)

    tk.Button(
        loan_menu_window,
        text="Check Loan Balance",
        width=30,
        command=check_loan_balance_gui
    ).pack(pady=8)

    tk.Button(
        loan_menu_window,
        text="Repayment History",
        width=30,
        command=repayment_history_gui
    ).pack(pady=8)

    tk.Button(
        loan_menu_window,
        text="Back",
        width=30,
        command=loan_menu_window.destroy
    ).pack(pady=8)


# =========================================================
# REPORTS
# =========================================================

def member_list_report_gui():
    report_window = tk.Toplevel(window)
    report_window.title("Member List Report")
    report_window.geometry("800x500")

    tk.Label(
        report_window,
        text="MEMBER LIST REPORT",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    columns = (
        "Member ID",
        "Full Name",
        "Phone",
        "Email",
        "Registration Date"
    )

    tree = ttk.Treeview(
        report_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=150)

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    try:
        connection = sqlite3.connect("sacco.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                member_id,
                full_name,
                phone,
                email,
                registration_date
            FROM members
            ORDER BY member_id
        """)

        records = cursor.fetchall()
        connection.close()

        for record in records:
            tree.insert("", tk.END, values=record)

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            str(error)
        )

    tk.Button(
        report_window,
        text="Back",
        width=20,
        command=report_window.destroy
    ).pack(pady=10)


def individual_financial_statement_gui():
    report_window = tk.Toplevel(window)
    report_window.title("Individual Financial Statement")
    report_window.geometry("700x600")

    tk.Label(
        report_window,
        text="INDIVIDUAL FINANCIAL STATEMENT",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    search_frame = tk.Frame(report_window)
    search_frame.pack(pady=5)

    tk.Label(
        search_frame,
        text="Member ID:"
    ).pack(side="left", padx=5)

    member_id_entry = tk.Entry(
        search_frame,
        width=20
    )
    member_id_entry.pack(side="left", padx=5)

    output = tk.Text(
        report_window,
        width=75,
        height=25
    )
    output.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    def generate_statement():
        member_id = member_id_entry.get().strip()

        if not member_id:
            messagebox.showerror(
                "Error",
                "Please enter a Member ID."
            )
            return

        try:
            connection = sqlite3.connect("sacco.db")
            cursor = connection.cursor()

            cursor.execute("""
                SELECT full_name, phone, email
                FROM members
                WHERE member_id = ?
            """, (member_id,))

            member = cursor.fetchone()

            if not member:
                connection.close()
                messagebox.showerror(
                    "Not Found",
                    "Member not found."
                )
                return

            cursor.execute("""
                SELECT COALESCE(
                    SUM(
                        CASE
                            WHEN transaction_type = 'Deposit'
                                THEN amount
                            WHEN transaction_type = 'Withdrawal'
                                THEN -amount
                            ELSE 0
                        END
                    ),
                    0
                )
                FROM savings
                WHERE member_id = ?
            """, (member_id,))

            savings_balance = cursor.fetchone()[0]

            cursor.execute("""
                SELECT
                    COALESCE(SUM(loan_amount), 0)
                FROM loans
                WHERE member_id = ?
                AND status = 'Approved'
            """, (member_id,))

            approved_loans = cursor.fetchone()[0]

            cursor.execute("""
                SELECT
                    COALESCE(SUM(r.amount), 0)
                FROM loan_repayments r
                INNER JOIN loans l
                    ON r.loan_id = l.loan_id
                WHERE l.member_id = ?
                AND l.status = 'Approved'
            """, (member_id,))

            total_repaid = cursor.fetchone()[0]

            outstanding = max(
                0,
                approved_loans - total_repaid
            )

            cursor.execute("""
                SELECT
                    l.loan_id,
                    l.loan_amount,
                    l.application_date,
                    l.status,
                    COALESCE(l.approval_date, ''),
                    COALESCE(
                        (
                            SELECT SUM(r.amount)
                            FROM loan_repayments r
                            WHERE r.loan_id = l.loan_id
                        ),
                        0
                    )
                FROM loans l
                WHERE l.member_id = ?
                ORDER BY l.loan_id
            """, (member_id,))

            loans = cursor.fetchall()

            cursor.execute("""
                SELECT
                    transaction_type,
                    amount,
                    transaction_date,
                    description
                FROM transactions
                WHERE member_id = ?
                ORDER BY transaction_id
            """, (member_id,))

            transactions = cursor.fetchall()

            connection.close()

            output.delete("1.0", tk.END)

            output.insert(
                tk.END,
                "INDIVIDUAL FINANCIAL STATEMENT\n"
            )
            output.insert(
                tk.END,
                "========================================\n\n"
            )

            output.insert(
                tk.END,
                "Member ID: " + member_id +
                "\nName: " + member[0] +
                "\nPhone: " + member[1] +
                "\nEmail: " + member[2] +
                "\n\n"
            )

            output.insert(
                tk.END,
                "SAVINGS\n"
            )
            output.insert(
                tk.END,
                "----------------------------------------\n"
            )
            output.insert(
                tk.END,
                "Savings Balance: " +
                str(savings_balance) +
                "\n\n"
            )

            output.insert(
                tk.END,
                "LOANS\n"
            )
            output.insert(
                tk.END,
                "----------------------------------------\n"
            )
            output.insert(
                tk.END,
                "Approved Loans: " +
                str(approved_loans) +
                "\n"
            )
            output.insert(
                tk.END,
                "Total Repaid: " +
                str(total_repaid) +
                "\n"
            )
            output.insert(
                tk.END,
                "Outstanding Loans: " +
                str(outstanding) +
                "\n\n"
            )

            output.insert(
                tk.END,
                "LOAN DETAILS\n"
            )
            output.insert(
                tk.END,
                "----------------------------------------\n"
            )

            if loans:
                for loan in loans:
                    loan_id = loan[0]
                    loan_amount = loan[1]
                    application_date = loan[2]
                    status = loan[3]
                    approval_date = loan[4]
                    repaid = loan[5]

                    if status == "Approved":
                        loan_balance = max(
                            0,
                            loan_amount - repaid
                        )
                    else:
                        loan_balance = 0

                    output.insert(
                        tk.END,
                        "Loan ID: " + str(loan_id) +
                        "\nAmount: " + str(loan_amount) +
                        "\nApplication Date: " +
                        application_date +
                        "\nStatus: " + status +
                        "\nApproval Date: " +
                        (approval_date or "N/A") +
                        "\nAmount Repaid: " +
                        str(repaid) +
                        "\nOutstanding: " +
                        str(loan_balance) +
                        "\n\n"
                    )
            else:
                output.insert(
                    tk.END,
                    "No loans recorded.\n\n"
                )

            output.insert(
                tk.END,
                "TRANSACTIONS\n"
            )
            output.insert(
                tk.END,
                "----------------------------------------\n"
            )

            if transactions:
                for transaction in transactions:
                    output.insert(
                        tk.END,
                        transaction[2] +
                        " | " +
                        transaction[0] +
                        " | " +
                        str(transaction[1]) +
                        " | " +
                        (transaction[3] or "") +
                        "\n"
                    )
            else:
                output.insert(
                    tk.END,
                    "No transactions recorded.\n"
                )

        except sqlite3.Error as error:
            messagebox.showerror(
                "Database Error",
                str(error)
            )

    tk.Button(
        search_frame,
        text="Generate Statement",
        command=generate_statement
    ).pack(side="left", padx=5)

    tk.Button(
        report_window,
        text="Back",
        width=20,
        command=report_window.destroy
    ).pack(pady=10)


def total_savings_report_gui():
    report_window = tk.Toplevel(window)
    report_window.title("Total Savings Report")
    report_window.geometry("500x350")

    tk.Label(
        report_window,
        text="TOTAL SAVINGS REPORT",
        font=("Arial", 16, "bold")
    ).pack(pady=30)

    result_label = tk.Label(
        report_window,
        text="",
        font=("Arial", 14)
    )
    result_label.pack(pady=30)

    try:
        connection = sqlite3.connect("sacco.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT COALESCE(
                SUM(
                    CASE
                        WHEN transaction_type = 'Deposit'
                            THEN amount
                        WHEN transaction_type = 'Withdrawal'
                            THEN -amount
                        ELSE 0
                    END
                ),
                0
            )
            FROM savings
        """)

        total = cursor.fetchone()[0]
        connection.close()

        result_label.config(
            text="Total SACCO Savings: " + str(total)
        )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            str(error)
        )

    tk.Button(
        report_window,
        text="Back",
        width=20,
        command=report_window.destroy
    ).pack(pady=20)


def total_loans_issued_report_gui():
    report_window = tk.Toplevel(window)
    report_window.title("Total Loans Issued Report")
    report_window.geometry("600x400")

    tk.Label(
        report_window,
        text="TOTAL LOANS ISSUED",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    columns = (
        "Loan ID",
        "Member ID",
        "Member Name",
        "Amount",
        "Date"
    )

    tree = ttk.Treeview(
        report_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=110)

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    try:
        connection = sqlite3.connect("sacco.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                l.loan_id,
                l.member_id,
                m.full_name,
                l.loan_amount,
                l.approval_date
            FROM loans l
            INNER JOIN members m
                ON l.member_id = m.member_id
            WHERE l.status = 'Approved'
            ORDER BY l.loan_id
        """)

        records = cursor.fetchall()
        connection.close()

        for record in records:
            tree.insert("", tk.END, values=record)

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            str(error)
        )

    tk.Button(
        report_window,
        text="Back",
        width=20,
        command=report_window.destroy
    ).pack(pady=10)


def outstanding_loans_report_gui():
    report_window = tk.Toplevel(window)
    report_window.title("Outstanding Loans Report")
    report_window.geometry("800x500")

    tk.Label(
        report_window,
        text="OUTSTANDING LOANS REPORT",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    columns = (
        "Loan ID",
        "Member ID",
        "Member Name",
        "Loan Amount",
        "Amount Repaid",
        "Outstanding"
    )

    tree = ttk.Treeview(
        report_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=125)

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    try:
        connection = sqlite3.connect("sacco.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                l.loan_id,
                l.member_id,
                m.full_name,
                l.loan_amount,
                COALESCE(
                    (
                        SELECT SUM(r.amount)
                        FROM loan_repayments r
                        WHERE r.loan_id = l.loan_id
                    ),
                    0
                )
            FROM loans l
            INNER JOIN members m
                ON l.member_id = m.member_id
            WHERE l.status = 'Approved'
            ORDER BY l.loan_id
        """)

        records = cursor.fetchall()
        connection.close()

        for record in records:
            loan_id = record[0]
            member_id = record[1]
            member_name = record[2]
            loan_amount = record[3]
            amount_repaid = record[4]
            outstanding = max(
                0,
                loan_amount - amount_repaid
            )

            if outstanding > 0:
                tree.insert(
                    "",
                    tk.END,
                    values=(
                        loan_id,
                        member_id,
                        member_name,
                        loan_amount,
                        amount_repaid,
                        outstanding
                    )
                )

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            str(error)
        )

    tk.Button(
        report_window,
        text="Back",
        width=20,
        command=report_window.destroy
    ).pack(pady=10)


def loan_repayment_report_gui():
    report_window = tk.Toplevel(window)
    report_window.title("Loan Repayment Report")
    report_window.geometry("800x500")

    tk.Label(
        report_window,
        text="LOAN REPAYMENT REPORT",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    columns = (
        "Repayment ID",
        "Loan ID",
        "Member ID",
        "Member Name",
        "Amount",
        "Date"
    )

    tree = ttk.Treeview(
        report_window,
        columns=columns,
        show="headings"
    )

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=125)

    tree.pack(
        fill="both",
        expand=True,
        padx=10,
        pady=10
    )

    try:
        connection = sqlite3.connect("sacco.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                r.repayment_id,
                r.loan_id,
                l.member_id,
                m.full_name,
                r.amount,
                r.repayment_date
            FROM loan_repayments r
            INNER JOIN loans l
                ON r.loan_id = l.loan_id
            INNER JOIN members m
                ON l.member_id = m.member_id
            ORDER BY r.repayment_id
        """)

        records = cursor.fetchall()
        connection.close()

        for record in records:
            tree.insert("", tk.END, values=record)

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            str(error)
        )

    tk.Button(
        report_window,
        text="Back",
        width=20,
        command=report_window.destroy
    ).pack(pady=10)


def transaction_report_gui():
    report_window = tk.Toplevel(window)
    report_window.title("Transaction Report")
    report_window.geometry("950x500")

    tk.Label(
        report_window,
        text="TRANSACTION REPORT",
        font=("Arial", 16, "bold")
    ).pack(pady=15)

    columns = (
        "Transaction ID",
        "Member ID",
        "Member Name",
        "Transaction Type",
        "Amount",
        "Date",
        "Description"
    )

    tree = ttk.Treeview(
        report_window,
        columns=columns,
        show="headings"
    )

    widths = {
        "Transaction ID": 100,
        "Member ID": 90,
        "Member Name": 150,
        "Transaction Type": 130,
        "Amount": 100,
        "Date": 120,
        "Description": 180
    }

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=widths[column])

    scrollbar = ttk.Scrollbar(
        report_window,
        orient="vertical",
        command=tree.yview
    )
    tree.configure(yscrollcommand=scrollbar.set)

    tree.pack(
        side="left",
        fill="both",
        expand=True,
        padx=(10, 0),
        pady=10
    )

    scrollbar.pack(
        side="right",
        fill="y",
        pady=10,
        padx=(0, 10)
    )

    try:
        connection = sqlite3.connect("sacco.db")
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                t.transaction_id,
                t.member_id,
                m.full_name,
                t.transaction_type,
                t.amount,
                t.transaction_date,
                COALESCE(t.description, '')
            FROM transactions t
            INNER JOIN members m
                ON t.member_id = m.member_id
            ORDER BY t.transaction_id
        """)

        records = cursor.fetchall()
        connection.close()

        for record in records:
            tree.insert("", tk.END, values=record)

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            str(error)
        )

    tk.Button(
        report_window,
        text="Back",
        width=20,
        command=report_window.destroy
    ).pack(pady=10)


def reports_management():
    reports_window = tk.Toplevel(window)
    reports_window.title("Reports")
    reports_window.geometry("550x650")

    tk.Label(
        reports_window,
        text="REPORTS",
        font=("Arial", 16, "bold")
    ).pack(pady=20)

    tk.Button(
        reports_window,
        text="Member List Report",
        width=35,
        command=member_list_report_gui
    ).pack(pady=8)

    tk.Button(
        reports_window,
        text="Individual Financial Statement",
        width=35,
        command=individual_financial_statement_gui
    ).pack(pady=8)

    tk.Button(
        reports_window,
        text="Total Savings Report",
        width=35,
        command=total_savings_report_gui
    ).pack(pady=8)

    tk.Button(
        reports_window,
        text="Total Loans Issued Report",
        width=35,
        command=total_loans_issued_report_gui
    ).pack(pady=8)

    tk.Button(
        reports_window,
        text="Outstanding Loans Report",
        width=35,
        command=outstanding_loans_report_gui
    ).pack(pady=8)

    tk.Button(
        reports_window,
        text="Loan Repayment Report",
        width=35,
        command=loan_repayment_report_gui
    ).pack(pady=8)

    tk.Button(
        reports_window,
        text="Transaction Report",
        width=35,
        command=transaction_report_gui
    ).pack(pady=8)

    tk.Button(
        reports_window,
        text="Back",
        width=35,
        command=reports_window.destroy
    ).pack(pady=8)


# =========================================================
# LOGIN AND MAIN WINDOW
# =========================================================

# ---------------------------------------------------------
# APPLICATION SETTINGS
# ---------------------------------------------------------
APP_BG = "#f4f6f8"
PRIMARY = "#1f4e78"
PRIMARY_DARK = "#173a5a"
ACCENT = "#dbeafe"
TEXT = "#1f2937"
MUTED = "#6b7280"
WHITE = "white"
DANGER_BG = "#f8d7da"
DANGER_TEXT = "#842029"

# Demo login credentials for the course project.
# Change these values if you want different credentials.
LOGIN_USERNAME = "admin"
LOGIN_PASSWORD = "admin123"


def configure_application_style(root):
    """Apply consistent styling to the application."""
    root.configure(bg=APP_BG)
    root.option_add("*Font", ("Arial", 10))
    root.option_add("*Button.Font", ("Arial", 10, "bold"))
    root.option_add("*Button.Relief", "raised")
    root.option_add("*Button.BorderWidth", 1)
    root.option_add("*Button.Padx", 10)
    root.option_add("*Button.Pady", 6)
    root.option_add("*Entry.Font", ("Arial", 10))
    root.option_add("*Label.Font", ("Arial", 10))

    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure(
        "Treeview",
        font=("Arial", 10),
        rowheight=28
    )
    style.configure(
        "Treeview.Heading",
        font=("Arial", 10, "bold")
    )


def show_main_window():
    """Close the login screen and open the main SACCO system."""
    global window

    login_window.destroy()

    window = tk.Tk()
    window.title("SACCO Financial Management System")
    window.geometry("650x600")
    window.resizable(False, False)
    configure_application_style(window)

    # -----------------------------------------------------
    # MAIN HEADER
    # -----------------------------------------------------
    header_frame = tk.Frame(window, bg=PRIMARY, height=135)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    tk.Label(
        header_frame,
        text="SACCO FINANCIAL MANAGEMENT SYSTEM",
        font=("Arial", 20, "bold"),
        bg=PRIMARY,
        fg=WHITE
    ).pack(pady=(28, 4))

    tk.Label(
        header_frame,
        text="Member • Savings • Loans • Reports",
        font=("Arial", 11),
        bg=PRIMARY,
        fg=WHITE
    ).pack()

    # -----------------------------------------------------
    # MAIN MENU
    # -----------------------------------------------------
    menu_frame = tk.Frame(window, bg=APP_BG)
    menu_frame.pack(fill="both", expand=True, pady=20)

    tk.Label(
        menu_frame,
        text="MAIN MENU",
        font=("Arial", 14, "bold"),
        bg=APP_BG,
        fg=PRIMARY
    ).pack(pady=(0, 12))

    def create_main_button(text, command):
        button = tk.Button(
            menu_frame,
            text=text,
            width=32,
            command=command,
            font=("Arial", 11, "bold"),
            bg=WHITE,
            fg=TEXT,
            activebackground=ACCENT,
            activeforeground=TEXT,
            cursor="hand2"
        )
        button.pack(pady=6)
        return button

    create_main_button("Member Management", member_management)
    create_main_button("Savings Management", savings_management)
    create_main_button("Loan Management", loan_management)
    create_main_button("Reports", reports_management)

    exit_button = tk.Button(
        menu_frame,
        text="Exit",
        width=32,
        command=window.destroy,
        font=("Arial", 11, "bold"),
        bg=DANGER_BG,
        fg=DANGER_TEXT,
        activebackground="#f1b0b7",
        activeforeground="#58151c",
        cursor="hand2"
    )
    exit_button.pack(pady=(12, 6))

    tk.Label(
        window,
        text="Logged in as: Administrator  |  SQLite Database",
        font=("Arial", 9),
        bg=APP_BG,
        fg=MUTED
    ).pack(pady=(0, 10))

    window.protocol("WM_DELETE_WINDOW", window.destroy)
    window.mainloop()


def attempt_login():
    """Validate the username and password entered on the login screen."""
    username = username_entry.get().strip()
    password = password_entry.get()

    if not username or not password:
        messagebox.showwarning(
            "Login Required",
            "Please enter both username and password.",
            parent=login_window
        )
        return

    if username == LOGIN_USERNAME and password == LOGIN_PASSWORD:
        show_main_window()
    else:
        messagebox.showerror(
            "Login Failed",
            "Invalid username or password. Please try again.",
            parent=login_window
        )
        password_entry.delete(0, tk.END)
        password_entry.focus_set()


def toggle_password():
    """Show or hide the password characters."""
    if show_password_var.get():
        password_entry.config(show="")
    else:
        password_entry.config(show="*")


# =========================================================
# LOGIN WINDOW
# =========================================================

login_window = tk.Tk()
login_window.title("SACCO Financial Management System - Login")
login_window.geometry("560x500")
login_window.resizable(True, True)
configure_application_style(login_window)

# ---------------------------------------------------------
# LOGIN HEADER
# ---------------------------------------------------------
login_header = tk.Frame(login_window, bg=PRIMARY, height=155)
login_header.pack(fill="x")
login_header.pack_propagate(False)

tk.Label(
    login_header,
    text="SACCO",
    font=("Arial", 28, "bold"),
    bg=PRIMARY,
    fg=WHITE
).pack(pady=(25, 0))

tk.Label(
    login_header,
    text="FINANCIAL MANAGEMENT SYSTEM",
    font=("Arial", 14, "bold"),
    bg=PRIMARY,
    fg=WHITE
).pack(pady=(3, 4))

tk.Label(
    login_header,
    text="Secure Administrator Login",
    font=("Arial", 10),
    bg=PRIMARY,
    fg=WHITE
).pack()

# ---------------------------------------------------------
# LOGIN FORM
# ---------------------------------------------------------
login_card = tk.Frame(
    login_window,
    bg=WHITE,
    bd=1,
    relief="solid",
    padx=35,
    pady=22
)
login_card.pack(pady=25)

# Username
username_label = tk.Label(
    login_card,
    text="Username",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEXT
)
username_label.pack(anchor="w")

username_entry = tk.Entry(
    login_card,
    width=36,
    font=("Arial", 11),
    relief="solid",
    bd=1
)
username_entry.pack(pady=(6, 15), ipady=5)

# Password
password_label = tk.Label(
    login_card,
    text="Password",
    font=("Arial", 10, "bold"),
    bg=WHITE,
    fg=TEXT
)
password_label.pack(anchor="w")

password_entry = tk.Entry(
    login_card,
    width=36,
    font=("Arial", 11),
    relief="solid",
    bd=1,
    show="*"
)
password_entry.pack(pady=(6, 5), ipady=5)

show_password_var = tk.BooleanVar(value=False)

show_password_check = tk.Checkbutton(
    login_card,
    text="Show password",
    variable=show_password_var,
    command=toggle_password,
    bg=WHITE,
    fg=MUTED,
    activebackground=WHITE,
    activeforeground=TEXT,
    selectcolor=WHITE
)
show_password_check.pack(anchor="w")

login_button = tk.Button(
    login_card,
    text="LOGIN",
    width=28,
    command=attempt_login,
    font=("Arial", 11, "bold"),
    bg=PRIMARY,
    fg=WHITE,
    activebackground=PRIMARY_DARK,
    activeforeground=WHITE,
    cursor="hand2"
)
login_button.pack(pady=(18, 8))

exit_login_button = tk.Button(
    login_card,
    text="EXIT",
    width=28,
    command=login_window.destroy,
    font=("Arial", 10, "bold"),
    bg=DANGER_BG,
    fg=DANGER_TEXT,
    activebackground="#f1b0b7",
    activeforeground="#58151c",
    cursor="hand2"
)
exit_login_button.pack(pady=4)

# ---------------------------------------------------------
# LOGIN FOOTER
# ---------------------------------------------------------
tk.Label(
    login_window,
    text="Authorized users only | SQLite database system",
    font=("Arial", 9),
    bg=APP_BG,
    fg=MUTED
).pack(pady=(0, 12))

# Pressing Enter logs in.
login_window.bind("<Return>", lambda event: attempt_login())
username_entry.focus_set()

login_window.mainloop()

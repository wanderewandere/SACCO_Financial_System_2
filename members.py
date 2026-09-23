import sqlite3
from datetime import date


def register_member():
    member_id = input("Enter Member ID: ").strip()
    full_name = input("Enter Full Name: ").strip()
    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email Address: ").strip()

    registration_date = date.today().isoformat()

    if not member_id or not full_name or not phone or not email:
        print("All fields are required.")
        return

    try:
        connection = sqlite3.connect("sacco.db")
        cursor = connection.cursor()

        cursor.execute("""
            INSERT INTO members (member_id, full_name, phone, email, registration_date)
            VALUES (?, ?, ?, ?, ?)
        """, (member_id, full_name, phone, email, registration_date))

        connection.commit()

        print("Member registered successfully.")

    except sqlite3.IntegrityError:
        print("Member ID already exists.")

    finally:
        connection.close()


def view_members():
    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM members")
    members = cursor.fetchall()

    connection.close()

    if not members:
        print("No members registered.")
        return

    print("\n========== REGISTERED MEMBERS ==========")

    for member in members:
        print("Member ID:", member[0])
        print("Full Name:", member[1])
        print("Phone:", member[2])
        print("Email:", member[3])
        print("Registration Date:", member[4])
        print("----------------------------------------")

def search_member():
    member_id = input("Enter Member ID to search: ").strip()

    connection = sqlite3.connect("sacco.db")
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM members WHERE member_id = ?",
        (member_id,)
    )

    member = cursor.fetchone()

    connection.close()

    if member:
        print("\n========== MEMBER FOUND ==========")
        print("Member ID:", member[0])
        print("Full Name:", member[1])
        print("Phone:", member[2])
        print("Email:", member[3])
        print("Registration Date:", member[4])
    else:
        print("Member not found.")

def update_member():
    member_id = input("Enter Member ID to update: ").strip()

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

    print("\nEnter the new details.")

    full_name = input("Enter Full Name: ").strip()
    phone = input("Enter Phone Number: ").strip()
    email = input("Enter Email Address: ").strip()

    if not full_name or not phone or not email:
        print("All fields are required.")
        connection.close()
        return

    cursor.execute("""
        UPDATE members
        SET full_name = ?, phone = ?, email = ?
        WHERE member_id = ?
    """, (full_name, phone, email, member_id))

    connection.commit()
    connection.close()

    print("Member updated successfully.")

def delete_member():
    member_id = input("Enter Member ID to delete: ").strip()

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

    confirmation = input(
        "Are you sure you want to delete this member? (yes/no): "
    ).strip().lower()

    if confirmation != "yes":
        print("Deletion cancelled.")
        connection.close()
        return

    cursor.execute(
        "DELETE FROM members WHERE member_id = ?",
        (member_id,)
    )

    connection.commit()
    connection.close()

    print("Member deleted successfully.")



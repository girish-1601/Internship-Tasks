import colorama
from colorama import Fore, Style
import sqlite3 as sql

# Initialize colorama to enable colored output in the terminal
colorama.init()

# Function to create the attendance table in the database
def create_table():
    conn = sql.connect("attendance.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS attable (
                   subid INTEGER PRIMARY KEY,
                   subject TEXT,
                   attended INTEGER,
                   bunked INTEGER
                   )''')
    conn.commit()
    conn.close()

# Function to add subjects to the attendance table
def add_subjects():
    # Input subject names from the user
    subjects = input(Fore.LIGHTBLUE_EX + "Enter subject names separated by comma(s): ")
    subjects_list = subjects.split(',')
    conn = sql.connect("attendance.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM attable")  # Clear the existing records from the table
    for index, subject in enumerate(subjects_list, 1):
        # Insert subjects into the table with default attendance values
        cur.execute("INSERT INTO attable (subid, subject, attended, bunked) VALUES (?, ?, 0, 0)", (index, subject.strip()))
    conn.commit()

    # Display the list of subjects and their IDs after adding
    print(Fore.LIGHTBLUE_EX + "Subjects added successfully.")
    cur.execute("SELECT subid, subject FROM attable")
    rows = cur.fetchall()
    print("\nList of subjects and their IDs:")
    for row in rows:
        print(f"Subject ID: {row[0]}, Subject: {row[1]}")
    
    # Reset color back to default
    print(Style.RESET_ALL)
    
    conn.close()

# Function to clear the database
def clear_database():
    conn = sql.connect("attendance.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM attable")
    row = cur.fetchone()
    if row[0] == 0:
        # If there are no records, show that the database is already empty
        print(Fore.RED + "Database is already empty.")
    else:
        # Ask for confirmation from the user before clearing the database
        confirm = input("Are you sure you want to clear the database? (y/n): ")
        if confirm.lower() == 'y':
            cur.execute("DELETE FROM attable")  # Clear all records from the table
            conn.commit()
            print(Fore.WHITE + "Database cleared successfully.")
        else:
            print(Fore.WHITE + "Database not cleared.")
    
    # Reset color back to default
    print(Style.RESET_ALL)
    
    conn.close()

# Function to update attendance for a specific subject
def update_attendance():
    conn = sql.connect("attendance.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM attable")
    record_count = cur.fetchone()[0]
    conn.close()

    if record_count == 0:
        # If there are no records, show that there is nothing to update
        print(Fore.RED + "There are no records in the database.")
        return

    try:
        # Get the subject ID from the user to update attendance
        subject_id = int(input(Fore.LIGHTBLUE_EX + "Enter the subject ID to update attendance: "))
        conn = sql.connect("attendance.db")
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM attable WHERE subid = ?", (subject_id,))
        subject_count = cur.fetchone()[0]
        if subject_count == 0:
            # If the subject ID doesn't exist in the database, show an error
            print(Fore.RED + "No such subject ID found in the database.")
            conn.close()
            return

        # Get the attendance counts from the user
        attended = int(input(Fore.LIGHTBLUE_EX + "Enter the number of times attended: "))
        bunked = int(input(Fore.LIGHTBLUE_EX + "Enter the number of times bunked: "))
        cur.execute("UPDATE attable SET attended = ?, bunked = ? WHERE subid = ?", (attended, bunked, subject_id))
        conn.commit()
        conn.close()
        print(Fore.WHITE + "Attendance updated successfully.")
    except ValueError:
        # Handle invalid input for subject ID and attendance counts
        print(Fore.RED + "Invalid input. Please enter a valid subject ID and attendance counts.")

# Function to show the list of subject IDs and their attendance percentages
def show_subject_ids():
    conn = sql.connect("attendance.db")
    cur = conn.cursor()
    cur.execute("SELECT subid, subject, attended, bunked FROM attable")
    rows = cur.fetchall()
    conn.close()
    if not rows:
        # If there are no records, show that the database is empty
        print(Fore.RED + "\nThere are no records in the database.\n")
    else:
        # Display subject IDs, subjects, and their attendance percentages
        for row in rows:
            total_classes = row[2] + row[3]
            if total_classes == 0:
                percentage = 0
            else:
                percentage = (row[2] / total_classes) * 100
            print(Fore.LIGHTBLUE_EX + f"Subject ID: {row[0]}, Subject: {row[1]}, Attendance Percentage: {percentage:.2f}%")

# Function to show the attendance status for all subjects
def show_attendance_status():
    conn = None  # Define the variable before the try-except block
    try:
        conn = sql.connect("attendance.db")
        cur = conn.cursor()
        cur.execute('SELECT * FROM attable')
        rows = cur.fetchall()
        
        if not rows:
            # If there are no records, show that the database is empty
            print(Fore.LIGHTRED_EX + "No records in database.")
            print(Style.RESET_ALL)
            return

        print(Fore.LIGHTBLUE_EX + "Attendance status:")
        for w in rows:
            total_classes = w[2] + w[3]
            if total_classes == 0:
                percentage = 0
            else:
                percentage = (w[2] / total_classes) * 100
            print(Fore.LIGHTBLUE_EX + f"Subject ID {w[0]}, {w[1]}, Attendance Percentage: {percentage:.2f}%")

        # Reset color back to default
        print(Style.RESET_ALL)

    except:
        # Handle any errors that occur while fetching data from the database
        print(Fore.LIGHTRED_EX + "No records in database.")
        print(Style.RESET_ALL)

    finally:
        if conn:
            conn.close()

# Main function
def main():
    create_table()

    while True:
        print(Fore.LIGHTYELLOW_EX + "\nAttendance Monitoring System")
        print(Fore.YELLOW + "1. Add subjects")
        print(Fore.YELLOW + "2. Update attendance")
        print(Fore.YELLOW + "3. Show subject IDs")
        print(Fore.YELLOW + "4. Show attendance status")
        print(Fore.YELLOW + "5. Clear Database")
        print(Fore.YELLOW + "6. Exit")
        choice = input(Fore.YELLOW + "Enter your choice: ")

        if choice == '1':
            add_subjects()
        elif choice == '2':
            update_attendance()
        elif choice == '3':
            show_subject_ids()
        elif choice == '4':
            show_attendance_status()
        elif choice == '5':
            clear_database()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

#Bug Tracker program to log, view and track status of bugs

bug_database = {}

def log_bug(title, description, reporter, assignee):
    bug_id = len(bug_database) + 1
    bug_info = {
        'title': title,
        'description': description,
        'reporter': reporter,
        'assignee': assignee,
        'status': 'Open'
    }
    bug_database[bug_id] = bug_info
    print(f"Bug #{bug_id} logged successfully.")

def view_bugs():
    if not bug_database:
        print("Bug database is empty.")
    else:
        print("Bug ID | Title | Status")
        print("-----------------------")
        for bug_id, bug_info in bug_database.items():
            print(f"{bug_id} | {bug_info['title']} | {bug_info['status']}")

def assign_bug(bug_id, assignee):
    if bug_id not in bug_database:
        print("Invalid bug ID.")
    else:
        bug_database[bug_id]['assignee'] = assignee
        print(f"Bug #{bug_id} assigned to {assignee}.")

def close_bug(bug_id):
    if bug_id not in bug_database:
        print("Invalid bug ID.")
    else:
        bug_database[bug_id]['status'] = 'Closed'
        print(f"Bug #{bug_id} closed.")

if __name__ == "__main__":
    while True:
        print("\nBug Tracking System Menu:")
        print("1. Log a Bug")
        print("2. View Bugs")
        print("3. Assign Bug")
        print("4. Close Bug")
        print("5. Exit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice == '1':
            title = input("Enter bug title: ")
            description = input("Enter bug description: ")
            reporter = input("Enter reporter's name: ")
            assignee = input("Enter assignee's name: ")
            log_bug(title, description, reporter, assignee)

        elif choice == '2':
            view_bugs()

        elif choice == '3':
            bug_id = int(input("Enter bug ID: "))
            assignee = input("Enter assignee's name: ")
            assign_bug(bug_id, assignee)

        elif choice == '4':
            bug_id = int(input("Enter bug ID: "))
            close_bug(bug_id)

        elif choice == '5':
            print("Exiting Bug Tracking System.")
            break

        else:
            print("Invalid choice. Please try again.")

from crud import create_member, update_member, delete_member,create_tee_time,create_course, update_course, delete_course, create_payment, update_payment,delete_payment
from models import SessionLocal
from datetime import datetime
from contextlib import contextmanager

# Utility function to handle session management
@contextmanager
# turns function into a context maneger allowing to use with
def get_db_session():
    db = SessionLocal()
    try:
        yield db # returns the db session
    finally:
        db.close()

# Simplified member interaction
def handle_add_member():
    with get_db_session() as db:
        name = input('Enter member name: ')
        membership_type = input('Enter membership type: ')
        status = input('Enter membership status (active/inactive): ')
        member = create_member(db, name, membership_type, status)
        print(f"Member '{member.name}' added successfully.")
        
def handle_update_member():
    member_id = int(input('Enter member ID: '))
    name = input('Enter new name (leave blank to keep current): ')
    membership_type = input('Enter new membership type (leave blank to keep current): ')
    status = input('Enter new status (leave blank to keep current): ')
    
    with get_db_session() as db:
        member = update_member(db, member_id, name or None, membership_type or None, status or None)
        if member:
            print(f"Member {member_id} updated.")
        else:
            print("Member not found.")

def handle_delete_member():
    member_id = int(input('Enter member ID to delete: '))
    confirm = input(f"Are you sure you want to delete member {member_id}? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("Deletion cancelled.")
        return

    with get_db_session() as db:
        member = delete_member(db, member_id)
        if member:
            print(f"Member {member_id} deleted successfully.")
        else:
            print("Member not found.")

# TeeTime interaction
def handle_add_tee_time():
    with get_db_session() as db:
        member_id = int(input('Enter member ID: '))
        course_id = int(input('Enter course ID: '))
        date_time_str = input('Enter tee time (YYYY-MM-DD HH:MM:SS): ')
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
        tee_time = create_tee_time(db, member_id, course_id, date_time)
        print(f"Tee Time added for member {member_id} on {date_time}.")
        
def handle_update_tee_time():
    tee_time_id = int(input('Enter Tee Time ID to update: '))
    member_id = input('Enter new member ID (leave blank to keep current): ')
    course_id = input('Enter new course ID (leave blank to keep current): ')
    date_time_str = input('Enter new tee time (YYYY-MM-DD HH:MM:SS) (leave blank to keep current): ')
    
    date_time = None
    if date_time_str:
        date_time = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')

    with get_db_session() as db:
        tee_time = update_tee_time(db, tee_time_id, member_id or None, course_id or None, date_time or None)
        if tee_time:
            print(f"Tee Time {tee_time_id} updated successfully.")
        else:
            print(f"Tee Time {tee_time_id} not found.")

def handle_delete_tee_time():
    tee_time_id = int(input('Enter Tee Time ID to delete: '))
    confirm = input(f"Are you sure you want to delete Tee Time {tee_time_id}? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("Deletion cancelled.")
        return

    with get_db_session() as db:
        tee_time = delete_tee_time(db, tee_time_id)
        if tee_time:
            print(f"Tee Time {tee_time_id} deleted successfully.")
        else:
            print(f"Tee Time {tee_time_id} not found.)t found.") 
    

def handle_add_course():
    with get_db_session() as db:
        name = input('Enter course name: ')
        location = input('Enter course location: ')
        holes = int(input("Enter course holes: "))  
        par = int(input('Enter course par: '))
        course = create_course(db, name, location, par,holes)
        print(f"Course '{course.name}' added successfully.")   

def handle_update_course():
    course_id= int(input('Enter course ID:'))
    name= input('Enter course name: ')
    location=input('Enter course location: ')
    hole=int(input('Enter course holes:'))
    # par=int('Enter course par:')
    
    with get_db_session() as db:
        course= update_course(db, name or None,location or None,hole or None)
        if course:
            print(f"Course {course_id} updated. ")
        else:
            print("Course not found.")
            
def handle_delete_course():
    course_id = int(input('Enter course ID: ')) 
    with get_db_session() as db:
        course = delete_course(db, course_id)
        if course:
            print(f"Course {course_id} deleted successfully.")
        else:
            print("Course not found.")
            
def handle_add_payment():
    with get_db_session() as db:
        member_id = int(input('Enter member ID: '))
        amount = float(input('Enter payment amount: '))
        date_time_str = input('Enter payment date (YYYY-MM-DD HH:MM:SS): ')
        date = datetime.strptime(date_time_str, '%Y-%m-%d %H:%M:%S')
        payment = create_payment(db, member_id, amount, date)
        print(f"Payment of {payment.amount} added for member {payment.member_id}.")
        
def handle_update_payment():
    member_id= int(input('Enter member ID: '))
    amount =input('Enter new amount(leave it blank if not changes):')
    date=input('Enter new date(leave it blank if not changes): ')
    with get_db_session() as db:
        amount=update_payment(db, member_id, amount or None, date or None)
        if payment:
            print(f"Member {member_id} updated. ")
        else:
            print("payment not found")       

# Main menu
def member_menu():
    print('\n---Mange Members ---')
    print("1. Add a new member")
    print("2. Upadate a member")
    print("3. Delete a member")
    print("4. Back to the main menu")
    return input("Select an option:")

def handle_member_menu():
    while True:
        choice = member_menu()
        if choice == '1':
            handle_add_member()
        elif choice == '2':
            handle_update_member()
        elif choice == '3':
            handle_delete_member()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

            
def tee_time_menu():
    print("\n--- Manage Tee Times ---")
    print("1. Add a new tee time")
    print("2. Update a tee time")
    print("3. Delete a tee time")
    print("4. Back to main menu")
    return input("Select an option: ")

def handle_tee_time_menu():
    while True:
        choice = tee_time_menu()
        if choice == '1':
            handle_add_tee_time()
        elif choice == '2':
            handle_update_tee_time()
        elif choice == '3':
            handle_delete_tee_time()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Sub-menu for managing courses
def course_menu():
    print("\n--- Manage Courses ---")
    print("1. Add a new course")
    print("2. Update a course")
    print("3. Delete a course")
    print("4. Back to main menu")
    return input("Select an option: ")

def handle_course_menu():
    while True:
        choice = course_menu()
        if choice == '1':
            handle_add_course()
        elif choice == '2':
            handle_update_course()
        elif choice == '3':
            handle_delete_course()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Sub-menu for managing payments
def payment_menu():
    print("\n--- Manage Payments ---")
    print("1. Add a new payment")
    print("2. Update a payment")
    print("3. Delete a payment")
    print("4. Back to main menu")
    return input("Select an option: ")

def handle_payment_menu():
    while True:
        choice = payment_menu()
        if choice == '1':
            handle_add_payment()
        elif choice == '2':
            handle_update_payment()
        elif choice == '3':
            handle_delete_payment()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Main menu with categories
def main_menu():
    print("\n--- Golf Management System ---")
    print("1. Manage Members")
    print("2. Manage Tee Times")
    print("3. Manage Courses")
    print("4. Manage Payments")
    print("5. Exit")
    return input("Select an option: ")

def run():
    while True:
        choice = main_menu()
        if choice == '1':
            handle_member_menu()
        elif choice == '2':
            handle_tee_time_menu()
        elif choice == '3':
            handle_course_menu()
        elif choice == '4':
            handle_payment_menu()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    print("Running Golf Management System...")
    run()
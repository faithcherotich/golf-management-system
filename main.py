from crud import create_member, update_member, delete_member,create_tee_time,update_tee_time,delete_tee_time, create_course, update_course, delete_course, create_payment, update_payment,delete_payment,get_all_members,get_all_tee_times,get_all_courses,get_all_payments
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
        try:
            name = input('Enter member name: ')
            membership_type = input('Enter membership type: ')
            status = input('Enter membership status (active/inactive): ').strip().lower()
            
            if status not in ['active', 'inactive']:
                print("Invalid status. Please enter 'active' or 'inactive'.")
                return
            
            member = create_member(db, name, membership_type, status)
            print(f"Member '{member.name}' added successfully.")
        
        except ValueError as e:
            print(f"Error: {e}. Please try again.")
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
def view_members():
    with get_db_session() as db:
        members = get_all_members(db)  # Fetch all members
        
        if members:
            print("\n--- List of Members ---")
            print(f"{'ID':<5} {'Name':<20} {'Membership Type':<15} {'Status':<10}")
            print('-' * 50)
            
            for member in members:
                print(f"{member.id:<5} {member.name:<20} {member.membership_type:<15} {member.status:<10}")
        else:
            print("No members found.")            

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
        tee_time = update_tee_time(
            db,
            tee_time_id,
            member_id if member_id else None,
            course_id if course_id else None,
            date_time
        )
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
            print(f"Tee Time {tee_time_id} not found.")
def view_tee_times(db):
    tee_times = get_all_tee_times(db) 
    print("\n--- List of Tee Times ---")
    print(f"{'ID':<5} {'Member ID':<10} {'Course ID':<10} {'Date Time'}")
    print("-" * 50)
    
    for tee_time in tee_times:
        # Use a default value if tee_time.date_time is None
        date_time_str = tee_time.date_time.strftime('%Y-%m-%d %H:%M:%S') if tee_time.date_time else 'N/A'
        print(f"{tee_time.id:<5} {tee_time.member_id:<10} {tee_time.course_id:<10} {date_time_str}")

    print("\n")
def handle_add_course():
    with get_db_session() as db:
        name = input('Enter course name: ')
        location = input('Enter course location: ')
        holes = int(input("Enter course holes: "))  
        par = int(input('Enter course par: '))
        course = create_course(db, name, location, par,holes)
        print(f"Course '{course.name}' added successfully.")   

def handle_update_course():
    course_id = int(input('Enter course ID: '))
    name = input('Enter new course name (leave blank to keep current): ')
    location = input('Enter new course location (leave blank to keep current): ')
    holes_input = input('Enter new course holes (leave blank to keep current): ')
    par_input = input('Enter new course par (leave blank to keep current): ')

    # Validate holes and par and convert to integers if provided
    holes = None
    if holes_input:
        try:
            holes = int(holes_input)
        except ValueError:
            print("Invalid number for holes. Please enter a valid number.")
            return  # Stop the function if invalid input is provided

    par = None
    if par_input:
        try:
            par = int(par_input)
        except ValueError:
            print("Invalid number for par. Please enter a valid number.")
            return  # Stop the function if invalid input is provided

    with get_db_session() as db:
        course = update_course(db, course_id, name or None, location or None, holes, par)
        if course:
            print(f"Course {course_id} updated successfully.")
        else:
            print("Course not found.")
def view_courses():
    with get_db_session() as db:
        courses = get_all_courses(db)  # Fetch all courses
        
        if courses:
            print("\n--- List of Courses ---")
            print(f"{'ID':<5} {'Name':<20} {'Location':<15} {'Par':<5} {'Holes':<5}")
            print('-' * 50)
            
            for course in courses:
                print(f"{course.id:<5} {course.name:<20} {course.location:<15} {course.par:<5} {course.holes:<5}")
        else:
            print("No courses found.")
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
    member_id = int(input('Enter member ID: '))
    amount_input = input('Enter new amount (leave it blank if no changes): ')
    date_input = input('Enter new date (leave it blank if no changes): ')

    # Validate amount and convert to float if provided
    amount = None
    if amount_input:
        try:
            amount = float(amount_input)
        except ValueError:
            print("Invalid amount. Please enter a valid number.")
            return  # Stop the function if invalid input is provided

    # Validate date and use it if provided
    date = date_input if date_input else None

    with get_db_session() as db:
        payment_updated = update_payment(db, member_id, amount, date)

        if payment_updated:
            print(f"Member {member_id} payment updated successfully.")
        else:
            print("Payment not found or update failed.")
def view_payments():
    with get_db_session() as db:
        payments = get_all_payments(db)  # Fetch all payments
        
        if payments:
            print("\n--- List of Payments ---")
            print(f"{'ID':<5} {'Member ID':<10} {'Amount':<10} {'Date':<20}")
            print('-' * 50)
            
            for payment in payments:
                print(f"{payment.id:<5} {payment.member_id:<10} {payment.amount:<10} {payment.date}")
        else:
            print("No payments found.")           
def handle_delete_payment():
    payment_id = int(input('Enter Payment ID to delete: '))
    confirm = input(f"Are you sure you want to delete Payment {payment_id}? (yes/no): ")
    
    if confirm.lower() != 'yes':
        print("Deletion cancelled.")
        return

    with get_db_session() as db:
        payment = delete_payment(db, payment_id)
        if payment:
            print(f"Payment {payment_id} deleted successfully.")
        else:
            print(f"Payment {payment_id} not found.")            
# Main menu
def member_menu():
    print('\n---Manage Members ---')
    print("1. Add a new member")
    print("2. Update a member")
    print("3. Delete a member")
    print("4. View all members")  # New option for viewing members
    print("5. Back to the main menu")
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
            view_members()  # Call the view function
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")
            
def tee_time_menu():
    print("\n--- Manage Tee Times ---")
    print("1. Add a new tee time")
    print("2. Update a tee time")
    print("3. View tee time")
    print("4. Delete a tee time")
    print("5. Back to main menu")
    return input("Select an option: ")

def handle_tee_time_menu():
    while True:
        choice = tee_time_menu()
        if choice == '1':
            handle_add_tee_time()
        elif choice == '2':
            handle_update_tee_time()
        elif choice == '3':
           with get_db_session() as db:
            view_tee_times(db)
        elif choice == '4':
            handle_delete_tee_time()
        elif choice =='5':
            break
        else:
            print("Invalid choice. Please try again.")
# Sub-menu for managing courses
def course_menu():
    print("\n--- Manage Courses ---")
    print("1. Add a new course")
    print("2. Update a course")
    print("3. Delete a course")
    print("4. View courses")
    print("5. Back to main menu")
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
            view_courses()
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

# Sub-menu for managing payments
def payment_menu():
    print("\n--- Manage Payments ---")
    print("1. Add a new payment")
    print("2. Update a payment")
    print("3. Delete a payment")
    print("4. View payments")
    print("5. Back to main menu")
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
            view_payments()
        elif choice == '5':
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
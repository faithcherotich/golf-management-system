from sqlalchemy.orm import Session
from models import Member, TeeTime,  Course,  Payment

# Helper functions to handle common tasks
# db.instance of Session to query a member
#.filter condition to the query
#Member.id==member_id filter rows in member table where id column 
#.first() executes the query and return results
def get_member(db: Session, member_id: int):
    return db.query(Member).filter(Member.id == member_id).first()

# CRUD Operations for Member
def create_member(db: Session, name: str, membership_type: str, status: str):
    member = Member(name=name, membership_type=membership_type, status=status)
    db.add(member)
    db.commit()
    db.refresh(member)
    return member

def update_member(db: Session, member_id: int, name: str = None, membership_type: str = None, status: str = None):
    member = get_member(db, member_id)
    if not member:
        return None
    if name:
        member.name = name
    if membership_type:
        member.membership_type = membership_type
    if status:
        member.status = status
    db.commit()
    db.refresh(member)
    return member

def delete_member(db, member_id):
    try:
        # Handle associated payments
        payments = db.query(Payment).filter(Payment.member_id == member_id).all()
        for payment in payments:
            db.delete(payment)
        
        # Commit changes for payments
        db.commit()

        # Delete the member
        member = db.query(Member).filter(Member.id == member_id).first()
        if member:
            db.delete(member)
            db.commit()
            return member
        else:
            return None
    
    except Exception as e:
        db.rollback()  # Rollback in case of error
        print(f"An error occurred: {e}")
        return None
# TeeTime operations
def create_tee_time(db: Session, member_id: int, course_id: int, date_time):
    tee_time = TeeTime(member_id=member_id, course_id=course_id, date_time=date_time)
    db.add(tee_time)
    db.commit()
    db.refresh(tee_time)
    return tee_time

def update_tee_time(db, tee_time_id, member_id=None, course_id=None, date_time=None):
    # Fetch the tee time object by ID
    tee_time = db.query(TeeTime).filter(TeeTime.id == tee_time_id).first()
    
    if tee_time:
        # Update fields if new values are provided
        if member_id is not None:
            tee_time.member_id = member_id
        if course_id is not None:
            tee_time.course_id = course_id
        if date_time is not None:
            tee_time.date_time = date_time
        
        # Commit the changes to the database
        db.commit()
        return tee_time
    else:
        return None

def delete_tee_time(db: Session, tee_time_id: int):
    # Fetch the tee time to be deleted
    tee_time = db.query(TeeTime).filter(TeeTime.id == tee_time_id).first()
    
    if not tee_time:
        return None  # TeeTime not found
    
    member_id = tee_time.member_id  # Get the member_id associated with the tee time
    
    # Delete the tee time
    db.delete(tee_time)
    db.commit()

    # Check if the member has any other tee times
    other_tee_times = db.query(TeeTime).filter(TeeTime.member_id == member_id).all()

    if not other_tee_times:  # If no other tee times exist for this member
        # Delete the member as well
        member = db.query(Member).filter(Member.id == member_id).first()
        if member:
            db.delete(member)
            db.commit()
            print(f"Member {member_id} deleted as well.")

    return tee_time
#crud for courses
def create_course(db,name,location,par,holes):
    course=Course(name=name, location=location,par=par, holes=holes)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course
def update_course(db, course_id: int, name: str = None, location: str = None, holes: int = None, par: int = None):
    course = db.query(Course).filter(Course.id == course_id).first()
    if not course:
        return None

    if name is not None:
        course.name = name
    if location is not None:
        course.location = location
    if holes is not None:
        course.holes = holes
    if par is not None:
        course.par = par

    db.commit()
    db.refresh(course)  # Refresh to get the updated values
    return course

def delete_course(db, course_id):
    course = db.query(Course).filter(Course.id == course_id).first()  # Corrected the filter condition
    if course:
        db.delete(course)
        db.commit()
    return course
def get_course_by_id(db, course_id):
    return db.query(Course).filter(Course.id == course_id).first()

#crud for payment
def create_payment(db, member_id, amount, date):
    payment = Payment(member_id=member_id, amount=amount, date=date)  # Added member_id as a keyword
    db.add(payment)
    db.commit()
    db.refresh(payment)
    return payment

def update_payment(db, payment_id, amount=None, date=None):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment:
        if amount is not None:
            payment.amount = amount
        if date:
            payment.date = date
        db.commit()
        db.refresh(payment)
    return payment

def delete_payment(db,payment_id):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()  
    if payment:
        db.delete(payment)
        db.commit()
    return payment

def get_payment_by_id(db, payment_id):
    return db.query(Payment).filter(Payment.id == payment_id).first()  # Removed .first() from filter
  
def get_member_by_id(db: Session, member_id: int):
    return db.query(Member).filter(Member.id == member_id).first()

# View all members
def get_all_members(db: Session):
    return db.query(Member).all()

# View a single course by ID
def get_course_by_id(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()

# View all courses
def get_all_courses(db: Session):
    return db.query(Course).all()

# View a single tee-time by ID
def get_tee_time_by_id(db: Session, tee_time_id: int):
    return db.query(TeeTime).filter(TeeTime.id == tee_time_id).first()

# View all tee-times
def get_all_tee_times(db: Session):
    return db.query(TeeTime).all()

# View a single payment by ID
def get_payment_by_id(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()

# View all payments
def get_all_payments(db: Session):
    return db.query(Payment).all()
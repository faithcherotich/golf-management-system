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

def delete_member(db: Session, member_id: int):
    member = get_member(db, member_id)
    if not member:
        return None
    db.delete(member)
    db.commit()
    return member

# TeeTime operations
def create_tee_time(db: Session, member_id: int, course_id: int, date_time):
    tee_time = TeeTime(member_id=member_id, course_id=course_id, date_time=date_time)
    db.add(tee_time)
    db.commit()
    db.refresh(tee_time)
    return tee_time

def update_tee_time(db: Session, tee_time_id: int, member_id: int = None, course_id: int = None, date_time = None):
    tee_time = db.query(TeeTime).filter(TeeTime.id == tee_time_id).first()
    if not tee_time:
        return None  # Tee time not found
    if member_id:
        tee_time.member_id = member_id
    if course_id:
        tee_time.course_id = course_id
    if date_time:
        tee_time.date_time = date_time
    db.commit()
    db.refresh(tee_time)
    return tee_time

def delete_tee_time(db: Session, tee_time_id: int):
    tee_time = db.query(TeeTime).filter(TeeTime.id == tee_time_id).first()
    if not tee_time:
        return None  # Tee time not found
    db.delete(tee_time)
    db.commit()
    return tee_time
#crud for courses
def create_course(db,name,location,par,holes):
    course=Course(name=name, location=location,par=par, holes=holes)
    db.add(course)
    db.commit()
    db.refresh(course)
    return course
def update_course(db,course_id,name=None, location=None,par=None):
    course = db.query(Course).filter(Course.id == course_id).first()
    if course: 
        if name:
            course.name=name
        if location:
            course.location=location
        if par:
            course.par=par
        db.commit()
        db.refresh(course)
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

def update_payment(db, payment_id, member_id=None, amount=None, date=None):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment:
        payment.member_id= member_id
        if amount:
           payment.amount = amount
        if date:
           payment.date = date
        db.commit()
        db.refresh(payment)
    return payment

def delete_payment(id,payment_id):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()  
    if payment:
        db.delete(payment)
        db.commit()
    return payment

def get_payment_by_id(db, payment_id):
    return db.query(Payment).filter(Payment.id == payment_id).first()  # Removed .first() from filter
  

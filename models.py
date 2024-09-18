from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()

class Member(Base):
    __tablename__ = 'members'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    membership_type = Column(String, nullable=False)
    status = Column(String, default='active')
    
    tee_times = relationship("TeeTime", back_populates="member")
    payments = relationship("Payment", back_populates="member")

    def __repr__(self):
        return f"<Member(name={self.name}, type={self.membership_type}, status={self.status})>"

class TeeTime(Base):
    __tablename__ = 'tee_times'
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    course_id = Column(Integer, ForeignKey('courses.id'), nullable=False)
    date_time = Column(DateTime, nullable=False)
    
    member = relationship("Member", back_populates="tee_times")
    course = relationship("Course", back_populates="tee_times")

    def __repr__(self):
        return f"<TeeTime(member_id={self.member_id}, course_id={self.course_id}, date_time={self.date_time})>"


class Course(Base):
    __tablename__ = 'courses'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    location = Column(String, nullable=False)
    par = Column(Integer, nullable=False)
    holes = Column(Integer)
    tee_times = relationship("TeeTime", back_populates="course")

    def __repr__(self):
        return f"<Course(name={self.name}, location={self.location}, par={self.par})>"


class Payment(Base):
    __tablename__ = 'payments'
    
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(Integer, ForeignKey('members.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date = Column(DateTime, nullable=False)
    
    member = relationship("Member", back_populates="payments")

    def __repr__(self):
        return f"<Payment(member_id={self.member_id}, amount={self.amount}, date={self.date})>"

DATABASE_URL = 'sqlite:///golf_management.db'
engine = create_engine(DATABASE_URL)

# Create tables
Base.metadata.create_all(bind=engine)

# SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
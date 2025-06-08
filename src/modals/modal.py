from sqlalchemy import Column, Integer, String, ForeignKey
from src.database.db_config import Base, engine
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, default="student")
    
    # Relationships
    teacher = relationship("Teacher", back_populates="user", uselist=False)
    student = relationship("Student", back_populates="user", uselist=False)

class Teacher(Base):
    __tablename__ = "teacher"
    
    id = Column(Integer, primary_key=True, index=True)
    teacher_name = Column(String, nullable=False)
    subject = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    
    # Relationships
    user = relationship("User", back_populates="teacher")
    students = relationship("Student", back_populates="teacher")
    subject_marks = relationship("SubjectMark", back_populates="teacher")

class Student(Base):    
    __tablename__ = "student"
    
    id = Column(Integer, primary_key=True, index=True)
    student_name = Column(String, nullable=False)
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    user_id = Column(Integer, ForeignKey("user.id"), unique=True)
    
    # Relationships
    user = relationship("User", back_populates="student")
    teacher = relationship("Teacher", back_populates="students")
    subject_marks = relationship("SubjectMark", back_populates="student")

class SubjectMark(Base):
    __tablename__ = "subject_mark"
    
    id = Column(Integer, primary_key=True, index=True)
    mark = Column(Integer)
    subject_name = Column(String, nullable=False)
    student_id = Column(Integer, ForeignKey("student.id"))
    teacher_id = Column(Integer, ForeignKey("teacher.id"))
    
    # Relationships
    teacher = relationship("Teacher", back_populates="subject_marks")
    student = relationship("Student", back_populates="subject_marks")

# Create all tables
Base.metadata.create_all(bind=engine)
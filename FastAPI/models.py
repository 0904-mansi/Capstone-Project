# from sqlalchemy import Column,Table, Integer, String, Date, DateTime, ForeignKey, Enum
# from sqlalchemy.orm import relationship
# from .database import Base
# import string
# import secrets

# class Project(Base):
#     __tablename__ = "projects"
#     id = Column(String, primary_key=True, index=True, autoincrement=True)
#     name = Column(String, index=True)
#     description = Column(String)
#     start_date = Column(DateTime)
#     end_date = Column(DateTime)
#     project_manager_id = Column(Integer, ForeignKey('managers.id'), nullable=True)
#     tasker_id = Column(Integer, ForeignKey('employees.id'), nullable=True)

#     project_manager = relationship("Manager", back_populates="requested_projects")
#     tasker = relationship("Employee", back_populates="tasked_projects")

# class Manager(Base):
#     __tablename__ = "managers"
#     id = Column(String, primary_key=True, index=True, autoincrement=True)
#     firstName = Column(String)
#     middleName = Column(String, nullable=True)
#     lastName = Column(String)
#     phoneNo = Column(String, unique=True)
#     email = Column(String, unique=True)
#     addharNo = Column(String, unique=True)
#     dOB = Column(Date)
#     salary = Column(String)
#     joinDate = Column(Date)

#     requested_projects = relationship("Project", back_populates="project_manager")

# class Employee(Base):
#     __tablename__ = "employees"
#     id = Column(String, primary_key=True, index=True, autoincrement=True)
#     firstName = Column(String)
#     middleName = Column(String, nullable=True)
#     lastName = Column(String)
#     phoneNo = Column(String, unique=True)
#     email = Column(String, unique=True)
#     addharNo = Column(String, unique=True)
#     dOB = Column(Date)
#     salary = Column(String)
#     joinDate = Column(Date)
#     skills = Column(String, default="Engineer")
#     manager_id = Column(Integer, ForeignKey('managers.id'), nullable=True)
#     availability = Column(String)

#     tasked_projects = relationship("Project", back_populates="tasker")

# class Notice(Base):
#     __tablename__ = "notices"
#     id = Column(String, primary_key=True, index=True, autoincrement=True)
#     title = Column(String)
#     description = Column(String)
#     publishDate = Column(DateTime)

# class Requests(Base):
#     __tablename__ = "requests"
#     id = Column(String, primary_key=True, index=True, autoincrement=True)
#     manager_id = Column(Integer, ForeignKey('managers.id'), nullable=True)
#     project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
#     message = Column(String)
#     created_at = Column(DateTime)
#     status = Column(String, default='Pending')
#     comment = Column(String, nullable=True, default="")

#     manager = relationship("Manager")
#     project = relationship("Project")
#     employees = relationship("Employee", secondary="requests_employees")

# class EmployeeLeaveApplication(Base):
#     __tablename__ = "employee_leave_applications"
#     id = Column(String, primary_key=True, index=True, autoincrement=True)
#     employee_id = Column(Integer, ForeignKey('employees.id'), nullable=True)
#     start_date = Column(Date)
#     end_date = Column(Date)
#     reason = Column(String)
#     status = Column(String, default='Pending')

# class ManagerLeaveApplication(Base):
#     __tablename__ = "manager_leave_applications"
#     id = Column(String, primary_key=True, index=True, autoincrement=True)
#     manager_id = Column(Integer, ForeignKey('managers.id'), nullable=True)
#     start_date = Column(Date)
#     end_date = Column(Date)
#     reason = Column(String)
#     status = Column(String, default='Pending')

# # Association table for many-to-many relationship between Requests and Employees
# requests_employees = Table(
#     'requests_employees', Base.metadata,
#     Column('request_id', Integer, ForeignKey('requests.id'), primary_key=True),
#     Column('employee_id', Integer, ForeignKey('employees.id'), primary_key=True)
# )


# class Users(Base):
#     __tablename__ = 'users'

#     user_id = Column(Integer, primary_key=True, index=True)
#     firstName = Column(String(50))
#     lastName = Column(String(50))
#     email = Column(String(70), unique=True)
#     password = Column(String(50), default='Auto-generated')
#     skills = Column(String(250), default='Engineer')
#     availability = Column(String(250), default="Unassigned", nullable=True)
#     role = Column(String(20), default='Employee')

#     def save(self, *args, **kwargs):
#         if self.password:
#             self.password = self.generate_password()
#         super().save(*args, **kwargs)

#     def generate_password(self, length=12):
#         characters = string.ascii_letters + string.digits + string.punctuation
#         return ''.join(secrets.choice(characters) for i in range(length))

from sqlalchemy import Column, Integer, String, Text, ForeignKey, Date, DateTime, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import string
import secrets

Base = declarative_base()

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for i in range(length))

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(50))
    lastName = Column(String(50))
    email = Column(String(70), unique=True)
    password = Column(String(50), default=generate_password())
    skills = Column(String(250), default='Engineer')
    availability = Column(String(250), default='Unassigned', nullable=True)
    role = Column(String(20), default='Employee')

    def save(self, *args, **kwargs):
        if not self.password:
            self.password = generate_password()
        super().save(*args, **kwargs)

class Project(Base):
    __tablename__ = 'projects'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    assigner = "Admin"
    project_manager = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    tasker = Column(Integer, ForeignKey('users.user_id'), nullable=True)

    manager = relationship("User", foreign_keys=[project_manager])
    employee = relationship("User", foreign_keys=[tasker])

class Notice(Base):
    __tablename__ = 'notices'
    
    Id = Column(Integer, primary_key=True, index=True)
    title = Column(String(250))
    description = Column(Text)
    publishDate = Column(DateTime)

class Requests(Base):
    __tablename__ = 'requests'
    
    id = Column(Integer, primary_key=True, index=True)
    manager_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    project_id = Column(Integer, ForeignKey('projects.id'), nullable=True)
    message = Column(Text)
    created_at = Column(Date)
    status = Column(String(20), default='Pending')
    comment = Column(String(200), default="", nullable=True)

    manager = relationship("User", foreign_keys=[manager_id])
    project = relationship("Project", foreign_keys=[project_id])
    employees = relationship("User", secondary='request_employee_link')

class RequestEmployeeLink(Base):
    __tablename__ = 'request_employee_link'
    
    request_id = Column(Integer, ForeignKey('requests.id'), primary_key=True)
    employee_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)

class EmployeeLeaveApplication(Base):
    __tablename__ = 'employee_leave_applications'
    
    Id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    start_date = Column(Date)
    end_date = Column(Date)
    reason = Column(Text)
    status = Column(String(20), default='Pending')

    employee = relationship("User", foreign_keys=[employee_id])

class ManagerLeaveApplication(Base):
    __tablename__ = 'manager_leave_applications'
    
    Id = Column(Integer, primary_key=True, index=True)
    manager_id = Column(Integer, ForeignKey('users.user_id'), nullable=True)
    start_date = Column(Date)
    end_date = Column(Date)
    reason = Column(Text)
    status = Column(String(20), default='Pending')

    manager = relationship("User", foreign_keys=[manager_id])

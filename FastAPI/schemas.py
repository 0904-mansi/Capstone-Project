# from pydantic import BaseModel, EmailStr, validator
# from datetime import date, datetime
# from typing import List, Optional

# def validate_domain_email(value: str):
#     if not value.endswith('@domain.com'):
#         raise ValueError('Email must be an @domain.com address.')
#     return value

# class ProjectCreate(BaseModel):
#     id:str
#     name: str
#     description: str
#     start_date: datetime
#     end_date: datetime
#     project_manager_id: Optional[int] = None
#     tasker_id: Optional[int] = None

# class ManagerCreate(BaseModel):
#     mID:str
#     firstName: str
#     middleName: Optional[str] = None
#     lastName: str
#     phoneNo: str
#     email: EmailStr
#     addharNo: str
#     dOB: date
#     salary: str
#     joinDate: date
#     @validator('email')
#     def must_end_with_domain(cls, v):
#         if not v.endswith('@domain.com'):
#             raise ValueError('Email must end with @domain.com')
    


#     @validator('dOB', 'joinDate', pre=True, always=True)
#     def date_must_be_past(cls, v):
#         if v > date.today():
#             raise ValueError('Date cannot be in the future')
#         return v

# class EmployeeCreate(BaseModel):
#     eID:str
#     firstName: str
#     middleName: Optional[str] = None
#     lastName: str
#     phoneNo: str
#     email: EmailStr
#     addharNo: str
#     dOB: date
#     salary: str
#     joinDate: date
#     skills: str = "Engineer"
#     manager_id: Optional[int] = None
#     availability: str
#     @validator('email')
#     def must_end_with_domain(cls, v):
#         if not v.endswith('@domain.com'):
#             raise ValueError('Email must end with @domain.com')
    


#     @validator('dOB', 'joinDate', pre=True, always=True)
#     def date_must_be_past(cls, v):
#         if v > date.today():
#             raise ValueError('Date cannot be in the future')
#         return v

# class NoticeCreate(BaseModel):
#     title: str
#     description: str
#     publishDate: date


# class RequestsCreate(BaseModel):
#     manager_id: Optional[str] = None
#     project_id: Optional[str] = None
#     employee_ids: List[str]
#     message: str
#     created_at: date
#     status: str = "Pending"
#     comment: Optional[str] = ""

# class EmployeeLeaveApplicationCreate(BaseModel):
#     id:int
#     employee_id: Optional[int] = None
#     start_date: date
#     end_date: date
#     reason: str
#     status: str = "Pending"

#     @validator('start_date', 'end_date', pre=True, always=True)
#     def date_must_be_past(cls, v):
#         if v > date.today():
#             raise ValueError('Date cannot be in the future')
#         return v

# class ManagerLeaveApplicationCreate(BaseModel):
#     id:int
#     manager_id: Optional[int] = None
#     start_date: date
#     end_date: date
#     reason: str
#     status: str = "Pending"

#     @validator('start_date', 'end_date', pre=True, always=True)
#     def date_must_be_past(cls, v):
#         if v > date.today():
#             raise ValueError('Date cannot be in the future')
#         return v


# def validate_domain_email(value: EmailStr) -> EmailStr:
#     if not value.endswith('@domain.com'):
#         raise ValueError('Email must end with @domain.com')
#     return value

# class ProjectUpdate(BaseModel):
#     name: Optional[str] = None
#     description: Optional[str] = None
#     start_date: Optional[date] = None
#     end_date: Optional[date] = None
#     assigner: Optional[str] = None
#     project_manager_id: Optional[str] = None
#     tasker_id: Optional[str] = None

# class ManagerUpdate(BaseModel):
#     mID: str
#     firstName: Optional[str] = None
#     middleName: Optional[str] = None
#     lastName: Optional[str] = None
#     phoneNo: Optional[str] = None
#     email: Optional[EmailStr] = None
#     addharNo: Optional[str] = None
#     dOB: Optional[date] = None
#     salary: Optional[str] = None
#     joinDate: Optional[date] = None
#     @validator('email')
#     def must_end_with_domain(cls, v):
#         if not v.endswith('@domain.com'):
#             raise ValueError('Email must end with @domain.com')
      

# class EmployeeUpdate(BaseModel):
#     firstName: Optional[str] = None
#     middleName: Optional[str] = None
#     lastName: Optional[str] = None
#     phoneNo: Optional[str] = None
#     email: Optional[EmailStr] = None
#     addharNo: Optional[str] = None
#     dOB: Optional[date] = None
#     salary: Optional[str] = None
#     joinDate: Optional[date] = None
#     skills: Optional[str] = None
#     manager_id: Optional[str] = None
#     availability: Optional[str] = None

#     @validator('email')
#     def must_end_with_domain(cls, v):
#         if not v.endswith('@domain.com'):
#             raise ValueError('Email must end with @domain.com')
    
# class NoticeUpdate(BaseModel):
#     title: Optional[str] = None
#     description: Optional[str] = None
#     publishDate: Optional[date] = None

# class RequestsUpdate(BaseModel):
#     manager_id: Optional[str] = None
#     project_id: Optional[str] = None
#     employee_ids: Optional[List[str]] = None
#     message: Optional[str] = None
#     created_at: Optional[date] = None
#     status: Optional[str] = None
#     comment: Optional[str] = None

# class StatusUpdate(BaseModel):
#     status: str


# class UserBase(BaseModel):
#     firstName: str
#     lastName: str
#     email: EmailStr
#     skills: str = "Engineer"
#     availability: Optional[str] = "Unassigned"
#     role: Optional[str] = "Employee"

# class UserCreate(UserBase):
#     password: str

#     @validator('availability')
#     def validate_availability(cls, value):
#         availabilities = ['Assigned', 'Unassigned', 'Manager']
#         if value not in availabilities:
#             raise ValueError(f"Invalid availability: {value}. Must be one of {availabilities}")
#         return value

#     @validator('role')
#     def validate_role(cls, value):
#         roles = ['Employee', 'Manager']
#         if value not in roles:
#             raise ValueError(f"Invalid role: {value}. Must be one of {roles}")
#         return value

# class UserUpdate(UserBase):
#     password: Optional[str] = None

# class UserResponse(UserBase):
#     user_id: int

#     class Config:
#         orm_mode = True

# class SuperUserCreate(BaseModel):
#     username: str
#     email: EmailStr
#     password: str  
    
#     @validator('email')
#     def must_end_with_domain(cls, v):
#         if not v.endswith('@domain.com'):
#             raise ValueError('Email must end with @domain.com')
       
# class EmployeeSkillsUpdate(BaseModel):
#     skills: str

from pydantic import BaseModel, EmailStr, validator,constr
from typing import Optional, List
from datetime import datetime, date

class UserBase(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    skills: str = "Engineer"
    availability: Optional[str] = "Unassigned"
    role: Optional[str] = "Employee"

    @validator('availability')
    def validate_availability(cls, value):
        availabilities = ['Assigned', 'Unassigned', 'Manager']
        if value not in availabilities:
            raise ValueError(f"Invalid availability: {value}. Must be one of {availabilities}")
        return value

    @validator('role')
    def validate_role(cls, value):
        roles = ['Employee', 'Manager']
        if value not in roles:
            raise ValueError(f"Invalid role: {value}. Must be one of {roles}")
        return value



class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: constr(min_length=8)
    skills: str
    availability: str
    role: str

class UserUpdate(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[constr(min_length=8)] = None
    skills: Optional[str] = None
    availability: Optional[str] = None
    role: Optional[str] = None


class ProjectBase(BaseModel):
    name: str
    description: str
    start_date: date
    end_date: date
    project_manager: Optional[int]
    tasker: Optional[int]

class ProjectCreate(BaseModel):
    name: str
    description: str
    start_date: date
    end_date: date
    project_manager: Optional[int] = None
    tasker: Optional[int] = None

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    project_manager: Optional[int] = None
    tasker: Optional[int] = None

class NoticeBase(BaseModel):
    title: str
    description: str
    publishDate:date

class NoticeCreate(BaseModel):
    title: str
    description: str
    publishDate: date

class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    publishDate: Optional[datetime] = None


class RequestBase(BaseModel):
    manager_id: Optional[int]
    project_id: Optional[int]
    message: str
    status: Optional[str] = 'Pending'
    comment: Optional[str] = ''

class RequestsCreate(BaseModel):
    manager_id: Optional[int] = None
    project_id: Optional[int] = None
    employee_ids: List[int]
    message: str
    created_at: date
    status: str = "Pending"
    comment: Optional[str] = ""
    @validator('status')
    def validate_status(cls, value):
        availabilities = ['Pending']
        if value not in availabilities:
            raise ValueError(f"Invalid status: {value}. Must be Pending")
        return value

class RequestsUpdate(BaseModel):
    manager_id: Optional[int] = None
    project_id: Optional[int] = None
    employee_ids: Optional[List[int]] = None
    message: Optional[str] = None
    created_at: Optional[date] = None
    status: Optional[str] = None
    comment: Optional[str] = None


class EmployeeLeaveApplicationBase(BaseModel):
    employee_id: Optional[int]
    start_date: date
    end_date: date
    reason: str
    status: Optional[str] = 'Pending'

class EmployeeLeaveApplicationCreate(BaseModel):
    employee_id: Optional[int] = None
    start_date: date
    end_date: date
    reason: str
    status: str = "Pending"

    @validator('status')
    def validate_status(cls, value):
        availabilities = ['Pending']
        if value not in availabilities:
            raise ValueError(f"Invalid status: {value}. Must be Pending")
        return value

class EmployeeLeaveApplicationUpdate(BaseModel):
    employee_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None
    status: Optional[str] = None

class ManagerLeaveApplicationBase(BaseModel):
    manager_id: Optional[int]
    start_date: date
    end_date: date
    reason: str
    status: Optional[str] = 'Pending'

class ManagerLeaveApplicationCreate(BaseModel):
    manager_id: Optional[int] = None
    start_date: date
    end_date: date
    reason: str
    status: str = "Pending"

    @validator('status')
    def validate_status(cls, value):
        availabilities = ['Pending']
        if value not in availabilities:
            raise ValueError(f"Invalid status: {value}. Must be Pending")
        return value


class ManagerLeaveApplicationUpdate(BaseModel):
    manager_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    reason: Optional[str] = None
    status: Optional[str] = None
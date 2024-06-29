import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'empmanagement.settings')
django.setup()
from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, HTMLResponse
import asyncpg
from datetime import date
from employee.models import *
from .schemas import *
from django.utils.dateparse import parse_datetime, parse_date
from typing import Optional, List
from django.contrib.auth.models import User
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from starlette.middleware.authentication import AuthenticationMiddleware
from starlette.middleware.sessions import SessionMiddleware
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import authenticate,login,logout
from pydantic import BaseModel, validator
from .database import * 
from django.shortcuts import get_object_or_404
from sqlalchemy.orm import Session



# Set the Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'empmanagement.settings')
django.setup()

from django.shortcuts import render
from django.conf import settings
from fastapi.templating import Jinja2Templates
from .database import *
from . import models, schemas


from .database import SessionLocal, engine
from . import models, schemas

# Initialize FastAPI app
app = FastAPI()

# Create the database tables
# models.Base.metadata.create_all(bind=engine)

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

templates = Jinja2Templates(directory="empmanagement/template")
# PostgreSQL database connection settings
# DATABASE_URL = "postgresql://postgres:jaiguruji@localhost/emp_fastapi"


# # Add session and authentication middleware
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
# app.add_middleware(AuthenticationMiddleware)

# # Dependency to get the current Django user
# def get_current_user(request: Request):
#     if not request.user.is_authenticated:
#         raise HTTPException(status_code=401, detail="Not authenticated")
#     return request.user


#Notice

# @app.get("/notices", response_class=JSONResponse)
# def notice(request: Request, db: Session = Depends(get_db)):
#     notices = Notice.objects.all()  # Adjust this to your ORM's method
#     notices_list = [{"id": notice.Id, "title": notice.title, "description": notice.description} for notice in notices]
#     return JSONResponse(content={"notices": notices_list})

# @app.post("/notices/")
# def create_notice(notice: NoticeCreate):
#     try:
#         new_notice = Notice(
#             title=notice.title,
#             description=notice.description,
#             publishDate=notice.publishDate,
#         )
#         new_notice.save()
#         return {"message": "Notice created successfully"}
#     except ValidationError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.put("/notices/{notice_id}")
# def update_notice(notice_id: int, notice_update: NoticeUpdate):
#     try:
#         notice = Notice.objects.get(Id=notice_id)
#     except Notice.DoesNotExist:
#         raise HTTPException(status_code=404, detail="Notice not found")
    
#     update_data = notice_update.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(notice, key, value)

#     notice.save()
#     return {"message": "Notice updated successfully"}

# @app.delete("/notices/{notice_id}")
# def delete_notice(notice_id: int):
#     try:
#         notice = Notice.objects.get(Id=notice_id)
#         notice.delete()
#         return {"message": "Notice deleted successfully"}
#     except Notice.DoesNotExist:
#         raise HTTPException(status_code=404, detail="Notice not found")

# #superuser
# @app.get("/superusers", response_class=JSONResponse)
# def view_superusers(request: Request):
#     superusers = User.objects.filter(is_superuser=True)
#     superusers_list = [{"id": user.id, "name": user.username, "email": user.email} for user in superusers]
#     return JSONResponse(content={"superusers": superusers_list})

# @app.post("/superusers", response_class=JSONResponse)
# def create_superuser(request: Request, user_create: SuperUserCreate):
#     try:
#         # Ensure the email is provided and valid
#         # Create a new superuser
#         new_user = User(
#             username=user_create.username,
#             email=user_create.email,
#             password=user_create.password,
#             is_superuser=True,
#             is_staff=True
#         )
#         print(user_create.username)
#         print(user_create.email)
#         if not user_create.email:
#             raise ValueError("Email is required")
#         new_user.set_password(user_create.password)  # Use set_password to hash the password
#         new_user.save()  # Save the new user to the database
        
#         return {"message": "Superuser created successfully"}
#     except ValidationError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except ValueError as e:
#         raise HTTPException(status_code=400, detail=str(e))
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

# @app.delete("/superusers/{user_id}")
# def delete_superuser(user_id: str):
#     try:
#         user = User.objects.get(id=user_id, is_superuser=True)
#         user.delete()
#         return {"message": "Superuser deleted successfully"}
#     except User.DoesNotExist:
#         raise HTTPException(status_code=404, detail="Superuser not found")

# # Manager
# @app.get("/managers", response_class=JSONResponse)
# def view_all_managers(request: Request):
#     managers = Manager.objects.all()
#     # managers_list = [{"id": manager.mID, "name": manager.firstName} for manager in managers]
#     return templates.TemplateResponse("admin/all_man.html", {"request": request, "managers": managers})

# @app.post("/managers/")
# def create_manager(
#     mID: str = Form(...),
#     firstName: str = Form(...),
#     middleName: Optional[str] = Form(None),
#     lastName: str = Form(...),
#     phoneNo: str = Form(...),
#     email: str = Form(...),
#     addharNo: str = Form(...),
#     dOB: str = Form(...),
#     salary: float = Form(...),
#     joinDate: str = Form(...)
# ):
#     try:
#         new_manager = Manager(
#             mID=mID,
#             firstName=firstName,
#             middleName=middleName,
#             lastName=lastName,
#             phoneNo=phoneNo,
#             email=email,
#             addharNo=addharNo,
#             dOB=dOB,
#             salary=salary,
#             joinDate=joinDate
#         )
#         new_manager.save()
#         return RedirectResponse(url="/managers", status_code=303)
#     except ValidationError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.delete("/managers/{manager_id}")
# def delete_manager(manager_id: str):
#     try:
#         manager = Manager.objects.get(mID=manager_id)
#         manager.delete()
#         return {"message": "Manager deleted successfully"}
#     except Manager.DoesNotExist:
#         raise HTTPException(status_code=404, detail="Manager not found")

# @app.put("/managers/{manager_id}")
# def update_manager(manager_id: str, manager_update: ManagerUpdate):
#     try:
#         manager = Manager.objects.get(mID=manager_id)
#     except Manager.DoesNotExist:
#         raise HTTPException(status_code=404, detail="Manager not found")
    
#     update_data = manager_update.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(manager, key, value)

#     manager.save()
#     return {"message": "Manager updated successfully"}


# # employee
# @app.get("/employees", response_class=JSONResponse)
# def view_all_employees(request: Request):
#     employees = Employee.objects.all()
#     # employees_list = [{"id": employee.eID, "name": employee.firstName} for employee in employees]
#     return templates.TemplateResponse("admin/all_emp.html", {"request": request, "employees": employees})

# @app.post("/employees/")
# def create_employee(employee: EmployeeCreate):
#     try:
#         new_employee = Employee(
#             eID=employee.eID,
#             firstName=employee.firstName,
#             middleName=employee.middleName,
#             lastName=employee.lastName,
#             phoneNo=employee.phoneNo,
#             email=employee.email,
#             addharNo=employee.addharNo,
#             dOB=employee.dOB,
#             salary=employee.salary,
#             joinDate=employee.joinDate,
#             skills=employee.skills,
#             manager_id=employee.manager_id,
#             availability=employee.availability,
#         )
#         new_employee.save()
#         return {"message": "Employee created successfully"}
#     except ValidationError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.delete("/employees/{employee_id}")
# def delete_employee(employee_id: str):
#     try:
#         employee = Employee.objects.get(eID=employee_id)
#         employee.delete()
#         return {"message": "Employee deleted successfully"}
#     except Employee.DoesNotExist:
#         raise HTTPException(status_code=404, detail="Employee not found")

# @app.put("/employees/{employee_id}")
# def update_employee(employee_id: str, employee_update: EmployeeUpdate):
#     try:
#         employee = Employee.objects.get(Id=employee_id)
#     except Employee.DoesNotExist:
#         raise HTTPException(status_code=404, detail="Employee not found")
    
#     update_data = employee_update.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(employee, key, value)

#     employee.save()
#     return {"message": "Employee updated successfully"}

# @app.put("/employees/{employee_id}/skills", response_class=JSONResponse)
# def update_employee_skills(employee_id: str, skills_update: EmployeeSkillsUpdate):
#     try:
#         employee = Employee.objects.get(id=employee_id)
#     except Employee.DoesNotExist:
#         raise HTTPException(status_code=404, detail="Employee not found")

#     employee.skills = skills_update.skills
#     employee.save()
#     return {"message": "Employee skills updated successfully"}

# # project
# @app.get("/projects", response_class=JSONResponse)
# def view_all_projects(request: Request):
#     projects = Project.objects.all()
#     # projects_list = [{"id": project.id, "name": project.name} for project in projects]
#     return templates.TemplateResponse("admin/all_pro.html", {"request": request, "projects": projects})

# @app.post("/projects/")
# def create_project(project: ProjectCreate):
#     try:
#         new_project = Project(
#             id=project.id,
#             name=project.name,
#             description=project.description,
#             start_date=(project.start_date),
#             end_date=(project.end_date),
#             project_manager_id=project.project_manager_id,
#             tasker_id=project.tasker_id,
#         )
#         new_project.save()
#         return {"message": "Project created successfully"}
#     except ValidationError as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
# @app.delete("/projects/{project_id}")
# def delete_project(project_id: str):
#     try:
#         project = Project.objects.get(id=project_id)
#         project.delete()
#         return {"message": "Project deleted successfully"}
#     except Project.DoesNotExist:
#         raise HTTPException(status_code=404, detail="Project not found")

# @app.patch("/projects/{project_id}")
# def update_project(project_id: str, project_update: ProjectUpdate):
#     try:
#         project = Project.objects.get(Id=project_id)
#     except Project.DoesNotExist:
#         raise HTTPException(status_code=404, detail="Project not found")
    
#     update_data = project_update.dict(exclude_unset=True)
#     for key, value in update_data.items():
#         setattr(project, key, value)

#     project.save()
#     return {"message": "Project updated successfully"}

# @app.get("/projects/{project_id}")
# def get_project(project_id: str):
#     projects = Project.objects.all()
#     for project in projects:
#         if project.id == project_id:
#             return project
#     raise HTTPException(status_code=404, detail="Project not found")


#features
@app.put("/projects/{project_id}/assign-employees", response_model=None)
def assign_employees_to_project(project_id: int, employee_id: int, db: Session = Depends(get_db)):
    project = Project.objects.get(id = project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")


    # for emp_id in employee_ids:
    employee = Users.objects.get(user_id = employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with id {employee_id} not found")

    # Check if employee is already assigned to another project
    if employee.availability == 'assigned' and project.tasker != employee:
        raise HTTPException(status_code=400, detail=f"Employee {employee_id} is already assigned to another project")

    # Assign employee to the project
    employee.availability = 'assigned'
    project.tasker = employee

    employee.save()
    project.save()
    return {"message": "Project assigned successfully"}

@app.put("/projects/{project_id}/unassign-employee/{employee_id}", response_model=None)
def unassign_employee_from_project(project_id: int, employee_id: int, db: Session = Depends(get_db)):
    project = Project.objects.get(id = project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    employee = Users.objects.get(user_id = employee_id )
    if not employee:
        raise HTTPException(status_code=404, detail=f"Employee with id {employee_id} not found")

    # Check if the employee is assigned to the project
    if employee.availability != 'unassigned' and project.tasker != employee:
        raise HTTPException(status_code=400, detail=f"Employee {employee_id} is not assigned to project {project_id}")

    # Unassign employee from the project
    employee.availability = 'unassigned'
    project.tasker = None

    employee.save()
    project.save()
    return project


# # requests
@app.get("/requests", response_class=JSONResponse)
def view_all_requests(request: Request):
    requests = Requests.objects.all()
    requests_list = [{"id": req.id, "description": req.message, "status":req.status, "project": req.project.name, "manager":req.manager.user_id } for req in requests]
    return JSONResponse(content={"requests": requests_list})

# @app.get("/requests/{request_id}", response_class=JSONResponse)
# def view_requests(request: Request,request_id: int):
#     requests = Requests.objects.get(id=request_id)
#     # requests_list = [{"id": req.id, "description": req.message, "status":req.status, "project": req.project.name, "manager":req.manager.user_id } for req in requests]
#     return JSONResponse(content={"requests": requests})

@app.post("/requests/")
def create_request(request: RequestsCreate):
    try:
        new_request = Requests(
            manager_id=request.manager_id,
            project_id=request.project_id,
            message=request.message,
            created_at=request.created_at,
            status=request.status,
            comment=request.comment,
        )
        new_request.save()
        for employee_id in request.employee_ids:
            new_request.employees.add(Users.objects.get(user_id=employee_id))
        new_request.save()
        return {"message": "Request created successfully"}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/requests/{request_id}")
def delete_request(request_id: int):
    try:
        request = Requests.objects.get(id=request_id)
        request.delete()
        return {"message": "Request deleted successfully"}
    except Requests.DoesNotExist:
        raise HTTPException(status_code=404, detail="Request not found")

@app.put("/requests/{request_id}")
def update_request(request_id: int, request_update: RequestsUpdate):
    try:
        request = Requests.objects.get(id=request_id)
    except Requests.DoesNotExist:
        raise HTTPException(status_code=404, detail="Request not found")
    
    update_data = request_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(request, key, value)

    request.save()
    return {"message": "Request updated successfully"}


# #leave request
# @app.get("/leave_requests", response_class=JSONResponse)
# def view_all_leave_requests(request: Request):
#     employee_leaves = EmployeeLeaveApplication.objects.all()
#     manager_leaves = ManagerLeaveApplication.objects.all()
#     return templates.TemplateResponse("admin/all_leave.html", {"request": request, "employee_leaves": employee_leaves, "manager_leaves": manager_leaves})

# def validate_and_parse_date(date_str):
#     parsed_date = parse_date(date_str)
#     if not parsed_date:
#         raise ValidationError(f"Invalid date format: {date_str}")
#     return parsed_date

# def validate_and_parse_datetime(datetime_str):
#     parsed_datetime = parse_datetime(datetime_str)
#     if not parsed_datetime:
#         raise ValidationError(f"Invalid datetime format: {datetime_str}")
#     return parsed_datetime

# #emp leave
# @app.post("/employee_leave_applications/")
# def create_employee_leave_application(application: EmployeeLeaveApplicationCreate):
#     try:
#         new_application = EmployeeLeaveApplication(
#             employee_id=application.employee_id,
#             start_date=application.start_date,
#             end_date=application.end_date,
#             reason=application.reason,
#             status=application.status,
#         )
#         new_application.save()
#         return {"message": "Employee leave application created successfully"}
#     except ValidationError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.delete("/employee_leave_applications/{application_id}")
# def delete_employee_leave_application(application_id: int):
#     try:
#         application = EmployeeLeaveApplication.objects.get(id=application_id)
#         application.delete()
#         return {"message": "Employee leave application deleted successfully"}
#     except EmployeeLeaveApplication.DoesNotExist:
#         raise HTTPException(status_code=404, detail="Employee leave application not found")

# @app.post("/leave_requests/employee/{leave_id}/status")
# def update_employee_leave_status(leave_id: int, status_update: StatusUpdate, db: Session = Depends(get_db)):
#     leave = EmployeeLeaveApplication.objects.get(id = leave_id)
#     print(leave)
#     if not leave:
#         raise HTTPException(status_code=404, detail="Employee leave request not found")
#     leave.status = status_update.status
#     print(leave.status)
#     leave.save()
#     return {"message": "Status updated successfully"}


# #manager leave
# @app.post("/manager_leave_applications/")
# def create_manager_leave_application(application: ManagerLeaveApplicationCreate):
#     try:
#         new_application = ManagerLeaveApplication(
#             manager_id=application.manager_id,
#             start_date=application.start_date,
#             end_date=application.end_date,
#             reason=application.reason,
#             status=application.status,
#         )
#         new_application.save()
#         return {"message": "Manager leave application created successfully"}
#     except ValidationError as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.delete("/manager_leave_applications/{application_id}")
# def delete_manager_leave_application(application_id: int):
#     try:
#         application = ManagerLeaveApplication.objects.get(id=application_id)
#         application.delete()
#         return {"message": "Manager leave application deleted successfully"}
#     except ManagerLeaveApplication.DoesNotExist:
#         raise HTTPException(status_code=404, detail="Manager leave application not found")
    
# @app.post("/leave_requests/manager/{leave_id}/status")
# def update_manager_leave_status(leave_id: int, status_update: StatusUpdate):
#     leave = ManagerLeaveApplication.objects.get(id = leave_id)
#     # print(leave)
#     if not leave:
#         raise HTTPException(status_code=404, detail="Employee leave request not found")
#     leave.status = status_update.status
#     # print(leave.status)
#     leave.save()
#     return {"message": "Status updated successfully"}



@app.post("/notices", response_class=JSONResponse)
def create_notice(request: Request, notice_create: NoticeCreate):
    try:
        new_notice = Notice(
            title=notice_create.title,
            description=notice_create.description,
            publishDate=notice_create.publishDate,
        )
        new_notice.save()
        return JSONResponse(content={"message": "Notice created successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/notices", response_class=JSONResponse)
def get_notices(request: Request):
    notices = Notice.objects.all()
    notices_list = [{"id": notice.Id, "title": notice.title, "description": notice.description,"Publish date":notice.publishDate} for notice in notices]
    return JSONResponse(content={"notices": notices_list})

@app.get("/notices/{notice_id}", response_class=JSONResponse)
def get_notice(notice_id: int):
    try:
        notice = Notice.objects.get(Id=notice_id)
        notice_data = {"id": notice.Id, "title": notice.title, "description": notice.description, "Publish date":notice.publishDate}
        return JSONResponse(content={"notice": notice_data})
    except Notice.DoesNotExist:
        raise HTTPException(status_code=404, detail="Notice not found")

@app.put("/notices/{notice_id}", response_class=JSONResponse)
def update_notice(notice_id: int, notice_update: NoticeCreate):
    try:
        notice = Notice.objects.get(Id=notice_id)
        notice.title = notice_update.title
        notice.description = notice_update.description
        notice.publishDate = notice_update.publishDate
        notice.save()
        return JSONResponse(content={"message": "Notice updated successfully"})
    except Notice.DoesNotExist:
        raise HTTPException(status_code=404, detail="Notice not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/notices/{notice_id}", response_class=JSONResponse)
def delete_notice(notice_id: int):
    try:
        notice = Notice.objects.get(Id=notice_id)
        notice.delete()
        return JSONResponse(content={"message": "Notice deleted successfully"})
    except Notice.DoesNotExist:
        raise HTTPException(status_code=404, detail="Notice not found")


#Project
def serialize_project(project):
    return {
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "start_date": project.start_date.isoformat(),
        "end_date": project.end_date.isoformat(),
        "project_manager": {
            "id": project.project_manager.user_id,
            "firstName": project.project_manager.firstName,
            "lastName": project.project_manager.lastName,
            "email": project.project_manager.email,
        } if project.project_manager else None,
        "tasker": {
            "id": project.tasker.user_id,
            "firstName": project.tasker.firstName,
            "lastName": project.tasker.lastName,
            "email": project.tasker.email,
        } if project.tasker else None,
    }


# Create a new project
@app.post("/projects", response_class=JSONResponse)
def create_project(request: ProjectCreate):
    try:
        project_manager = None
        tasker = None
        
        if request.project_manager is not None:
            project_manager = get_object_or_404(Users, pk=request.project_manager)
        
        if request.tasker is not None:
            tasker = get_object_or_404(Users, pk=request.tasker)
        
        new_project = Project(
            name=request.name,
            description=request.description,
            start_date=request.start_date,
            end_date=request.end_date,
            project_manager=project_manager,
            tasker=tasker
        )
        new_project.save()
        return JSONResponse(content={"message": "Project created successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Update an existing project
@app.put("/projects/{project_id}", response_class=JSONResponse)
def update_project(project_id: int, request: ProjectUpdate):
    try:
        project = get_object_or_404(Project, pk=project_id)
        
        if request.project_manager is not None:
            project_manager = get_object_or_404(Users, pk=request.project_manager)
            project.project_manager = project_manager
        
        if request.tasker is not None:
            tasker = get_object_or_404(Users, pk=request.tasker)
            project.tasker = tasker
        
        if request.name is not None:
            project.name = request.name
        if request.description is not None:
            project.description = request.description
        if request.start_date is not None:
            project.start_date = request.start_date
        if request.end_date is not None:
            project.end_date = request.end_date
        
        project.save()
        return JSONResponse(content={"message": "Project updated successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    

# Retrieve all projects
@app.get("/projects", response_class=JSONResponse)
def get_projects():
    projects = Project.objects.all()
    projects_list = [serialize_project(project) for project in projects]
    return JSONResponse(content={"projects": projects_list})

# Retrieve a specific project
@app.get("/projects/{project_id}", response_class=JSONResponse)
def get_project(project_id: int):
    project = get_object_or_404(Project, pk=project_id)
    project_data = serialize_project(project)
    return JSONResponse(content={"project": project_data})


@app.delete("/projects/{project_id}", response_class=JSONResponse)
def delete_project(project_id: int):
    try:
        project = Project.objects.get(id=project_id)
        project.delete()
        return JSONResponse(content={"message": "Project deleted successfully"})
    except Project.DoesNotExist:
        raise HTTPException(status_code=404, detail="Project not found")


# Users
@app.post("/users", response_class=JSONResponse)
def create_user(request: Request, user_create: UserCreate):
    try:
        new_user = Users(
            firstName=user_create.firstName,
            lastName=user_create.lastName,
            email=user_create.email,
            password=user_create.password,  # Password should be hashed in production
            skills=user_create.skills,
            availability=user_create.availability,
            role=user_create.role,
        )
        new_user.save()
        return JSONResponse(content={"message": "User created successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/users", response_class=JSONResponse)
def get_users(request: Request):
    users = Users.objects.all()
    users_list = [{"id": user.user_id, "firstName": user.firstName, "lastName": user.lastName, "email": user.email,"role":user.role, "Availability":user.availability, 'Skills':user.skills} for user in users]
    return JSONResponse(content={"users": users_list})

@app.get("/users/{user_id}", response_class=JSONResponse)
def get_user(user_id: int):
    try:
        user = Users.objects.get(user_id=user_id)
        user_data = {"id": user.user_id, "firstName": user.firstName, "lastName": user.lastName, "email": user.email,"role":user.role, "Availability":user.availability, 'Skills':user.skills}
        return JSONResponse(content={"user": user_data})
    except Users.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_class=JSONResponse)
def update_user(user_id: int, user_update: UserCreate):
    try:
        user = Users.objects.get(user_id=user_id)
        user.firstName = user_update.firstName
        user.lastName = user_update.lastName
        user.email = user_update.email
        user.password = user_update.password  # Password should be hashed in production
        user.skills = user_update.skills
        user.availability = user_update.availability
        user.role = user_update.role
        user.save()
        return JSONResponse(content={"message": "User updated successfully"})
    except Users.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.delete("/users/{user_id}", response_class=JSONResponse)
def delete_user(user_id: int):
    try:
        user = Users.objects.get(user_id=user_id)
        user.delete()
        return JSONResponse(content={"message": "User deleted successfully"})
    except Users.DoesNotExist:
        raise HTTPException(status_code=404, detail="User not found")



def serialize_request(request):
    return {
        "id": request.id,
        "manager": {
            "id": request.manager.user_id,
            "firstName": request.manager.firstName,
            "lastName": request.manager.lastName,
            "email": request.manager.email,
        } if request.manager else None,
        "project": {
            "id": request.project.id,
            "name": request.project.name,
        } if request.project else None,
        "message": request.message,
        "created_at": request.created_at.isoformat(),
        "status": request.status,
        "comment": request.comment,
        "employees": [{
            "id": employee.user_id,
            "firstName": employee.firstName,
            "lastName": employee.lastName,
            "email": employee.email,
        } for employee in request.employees]
    }

def serialize_employee_leave_application(leave_application):
    return {
        "id": leave_application.Id,
        "employee": {
            "id": leave_application.employee.user_id,
            "firstName": leave_application.employee.firstName,
            "lastName": leave_application.employee.lastName,
            "email": leave_application.employee.email,
        } if leave_application.employee else None,
        "start_date": leave_application.start_date.isoformat(),
        "end_date": leave_application.end_date.isoformat(),
        "reason": leave_application.reason,
        "status": leave_application.status,
    }

def serialize_manager_leave_application(leave_application):
    return {
        "id": leave_application.Id,
        "manager": {
            "id": leave_application.manager.user_id,
            "firstName": leave_application.manager.firstName,
            "lastName": leave_application.manager.lastName,
            "email": leave_application.manager.email,
        } if leave_application.manager else None,
        "start_date": leave_application.start_date.isoformat(),
        "end_date": leave_application.end_date.isoformat(),
        "reason": leave_application.reason,
        "status": leave_application.status,
    }

#requests

# # Retrieve all requests
# @app.get("/requests", response_class=JSONResponse)
# def get_requests():
#     requests = Requests.objects.all()
#     requests_list = [serialize_request(request) for request in requests]
#     return JSONResponse(content={"requests": requests_list})

# # Retrieve a specific request
# @app.get("/requests/{request_id}", response_class=JSONResponse)
# def get_request(request_id: int):
#     request = get_object_or_404(Requests, pk=request_id)
#     request_data = {
#         "id": request.id,
#         "manager_id": request.manager.user_id,
#         "project_id": request.project.id,
#         "employee_ids": [emp.user_id for emp in request.employees.all()],
#         "message": request.message,
#         "created_at": request.created_at,
#         "status": request.status,
#         "comment": request.comment
#     }
#     return JSONResponse(content={"request": request_data})

# Create a new request
# @app.post("/requests", response_class=JSONResponse)
# def create_request(request_data: RequestsCreate):
#     try:
#         manager = get_object_or_404(Users, pk=request_data.manager_id)
#         project = get_object_or_404(Project, pk=request_data.project_id)
#         employees = [get_object_or_404(Users, pk=emp_id) for emp_id in request_data.employee_ids]

#         new_request = Requests(
#             manager=manager,
#             project=project,
#             message=request_data.message,
#             created_at=request_data.created_at,
#             status=request_data.status,
#             comment=request_data.comment,
#         )
#         new_request.save()
#         new_request.employees.set(employees)
#         return JSONResponse(content={"message": "Request created successfully"})
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # Update an existing request
# @app.put("/requests/{request_id}", response_class=JSONResponse)
# def update_request(request_id: int, request_data: RequestsUpdate):
#     try:
#         request = get_object_or_404(Requests, pk=request_id)

#         if request_data.manager_id:
#             manager = get_object_or_404(Users, pk=request_data.manager_id)
#             request.manager = manager

#         if request_data.project_id:
#             project = get_object_or_404(Project, pk=request_data.project_id)
#             request.project = project

#         if request_data.employee_ids:
#             employees = [get_object_or_404(Users, pk=emp_id) for emp_id in request_data.employee_ids]
#             request.employees.set(employees)

#         request.message = request_data.message or request.message
#         request.created_at = request_data.created_at or request.created_at
#         request.status = request_data.status or request.status
#         request.comment = request_data.comment or request.comment
        
#         request.save()
#         return JSONResponse(content={"message": "Request updated successfully"})
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


# Retrieve all employee leave applications
@app.get("/employee_leave_applications", response_class=JSONResponse)
def get_employee_leave_applications():
    leave_applications = EmployeeLeaveApplication.objects.all()
    leave_applications_list = [serialize_employee_leave_application(app) for app in leave_applications]
    return JSONResponse(content={"employee_leave_applications": leave_applications_list})

# Retrieve a specific employee leave application
@app.get("/employee_leave_applications/{application_id}", response_class=JSONResponse)
def get_employee_leave_application(application_id: int):
    leave_application = get_object_or_404(EmployeeLeaveApplication, pk=application_id)
    leave_application_data = serialize_employee_leave_application(leave_application)
    return JSONResponse(content={"employee_leave_application": leave_application_data})

# Create a new employee leave application
@app.post("/employee_leave_applications", response_class=JSONResponse)
def create_employee_leave_application(application_data: EmployeeLeaveApplicationCreate):
    try:
        employee = get_object_or_404(Users, pk=application_data.employee_id)

        new_leave_application = EmployeeLeaveApplication(
            employee=employee,
            start_date=application_data.start_date,
            end_date=application_data.end_date,
            reason=application_data.reason,
            status=application_data.status,
        )

        new_leave_application.save()
        return JSONResponse(content={"message": "Employee leave application created successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Update an existing employee leave application
@app.put("/employee_leave_applications/{application_id}", response_class=JSONResponse)
def update_employee_leave_application(application_id: int, application_data: EmployeeLeaveApplicationUpdate):
    try:
        leave_application = get_object_or_404(EmployeeLeaveApplication, pk=application_id)

        if application_data.employee_id:
            employee = get_object_or_404(Users, pk=application_data.employee_id)
            leave_application.employee = employee

        leave_application.start_date = application_data.start_date or leave_application.start_date
        leave_application.end_date = application_data.end_date or leave_application.end_date
        leave_application.reason = application_data.reason or leave_application.reason
        leave_application.status = application_data.status or leave_application.status

        leave_application.save()
        return JSONResponse(content={"message": "Employee leave application updated successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.delete("/employee_leave_applications/{application_id}", response_class=JSONResponse)
def delete_employee_leave_application(application_id: int):
    try:
        leave_application = get_object_or_404(EmployeeLeaveApplication, pk=application_id)
        leave_application.delete()
        return JSONResponse(content={"message": "Employee leave application deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


#Manager
# Retrieve all employee leave applications
@app.get("/manager_leave_applications", response_class=JSONResponse)
def get_manager_leave_applications():
    leave_applications = ManagerLeaveApplication.objects.all()
    leave_applications_list = [serialize_manager_leave_application(app) for app in leave_applications]
    return JSONResponse(content={"manager_leave_applications": leave_applications_list})

# Retrieve a specific employee leave application
@app.get("/manager_leave_applications/{application_id}", response_class=JSONResponse)
def get_manager_leave_application(application_id: int):
    leave_application = get_object_or_404(ManagerLeaveApplication, pk=application_id)
    leave_application_data = serialize_manager_leave_application(leave_application)
    return JSONResponse(content={"manager_leave_applications": leave_application_data})

# Create a new employee leave application
@app.post("/manager_leave_applications", response_class=JSONResponse)
def create_manager_leave_application(application_data: ManagerLeaveApplicationCreate):
    try:
        employee = get_object_or_404(Users, pk=application_data.manager_id)

        new_leave_application = ManagerLeaveApplication(
            manager=employee,
            start_date=application_data.start_date,
            end_date=application_data.end_date,
            reason=application_data.reason,
            status=application_data.status,
        )
        new_leave_application.save()
        return JSONResponse(content={"message": "Manager leave application created successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Update an existing employee leave application
@app.put("/manager_leave_applications/{application_id}", response_class=JSONResponse)
def update_manager_leave_application(application_id: int, application_data: ManagerLeaveApplicationUpdate):
    try:
        leave_application = get_object_or_404(ManagerLeaveApplication, pk=application_id)

        if application_data.manager_id:
            employee = get_object_or_404(Users, pk=application_data.manager_id)
            leave_application.manager = employee

        leave_application.start_date = application_data.start_date or leave_application.start_date
        leave_application.end_date = application_data.end_date or leave_application.end_date
        leave_application.reason = application_data.reason or leave_application.reason
        leave_application.status = application_data.status or leave_application.status

        leave_application.save()
        return JSONResponse(content={"message": "Manager leave application updated successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/manager_leave_applications/{application_id}", response_class=JSONResponse)
def delete_manager_leave_application(application_id: int):
    try:
        leave_application = get_object_or_404(ManagerLeaveApplication, pk=application_id)
        leave_application.delete()
        return JSONResponse(content={"message": "Manager leave application deleted successfully"})
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Employee Management System - Django(Python)

Employee Management System built in a Python Framework Django and PostgreSQL as Database. The project aims to develop a comprehensive Employee Management System with three types of users: Admin, Employee, and Manager. The system will facilitate the process of leave application and approval, project assignment, and employee management, ensuring efficient and transparent operations within the organization.

## Architechture Diagram

<img width="600" alt="image" src="https://github.com/0904-mansi/Capstone-Project/assets/81081105/7a5c93e8-1e43-4d1d-bb86-b22c303b52f7">


## Admin
Admins have comprehensive access to the system's functionalities, enabling them to manage users, projects, and resources effectively. Admins oversee the entire system, managing employees, managers, attendance, leave applications, notices and projects. They can assign/unassign projects, approve/reject resource requests, and update or delete employee details. 

### Functional Requirements:

- Add New Employees/Managers and Projects
- View All Employees and Projects
- Assign/Unassign Projects to Employees
- Approve/Reject Managers’ Requests for Resources
- Delete Employees/Managers/projects
- Update Employee/Manager/projects Details
- Add/delete/update Attendance/Notices
- Approve/Reject Leave Requests

### Admin Actions

<img width="400" alt="image" src="https://github.com/0904-mansi/Capstone-Project/assets/81081105/2bfb5917-4b58-4d0d-a853-6078e4721519">


## Manager (Admin Subtype)
Managers have access to specific functionalities that assist in managing projects and requesting resources. Managers oversee multiple projects and have the ability to view all employees, managers, and projects. They can filter employees by skills and availability and request unassigned employees from admins for their projects. 


### Functional Requirements:

- View All Employees, Managers, and Projects
- Filter Employees by Skills and Unassigned Status
- Request Employees for Projects
- Request Multiple Employees for a Project
- View Attendance/Notices
- Raise Leave Requests

### Manager Actions
<img width="400" alt="image" src="https://github.com/0904-mansi/Capstone-Project/assets/81081105/05323d33-1f2d-42a0-8cb4-d0b60ac993d1">


## Employee
Employees have limited access to the system, focusing on updating personal information and viewing relevant details. Employees are key project contributors with limited access. They can update skills, raise request for leave, view their project and manager information, and see all other employees and managers. 


### Functional Requirements:

- View Profile Information
- Update New Skills
- View All Employees (Including Managers)
- View Attendance/Notices 
- Raise Leave Requests

### Employee Actions
<img width="400" alt="image" src="https://github.com/0904-mansi/Capstone-Project/assets/81081105/ea075e24-70c7-46bf-98d8-f9f6d2f2008f">


## How to Use this Project?
***
- Install Python to your System.
- Run Following command to your terminal.
    ```python
    pip install django
    ```
- Install Pipenv for Virtual Environment, run the command...
    ```python
    pip install pipenv
    ```
- Clone the repository to your local system.
- Setup PostgreSQL Database and update database name and password in settings.py file in employeemanagement.
- Make the Migrations, run the command
    ```python
    python manage.py makemigrations
    ```
- Migrate the App, run the command
    ```python
    python manage.py migrate
    ```
- Finally Run the App, run the command.
    ```python
    python manage.py runserver
    ```
- Hola, It's running !!

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
- Access the application on ``http://127.0.0.1:8000/``

### Directory Structure


<details>
<summary><b>View Directory Structure</b></summary>


```
Employee-Management-System
├── accounts
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── signals.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── employee
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── empmanagement
│   ├── settings.py
│   ├── static
│   │   ├── assets
│   │   │   ├── Team.jpg
│   │   │   ├── logo.png
│   │   │   └── welcome.webp
│   │   ├── css
│   │   │   └── style.css
│   │   └── js
│   │       └── script.js
│   ├── urls.py
│   └── wsgi.py
├── logs
│   └── debug.log
├── manage.py
├── manager
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── requirements.txt
└── templates
    ├── admin
    │   ├── app_list.html
    │   ├── base.html
    │   ├── base_site.html
    │   ├── count.html
    │   ├── email.html
    │   ├── inc
    │   │   ├── branding.html
    │   │   └── title.html
    │   ├── notice.html
    │   ├── viewallemployees.html
    │   ├── viewallmanagers.html
    │   ├── viewallprojects.html
    │   └── viewallrequests.html
    ├── base.html
    ├── base2.html
    ├── employee
    │   ├── attendance.html
    │   ├── dashboard.html
    │   ├── deleterequest.html
    │   ├── empleaverequest.html
    │   ├── leaverequest.html
    │   ├── login.html
    │   ├── myproject.html
    │   ├── notice.html
    │   ├── noticedetail.html
    │   ├── projectdetails.html
    │   ├── request.html
    │   ├── requestdetails.html
    │   ├── signup.html
    │   ├── updaterequest.html
    │   ├── updateskills.html
    │   ├── viewallemployees.html
    │   ├── viewallmanagers.html
    │   └── viewleaverequest.html
    └── manager
        ├── attendance.html
        ├── leaverequest.html
        ├── leaveupdaterequest.html
        ├── login.html
        ├── m_dashboard.html
        ├── managerrequest.html
        ├── manleaverequest.html
        ├── manrequestdetails.html
        ├── mywork.html
        ├── notice.html
        ├── noticedetail.html
        ├── request.html
        ├── requestdetails.html
        ├── updaterequest.html
        ├── viewRequest.html
        ├── viewallemployees.html
        ├── viewallmanagers.html
        ├── viewallprojects.html
        ├── viewleaverequest.html
        |__ viewproject.html
```
</details>

## Unit Test Coverage of 90%

```
Name                                                                                       Stmts   Miss  Cover
--------------------------------------------------------------------------------------------------------------
accounts/__init__.py                                                                           0      0   100%
accounts/admin.py                                                                              1      0   100%
accounts/apps.py                                                                               6      0   100%
accounts/models.py                                                                             2      0   100%
accounts/signals.py                                                                           16      0   100%
accounts/tests.py                                                                            136      0   100%
accounts/urls.py                                                                               4      0   100%
accounts/views.py                                                                            139     50    64%
employee/__init__.py                                                                           0      0   100%
employee/admin.py                                                                             15      1    93%
employee/apps.py                                                                               4      0   100%
employee/forms.py                                                                             15      0   100%
employee/models.py                                                                           103      3    97%
employee/tests.py                                                                            132      0   100%
employee/urls.py                                                                               3      0   100%
employee/views.py                                                                             86     25    71%
empmanagement/__init__.py                                                                      0      0   100%
empmanagement/settings.py                                                                     30      0   100%
empmanagement/urls.py                                                                          5      0   100%
manage.py                                                                                     11      2    82%
manager/__init__.py                                                                            0      0   100%
manager/admin.py                                                                               3      0   100%
manager/apps.py                                                                                4      0   100%
manager/forms.py                                                                              17      0   100%
manager/migrations/__init__.py                                                                 0      0   100%
manager/tests.py                                                                              86      0   100%
manager/urls.py                                                                                3      0   100%
manager/views.py                                                                             149     38    74%
--------------------------------------------------------------------------------------------------------------
TOTAL                                                                                       1202    119    90%
```

## View Live Coverage Report [here](https://unit-testcoverage.static.domains/)

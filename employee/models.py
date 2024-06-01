from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from pickle import TRUE
from turtle import title
from django.db import models

months = (
    ('January','January'),
    ('February','February'),
    ('March','March'),
    ('April','April'),
    ('May','May'),
    ('June','June'),
    ('July','July'),
    ('August','August'),
    ('September','September'),
    ('October','October'),
    ('November','November'),
    ('December','December')
)
year = (('2020', '2020'), ('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'))

days = (('0','0'),('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8'),('9','9'),('10','10'),
('11','11'),('12','12'),('13','13'),('14','14'),('15','15'),('16','16'),('17','17'),('18','18'),('19','19'),('20','20'),
('21','21'),('22','22'),('23','23'),('24','24'),('25','25'),('26','26'),('27','27'),('28','28'),('29','29'),('30','30'),('31','31'))

def validate_email_domain(value):
    if not value.endswith('@domain.com'):
        raise ValidationError(
            ('%(value)s is not an email with the @domain.com domain'),
            params={'value': value},
        )

 
class Project(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default=0)
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    assigner = "Admin" #models.ForeignKey(User, on_delete=models.CASCADE, related_name="assigned_projects", default='admin')
    project_manager = models.ForeignKey('Manager', on_delete=models.CASCADE, related_name="requested_projects")
    tasker = models.ForeignKey('Employee', on_delete=models.CASCADE, related_name="tasked_projects")

    
    def __str__(self):
        return self.name
        
class Manager(models.Model):
    mID = models.CharField(primary_key=True, max_length=20)
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50,blank=True, null=True)
    lastName = models.CharField(max_length=50)
    phoneNo = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=70, unique=True, validators=[validate_email_domain])
    addharNo = models.CharField(max_length=20, unique=True)
    dOB = models.DateField()
    salary = models.CharField(max_length=20)
    joinDate = models.DateField()
    # project = models.ManyToManyField(Project)

    def __str__(self):
        return f"{self.firstName} {self.lastName} - {self.mID}"

     


class Employee(models.Model):
    __tablename__ = "employee_employee"
    AVAILABILITY_CHOICES = [
        ('assigned', 'Assigned'),
        ('unassigned', 'Unassigned'),
    ]
    eID = models.CharField(primary_key=True, max_length=20)
    firstName = models.CharField(max_length=50)
    middleName = models.CharField(max_length=50,blank=True, null=True)
    lastName = models.CharField(max_length=50)
    phoneNo = models.CharField(max_length=12, unique=True)
    email = models.EmailField(max_length=70, unique=True, validators=[validate_email_domain])
    addharNo = models.CharField(max_length=20, unique=True)
    dOB = models.DateField()
    salary = models.CharField(max_length=20)
    joinDate = models.DateField()
    skills = models.CharField(max_length=200, default = "Engineer")
    manager_id = models.ForeignKey(Manager, on_delete=models.CASCADE, db_column='mID', default=None, null=True, blank=True)      # skills = models.ManyToManyField(Skill)
    # project_id = models.ForeignKey(Project, on_delete=models.CASCADE, db_column='project_id',default=None, null=True, blank=True)
    availability = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='unassigned')
    
    def __str__(self):
        return f"{self.eID} - {self.availability}"


class Employee_Attendance(models.Model):
    eId = models.ForeignKey(Employee,on_delete=models.CASCADE)
    month = models.CharField(max_length=50,choices=months)
    year = models.CharField(max_length=4, choices=year,default='2024')
    days = models.CharField(max_length=5,choices=days)

    def __str__(self):
        return "%s %s" % (self.eId, self.month)
    
class Manager_Attendance(models.Model):
    mId = models.ForeignKey(Manager,on_delete=models.CASCADE)
    month = models.CharField(max_length=50,choices=months)
    year = models.CharField(max_length=4, choices=year,default='2024')
    days = models.CharField(max_length=5,choices=days)

    def __str__(self):
        return "%s %s" % (self.mId, self.month)


class Notice(models.Model):
    Id = models.CharField(primary_key=True,max_length=20)
    title = models.CharField(max_length=250)
    description = models.TextField()
    publishDate = models.DateTimeField()

    def __str__(self):
        return self.title 
 

class Request(models.Model):
    # rID = models.CharField(max_length=20, primary_key=True, default=0)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    employees = models.ManyToManyField(Employee, related_name='requests')
    message = models.TextField()
    created_at = models.DateTimeField()
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')

    def __str__(self):
        return f"Request from {self.manager.firstName} for {self.project.name}"


class EmployeeLeaveApplication(models.Model):
    LEAVE_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=LEAVE_STATUS_CHOICES, default='Pending')
    
    def __str__(self):
        return f'{self.employee.eID} - ({self.start_date} to {self.end_date})'

    

class ManagerLeaveApplication(models.Model):
    LEAVE_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=LEAVE_STATUS_CHOICES, default='Pending')
    
    def __str__(self):
        return f'{self.manager.mID} - ({self.start_date} to {self.end_date})'

    
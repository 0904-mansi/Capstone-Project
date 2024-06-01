from django.test import TestCase
from django.contrib.auth.models import User
from .models import *
from django.contrib.messages import get_messages
from django.urls import reverse
from django.test import TestCase, Client
from django.utils import timezone
from datetime import date, timedelta
from django.core.mail import send_mail
from django.contrib.admin.sites import AdminSite
from .admin import RequestAdmin
class TestEmailDomainValidator(TestCase):
    def test_valid_email(self):
        # Valid email with the correct domain
        valid_email = 'test@domain.com'
        self.assertIsNone(validate_email_domain(valid_email))  # Should not raise ValidationError

    def test_invalid_email(self):
        # Invalid email with a different domain
        invalid_email = 'test@example.com'
        with self.assertRaises(ValidationError) as cm:
            validate_email_domain(invalid_email)
        self.assertEqual(cm.exception.message, '%(value)s is not an email with the @domain.com domain')

        # Another invalid email with no domain
        invalid_email_no_domain = 'test'
        with self.assertRaises(ValidationError) as cm:
            validate_email_domain(invalid_email_no_domain)
        self.assertEqual(cm.exception.message, '%(value)s is not an email with the @domain.com domain')

    def test_blank_email(self):
        # Blank email
        blank_email = ''
        with self.assertRaises(ValidationError) as cm:
            validate_email_domain(blank_email)
        self.assertEqual(cm.exception.message, '%(value)s is not an email with the @domain.com domain')


class ModelsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')


        # Create Manager instance
        self.manager = Manager.objects.create(
            mID='MGR001',
            firstName='John',
            middleName='A',
            lastName='Doe',
            phoneNo='1234567890',
            email='john.doe@example.com',
            addharNo='1234-5678-9012',
            dOB='1980-01-01',
            salary='100000',
            joinDate='2020-01-01'
        )

        # Create Employee instance
        self.employee = Employee.objects.create(
            eID='EMP001',
            firstName='Jane',
            middleName='B',
            lastName='Smith',
            phoneNo='0987654321',
            email='jane.smith@example.com',
            addharNo='9012-3456-7890',
            dOB='1990-01-01',
            salary='50000',
            joinDate='2021-01-01',
            manager_id=self.manager
        )

        # Create Project instance
        self.project = Project.objects.create(
            id='PRJ001',
            name='Project X',
            description='A top secret project.',
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=10),
            project_manager=self.manager,
            tasker=self.employee
        )

    def test_create_manager(self):
        manager_count = Manager.objects.count()
        self.assertEqual(manager_count, 1)
        self.assertEqual(self.manager.firstName, 'John')

    def test_create_employee(self):
        employee_count = Employee.objects.count()
        self.assertEqual(employee_count, 1)
        self.assertEqual(self.employee.firstName, 'Jane')
        self.assertEqual(self.employee.manager_id, self.manager)

    def test_create_project(self):
        project_count = Project.objects.count()
        self.assertEqual(project_count, 1)
        self.assertEqual(self.project.name, 'Project X')
        self.assertEqual(self.project.project_manager, self.manager)
        self.assertEqual(self.project.tasker, self.employee)

    def test_employee_attendance(self):
        attendance = Employee_Attendance.objects.create(
            eId=self.employee,
            month='January',
            year='2024',
            days='20'
        )
        self.assertEqual(attendance.eId, self.employee)
        self.assertEqual(attendance.month, 'January')

    def test_manager_attendance(self):
        attendance = Manager_Attendance.objects.create(
            mId=self.manager,
            month='January',
            year='2024',
            days='22'
        )
        self.assertEqual(attendance.mId, self.manager)
        self.assertEqual(attendance.month, 'January')

    def test_notice(self):
        notice = Notice.objects.create(
            Id='N001',
            title='Meeting Notice',
            description='There will be a meeting tomorrow.',
            publishDate=timezone.now()
        )
        self.assertEqual(notice.title, 'Meeting Notice')

    def test_request(self):
        request = Request.objects.create(
            manager=self.manager,
            project=self.project,
            message='Need more resources.',
            created_at=timezone.now(),
            status='Pending'
        )
        request.employees.add(self.employee)
        self.assertEqual(request.manager, self.manager)
        self.assertEqual(request.project, self.project)
        self.assertIn(self.employee, request.employees.all())

    def test_employee_leave_application(self):
        leave_application = EmployeeLeaveApplication.objects.create(
            employee=self.employee,
            start_date='2023-06-01',
            end_date='2023-06-10',
            reason='Vacation',
            status='Pending'
        )
        self.assertEqual(leave_application.employee, self.employee)
        self.assertEqual(leave_application.status, 'Pending')

    def test_manager_leave_application(self):
        leave_application = ManagerLeaveApplication.objects.create(
            manager=self.manager,
            start_date='2023-07-01',
            end_date='2023-07-10',
            reason='Medical',
            status='Pending'
        )
        self.assertEqual(leave_application.manager, self.manager)
        self.assertEqual(leave_application.status, 'Pending')


   
    



class ViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        
        self.employee = Employee.objects.create(
            eID='testuser',
            firstName='Test',
            middleName='User',
            lastName='Example',
            phoneNo='1234567890',
            email='testuser@example.com',
            addharNo='123456789012',
            dOB='1990-01-01',
            salary='50000',
            joinDate='2020-01-01'
        )

        self.manager = Manager.objects.create(
            mID='M001',
            firstName='Manager',
            middleName='Middle',
            lastName='Name',
            phoneNo='0987654321',
            email='manager@example.com',
            addharNo='098765432109',
            dOB='1985-01-01',
            salary='70000',
            joinDate='2015-01-01'
        )

        self.project = Project.objects.create(
            id='P001',
            name='Project A',
            description='Description A',
            start_date='2023-01-01T00:00:00Z',
            end_date='2023-12-31T00:00:00Z',
            project_manager=self.manager,
            tasker=self.employee
        )

        self.notice = Notice.objects.create(
            Id='N001',
            title='Notice Title',
            description='Notice Description',
            publishDate='2023-01-01T00:00:00Z'
        )

        self.request = Request.objects.create(
            manager=self.manager,
            project=self.project,
            message='Request Message',
            created_at='2023-01-01T00:00:00Z',
            status='Pending'
        )
        self.request.employees.add(self.employee)

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'employee/dashboard.html')

    def test_updateskills_view(self):
        response = self.client.post(reverse('updateskills'), {'skills': 'Django'})
        self.assertEqual(response.status_code, 302)
        self.employee.refresh_from_db()
        self.assertEqual(self.employee.skills, 'Django')

    def test_attendance_view(self):
        response = self.client.get(reverse('attendance'))
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'manager/attendance.html')

    def test_notice_view(self):
        response = self.client.get(reverse('notice'))
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'manager/notice.html')

    def test_noticedetail_view(self):
        notice = self.notice 
        response = self.client.get(reverse('noticedetail', args=[notice.Id])) 
        self.assertEqual(response.status_code, 200) 
    
    def test_myproject_view(self):
        response = self.client.get(reverse('myproject'))
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'employee/myproject.html')

    def test_projectdetails_view(self):
        response = self.client.get(reverse('projectdetails', args=['P001']))
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'employee/projectdetails.html')

    def test_viewallemployees_view(self):
        response = self.client.get(reverse('viewallemployees'))
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'manager/viewallemployees.html')

    def test_viewallmanagers_view(self):
        response = self.client.get(reverse('viewallmanagers'))
        self.assertEqual(response.status_code, 200)
        # self.assertTemplateUsed(response, 'manager/viewallmanagers.html')

    def test_viewleaverequest(self):
        EmployeeLeaveApplication.objects.create(
            employee=self.employee,
            start_date='2024-06-01',
            end_date='2024-06-05',
            reason='Testing leave request update',
            status='Pending'
        )
        response = self.client.get(reverse('viewleaverequest'))
        self.assertEqual(response.status_code, 200)
        # self.assertQuerysetEqual(response.context['requests'], EmployeeLeaveApplication.objects.filter(employee=self.employee), transform=lambda x: x)

    def test_leaverequestdetails(self):
        leave_request = EmployeeLeaveApplication.objects.create(
            employee=self.employee,
            start_date='2024-06-01',
            end_date='2024-06-05',
            reason='Testing leave request update',
            status='Pending'
        )
        response = self.client.get(reverse('leaverequestdetails', kwargs={'wid': leave_request.id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['requestdetail'], leave_request)

    def test_leavedeleterequest(self):
        leave_request = EmployeeLeaveApplication.objects.create(
            employee=self.employee,
            start_date='2024-06-01',
            end_date='2024-06-05',
            reason='Testing leave request update',
            status='Pending'
        )
        response = self.client.post(reverse('leavedeleterequest', kwargs={'wid': leave_request.id}))
        self.assertRedirects(response, reverse('viewleaverequest'))
        self.assertFalse(EmployeeLeaveApplication.objects.filter(id=leave_request.id).exists())

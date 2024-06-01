from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from employee.models import *
from django.contrib.messages import get_messages
import warnings; warnings.filterwarnings("ignore", category=RuntimeWarning, message="DateTimeField .* received a naive datetime")
from .views import *
from django.utils import timezone
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

class SignupViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')  # Assuming 'signup' is the name of the URL pattern for the signup view

    @patch('employee.models.Employee')
    @patch('employee.models.Manager')
    def test_signup_email_domain_invalid(self, MockManager, MockEmployee):
        response = self.client.post(self.signup_url, {
            'id': 'testid',
            'password': 'testpassword',
            'cnfpass': 'testpassword',
            'role': 'employee',
            'email': 'test@invalid.com'
        })
        
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Email must end with @domain.com")
        self.assertRedirects(response, self.signup_url)

    @patch('employee.models.Employee')
    @patch('employee.models.Manager')
    def test_signup_passwords_do_not_match(self, MockManager, MockEmployee):
        response = self.client.post(self.signup_url, {
            'id': 'testid',
            'password': 'testpassword',
            'cnfpass': 'differentpassword',
            'role': 'employee',
            'email': 'test@domain.com'
        })

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Password Doesn't Match")
        self.assertRedirects(response, self.signup_url)

    @patch('employee.models.Employee')
    @patch('employee.models.Manager')
    def test_signup_invalid_role(self, MockManager, MockEmployee):
        response = self.client.post(self.signup_url, {
            'id': 'testid',
            'password': 'testpassword',
            'cnfpass': 'testpassword',
            'role': 'invalidrole',
            'email': 'test@domain.com'
        })

        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid Employee/Manager ID")
        self.assertRedirects(response, self.signup_url)
        

    @patch('employee.models.Employee')
    @patch('employee.models.Manager')
    def test_signup_invalid_id(self, MockManager, MockEmployee):
        MockEmployee.objects.filter.return_value.exists.return_value = False
        MockManager.objects.filter.return_value.exists.return_value = False

        response = self.client.post(self.signup_url, {
            'id': 'testid',
            'password': 'testpassword',
            'cnfpass': 'testpassword',
            'role': 'employee',
            'email': 'test@domain.com'
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), "Invalid Employee/Manager ID")
        self.assertRedirects(response, self.signup_url)




class LoginUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()

        self.manager = Manager.objects.create(
            mID='MGR001',
            firstName='John',
            middleName='A',
            lastName='Doe',
            phoneNo='1234567890',
            email='john.doe@domain.com',
            addharNo='1234-5678-9012',
            dOB='1980-01-01',
            salary='100000',
            joinDate='2020-01-01'
        )

        self.employee = Employee.objects.create(
            eID='EMP001',
            firstName='Jane',
            middleName='B',
            lastName='Smith',
            phoneNo='0987654321',
            email='jane.smith@domain.com',
            addharNo='9012-3456-7890',
            dOB='1990-01-01',
            salary='50000',
            joinDate='2021-01-01',
            manager_id=self.manager
        )

        self.manager_user = User.objects.create_user(username='MGR001', password='testpassword')
        self.employee_user = User.objects.create_user(username='EMP001', password='testpassword')

    def test_login_employee_success(self):
        response = self.client.post(reverse('login_user'), {
            'id': 'EMP001',
            'password': 'testpassword',
            'role': 'employee',
            'email': 'jane.smith@domain.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/employee/dashboard')

    def test_login_manager_success(self):
        response = self.client.post(reverse('login_user'), {
            'id': 'MGR001',
            'password': 'testpassword',
            'role': 'manager',
            'email': 'john.doe@domain.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/manager/m_dashboard')

    def test_login_invalid_role(self):
        response = self.client.post(reverse('login_user'), {
            'id': 'MGR001',
            'password': 'testpassword',
            'role': 'invalidrole',
            'email': 'john.doe@domain.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "Invalid role specified.")

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse('login_user'), {
            'id': 'EMP001',
            'password': 'wrongpassword',
            'role': 'employee',
            'email': 'jane.smith@domain.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "Invalid credentials or user does not exist.")

    def test_login_invalid_email_domain(self):
        response = self.client.post(reverse('login_user'), {
            'id': 'EMP001',
            'password': 'testpassword',
            'role': 'employee',
            'email': 'jane.smith@otherdomain.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "Please use the company's email ending with @domain.com")

    def test_login_email_mismatch(self):
        response = self.client.post(reverse('login_user'), {
            'id': 'EMP001',
            'password': 'testpassword',
            'role': 'employee',
            'email': 'wrong.email@domain.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/')
        messages = list(response.wsgi_request._messages)
        self.assertEqual(str(messages[0]), "Email does not match the registered email for this Employee ID.")

class LogoutUserTestCase(TestCase):
    def test_logout_user(self):
        self.client.login(username='testuser', password='password')
        response = self.client.get(reverse('logout_user'))
        self.assertRedirects(response, "/")
        # self.assertFalse('_auth_user_id' in self.client.session)


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        # Create test data for each model with all fields filled in
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')


        self.manager = Manager.objects.create(
            mID='MGR001',
            firstName='John',
            middleName='A',
            lastName='Doe',
            phoneNo='1234567890',
            email='john.doe@domain.com',
            addharNo='111122223333',
            dOB='1980-01-01',
            salary='50000',
            joinDate='2020-01-01'
        )
        
        self.employee = Employee.objects.create(
            eID='EMP001',
            firstName='Jane',
            middleName='B',
            lastName='Smith',
            phoneNo='0987654321',
            email='jane.smith@domain.com',
            addharNo='444455556666',
            dOB='1990-01-01',
            salary='40000',
            joinDate='2021-01-01',
            skills='Engineer',
            manager_id=self.manager,
            availability='unassigned'
        )
        
        self.project = Project.objects.create(
            id='PRJ001',
            name='Project1',
            description='Test Project',
            start_date='2024-01-01T00:00:00Z',
            end_date='2024-12-31T23:59:59Z',
            # assigner='Admin',
            project_manager=self.manager,
            tasker=self.employee
        )
        
        self.request = Request.objects.create(
            manager=self.manager,
            project=self.project,
            message='Test Request Message',
            created_at='2024-05-01T00:00:00Z',
            status='Pending'
        )
        self.request.employees.add(self.employee)

        self.notice = Notice.objects.create(
            Id='NTC001',
            title='Notice1',
            description='Test Notice',
            publishDate='2024-05-01T00:00:00Z'
        )
    
    def test_viewallmanagers(self):
        response = self.client.get(reverse('viewallmanagers'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/viewallmanagers.html')
        self.assertContains(response, self.manager.firstName)

    def test_viewallemployees(self):
        response = self.client.get(reverse('viewallemployees'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/viewallemployees.html')
        self.assertContains(response, self.employee.firstName)

    def test_viewallprojects(self):
        response = self.client.get(reverse('viewallprojects'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'manager/viewallprojects.html')
        self.assertContains(response, self.project.name)

    def test_viewallrequests(self):
        response = self.client.get(reverse('viewallrequests'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/viewallrequests.html')

    def test_viewallnotices(self):
        response = self.client.get(reverse('viewallnotices'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin/notice.html')
        self.assertContains(response, self.notice.title)

    def test_countview(self):
        response = self.client.get(reverse('countview'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/json')
        data = response.json()
        self.assertEqual(data['total_employees'], 1)
        self.assertEqual(data['total_managers'], 1)
        self.assertEqual(data['total_requests'], 1)
        self.assertEqual(data['total_projects'], 1)


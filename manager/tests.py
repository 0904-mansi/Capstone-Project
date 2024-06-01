import warnings; warnings.filterwarnings("ignore", category=RuntimeWarning, message="DateTimeField .* received a naive datetime")
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from employee.models import *
from .forms import makeRequestForm
from datetime import datetime


class ManagerViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.manager = Manager.objects.create(mID='testmanager', firstName='Test', lastName='Manager',
                                              phoneNo='1234567890', email='test@example.com',
                                              addharNo='123456789012', dOB=datetime.now(), salary='10000',
                                              joinDate=datetime.now())
        
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

        self.user = User.objects.create_user(username='testmanager', password='password')
        self.project = Project.objects.create(
            id='P001',
            name='Project A',
            description='Description A',
            start_date='2023-01-01T00:00:00Z',
            end_date='2023-12-31T00:00:00Z',
            # assigner=self.user,
            project_manager=self.manager,
            tasker=self.employee
        )

        self.notice =Notice.objects.create(
    Id="123456",  # Assuming a specific ID for the notice
    title="Important Notice",
    description="This is an important notice for all employees.",
    publishDate=datetime.now()
)
        self.client.login(username='testmanager', password='password')
        employee1 = self.employee #Employee.objects.create(firstName="Alice", lastName="Smith", email="alice@example.com", eID="alice_smith")

        # Create a Request instance
        self.request = Request.objects.create(
            manager=self.manager,
            project=self.project,
            message="This is a test request message.",
            created_at=datetime.now(),
            status='Pending'
        )

        self.request.employees.add(employee1)


    def test_m_dashboard_view(self):
        response = self.client.get(reverse('m_dashboard'))
        self.assertEqual(response.status_code, 200)

    def test_attendance_view(self):
        response = self.client.get(reverse('attendance'))
        self.assertEqual(response.status_code, 200)

    def test_notice_view(self):
        response = self.client.get(reverse('notice'))
        self.assertEqual(response.status_code, 200)

    
    def test_filteredemployees_view(self):
        response = self.client.get(reverse('filteredemployees'))
        self.assertEqual(response.status_code, 200)

    # def test_myproject_view(self):
    #     response = self.client.get(reverse('myproject'))
    #     self.assertEqual(response.status_code, 200)

    def test_filteredassignedemployees_view(self):
        response = self.client.get(reverse('filteredassignedemployees'))
        self.assertEqual(response.status_code, 200)

    def test_viewRequest_view(self):
        response = self.client.get(reverse('viewRequest'))
        self.assertEqual(response.status_code, 200)

    def test_managerrequest_view(self):
        response = self.client.get(reverse('managerrequest'))
        self.assertEqual(response.status_code, 200)

    
    
    def test_viewallemployees_view(self):
        response = self.client.get(reverse('viewallemployees'))
        self.assertEqual(response.status_code, 200)

    def test_viewallprojects_view(self):
        response = self.client.get(reverse('viewallprojects'))
        self.assertEqual(response.status_code, 200)

    def test_viewproject_view(self):
        response = self.client.get(reverse('viewproject'))
        self.assertEqual(response.status_code, 200)

    def test_viewallmanagers_view(self):
        response = self.client.get(reverse('viewallmanagers'))
        self.assertEqual(response.status_code, 200)

    def test_manleaverequest_view(self):
        response = self.client.get(reverse('manleaverequest'))
        self.assertEqual(response.status_code, 200)

    def test_manviewleaverequest_view(self):
        response = self.client.get(reverse('manviewleaverequest'))
        self.assertEqual(response.status_code, 200)

    
    
    def test_noticedetail_view(self):
            # Create a test notice
        notice = self.notice
        response = self.client.get(reverse('noticedetail', args=[notice.Id]))
        self.assertEqual(response.status_code, 200)

    def test_requestdetails_view(self):
        # Create a test request
        request = self.request
        response = self.client.get(reverse('requestdetails', args=[request.id]))
        self.assertEqual(response.status_code, 200)

    def test_updaterequest_view(self):
        # Create a test request
        request = self.request
        response = self.client.get(reverse('updaterequest', args=[request.id]))
        self.assertEqual(response.status_code, 200)

    def test_deleterequest_view(self):
        # Create a test request
        request = self.request
        response = self.client.get(reverse('deleterequest', args=[request.id]))
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after deletion

    def test_manleaverequestdetails_view(self):
        # Create a test leave request
        leave_request = ManagerLeaveApplication.objects.create(manager=self.manager, start_date="2024-06-01", end_date="2024-06-05", reason="Test leave request")
        response = self.client.get(reverse('manleaverequestdetails', args=[leave_request.id]))
        self.assertEqual(response.status_code, 200)

    def test_manleaveupdaterequest_view(self):
        # Create a test leave request
        leave_request = ManagerLeaveApplication.objects.create(manager=self.manager, start_date="2024-06-01", end_date="2024-06-05", reason="Test leave request")
        response = self.client.get(reverse('manleaveupdaterequest', args=[leave_request.id]))
        self.assertEqual(response.status_code, 200)

    def test_manleavedeleterequest_view(self):
        # Create a test leave request
        leave_request = ManagerLeaveApplication.objects.create(manager=self.manager, start_date="2024-06-01", end_date="2024-06-05", reason="Test leave request")
        response = self.client.get(reverse('manleavedeleterequest', args=[leave_request.id]))
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after deletion

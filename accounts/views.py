from urllib import request
from django.shortcuts import redirect, render
from django.http import HttpResponse
from employee.models import *
from django.contrib.auth.models import User,auth
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


def login_user(request):
    if request.method == "POST":
        id = request.POST["id"]
        password = request.POST["password"]
        role = request.POST["role"].lower()  # Normalize role to lowercase for easier comparison
        email_id = request.POST["email"]
        required_domain = "@domain.com"
        
        if not email_id.endswith(required_domain):
            messages.error(request, f"Please use the company's email ending with {required_domain}")
            return redirect("/")
        
        # Check if the user exists in the User model
        user = authenticate(request, username=id, password=password)
        if not user:
            messages.error(request, "Invalid credentials or user does not exist.")
            return redirect("/")
        
        # try:
        if role.lower() == "employee":
            employee = Employee.objects.get(eID=id)
            if employee.email != email_id:
                messages.error(request, "Email does not match the registered email for this Employee ID.")
                return redirect("/")
            if not user.check_password(password):
                messages.error(request, "Invalid credentials for Employee.")
                return redirect("/")
            
        elif role.lower() == "manager":
            manager = Manager.objects.get(mID=id)
            if manager.email != email_id:
                messages.error(request, "Email does not match the registered email for this Manager ID.")
                return redirect("/")
            if not user.check_password(password):
                messages.error(request, "Invalid credentials for Manager.")
                return redirect("/")
            
        else:
            messages.error(request, "Invalid role specified.")
            return redirect("/")
        
        
        # except:
        #     if user == manager and role == "Employee":
        #         messages.error(request, "Invalid role for ID.")
        #     elif  user == employee and role == "Manager":
        #         messages.error(request, "Invalid role for ID.")
        #     else:
        #         messages.error(request, "Invalid role specified.")
        #         return redirect("/")


        
        login(request, user)
        if role.lower() == "manager":
            return redirect("/manager/m_dashboard")
        elif role.lower() == "employee":
            return redirect("/employee/dashboard")

        # except Employee.DoesNotExist:
            
    return render(request, "employee/Login.html")

def logout_user(request):
    logout(request)
    return redirect("/")

def signup(request):
    if request.method == "POST":
        id = request.POST["id"]
        password = request.POST["password"]
        cnfpass = request.POST["cnfpass"]
        role = request.POST["role"]
        email = request.POST["email"]
        required_domain = "@domain.com"
        
        if not email.endswith(required_domain):
            messages.info(request, f"Email must end with {required_domain}")
            return redirect("/signup")
        
        if password == cnfpass:
            if Employee.objects.filter(eID=id).exists() or Manager.objects.filter(mID=id).exists():
                if role.lower() == "manager":
                    if Employee.objects.filter(eID=id).exists():
                        messages.info(request, "Invalid Credentials")
                        return redirect("/signup")
                    return redirect("/")
                elif role.lower() == "employee":
                    if Manager.objects.filter(mID=id).exists():
                        messages.info(request, "Invalid Credentials")
                        return redirect("/signup")
                    return redirect("/")
                else:
                    messages.info(request, "Invalid role specified.")
                    return redirect("/signup")
            else:
                messages.info(request, "Invalid Employee/Manager ID")
                return redirect("/signup")
        else:
            messages.info(request, "Password Doesn't Match")
            return redirect("/signup")
            
    return render(request, "employee/signup.html")


@login_required(login_url='/')
def viewallmanagers(request):
    managers = Manager.objects.all()
    return render(request, 'admin/viewallmanagers.html', {'managers': managers})

@login_required(login_url='/')
def viewallemployees(request):
    employees = Employee.objects.all()
    return render(request, 'admin/viewallemployees.html', {'employees': employees})


@login_required(login_url='/')
def viewallprojects(request):
    projects = Project.objects.all()
    return render(request, 'admin/viewallprojects.html', {'projects': projects})


# @login_required(login_url='/')
def viewallrequests(request):
    requests = Request.objects.all()
    return render(request,"admin/viewallrequests.html",{"requests":requests})

# @login_required(login_url='/')
def viewallnotices(request):
    notices  = Notice.objects.all()
    return render(request,"admin/notice.html",{"notices":notices})

# @login_required(login_url='/')
def create_employee(request):
    if request.method == 'POST':
        form = Employee(request.POST)
        if form.is_valid():
            employee = form.save()
            send_employee_notification(employee)
    return 

# @login_required(login_url='/')   
def send_employee_notification(employee):
    subject = 'New Employee Added'
    context = {'employee': employee}
    html_message = render_to_string('email/employee_notification.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'mansimishra510@gmail.com'  # Update with your email address
    to_email = 'mansimishra2314@gmail.com'  # Update with recipient's email address
    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)


def create_manager(request):
    if request.method == 'POST':
        form = Manager(request.POST)
        if form.is_valid():
            manager = form.save()
            send_manager_notification(manager)
        return 
    
def send_manager_notification(manager):
    subject = 'New Manager Added'
    context = {'manager': manager}
    html_message = render_to_string('email/employee_notification.html', context)
    plain_message = strip_tags(html_message)
    from_email = 'mansimishra510@gmail.com'  # Update with your email address
    to_email = 'mansimishra2314@gmail.com'  # Update with recipient's email address

    send_mail(subject, plain_message, from_email, [to_email], html_message=html_message)


def countview(request):
    total_employees = Employee.objects.count()
    total_managers = Manager.objects.count()
    total_requests = Request.objects.count()
    total_projects = Project.objects.count()
    total_notices = Notice.objects.count()
    context = {
        'total_employees': total_employees,
        'total_managers': total_managers,
        'total_requests': total_requests,
        'total_projects': total_projects,
        'total_notices': total_notices,
    }
    return JsonResponse(context)

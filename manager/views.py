import re
from django.shortcuts import render
from django.shortcuts import redirect, render, get_object_or_404
from .forms import *
from django.http import JsonResponse
from employee.models import Employee,Employee_Attendance,Notice,Manager,Project,Manager_Attendance
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
 

# Create your views here.
@login_required(login_url='/')
def m_dashboard(request):
    info = Manager.objects.filter(mID=request.user.username)
    return render(request,"manager/m_dashboard.html",{'info':info})

@login_required(login_url='/')
def attendance(request):
    attendance=Manager_Attendance.objects.filter(mId=request.user.username)
    return render(request,"manager/attendance.html",{"info":attendance})    

@login_required(login_url='/')
def notice(request):
    notices  = Notice.objects.all()
    return render(request,"manager/notice.html",{"notices":notices})

@login_required(login_url='/')
def noticedetail(request,id):
    noticedetail = Notice.objects.get(Id=id)
    return render(request,"manager/noticedetail.html",{"noticedetail":noticedetail})



@login_required(login_url='/')
def filteredemployees(request):
    skill_query = request.GET.get('skill_query', '')      
    employees = Employee.objects.filter(skills__contains=skill_query)
    return render(request, 'manager/viewallemployees.html', {'employees': employees, 'skill_query': skill_query})

# @login_required(login_url='/')
# def myproject(request):
#     user = request.user
#     try:
#         # Fetch the employee object associated with the logged-in user
#         manager = Manager.objects.get(mID=user)
#         projects = Project.objects.get(project_manager=manager)
       
#     except Manager.DoesNotExist:
#         projects = []
#         messages.error(request, "Manager details not found.")
    
#     return render(request, 'employee/myproject.html', {'projects': projects})


@login_required(login_url='/')
def filteredassignedemployees(request):
    skill_query = request.GET.get('skill_query', '')
    project_query = request.GET.get('project_query', '')

    # Initialize the queryset
    employees = Employee.objects.all()

    # Apply skill filter if provided
    if skill_query:
        employees = employees.filter(skills__icontains=skill_query)

    # Apply project filter if provided
    if project_query:
        if project_query.lower() == 'assigned':
            employees = employees.filter(availability='assigned')
        elif project_query.lower() == 'unassigned':
            employees = employees.filter(availability='unassigned')

    context = {
        'employees': employees,
        'skill_query': skill_query,
        'project_query': project_query,
    }

    return render(request, 'manager/viewallemployees.html', context)

@login_required(login_url='/')
def viewRequest(request):
    requests = Request.objects.filter(manager=request.user.username)
    return render(request,"manager/viewRequest.html",{"requests":requests})


@login_required(login_url='/')
def managerrequest(request):
    if request.method == "POST":
        form = makeRequestForm(request.POST)
        if form.is_valid():
            manager_id = form.cleaned_data.get('manager').mID
            if request.user.username != manager_id:
                messages.error(request, "Invalid ID selected.")
                return redirect('managerrequest')

            form.save()
            subject = 'New Request Submission'
            message = '''Dear Admin,

A new request has been submitted. Please have a look at it and give its status an update at your earliest.

Thank You!
Best Regards'''
            from_email = "mansimishra510@gmail.com"  # Ensure you have set this in your settings
            recipient_list = ['mansimishra2314@gmail.com']  # Replace with the recipient's email
            send_mail(subject, message, from_email, recipient_list)
            return redirect('viewRequest')
    else:
        form = makeRequestForm()
    return render(request, "manager/managerrequest.html", {"form": form})



@login_required(login_url='/')
def requestdetails(request,wid):
    requestdetail = Request.objects.get(id=wid)
    return render(request,"manager/requestdetails.html",{"requestdetail":requestdetail})


@login_required(login_url='/')
def updaterequest(request, wid):
    request_instance = get_object_or_404(Request, id=wid)
    form = makeRequestForm(request.POST or None, instance=request_instance)
    flag = ""
    if form.is_valid():
        form.save()
        flag = "Request Updated Successfully!!"
        return redirect('viewRequest')
    return render(request, "manager/updaterequest.html", {'form': form, 'flag': flag})

@login_required(login_url='/')
def deleterequest(request, wid):
    request = get_object_or_404(Request, id=wid)
    # if request.method == 'POST':
    request.delete()
    return redirect('viewRequest')
    # return render(request, "manager/deleterequest.html", {'request_instance': request_instance})


@login_required(login_url='/')
def viewallemployees(request):
    employees = Employee.objects.all()
    return render(request, 'manager/viewallemployees.html', {'employees': employees})


@login_required(login_url='/')
def viewallprojects(request):
    projects = Project.objects.all()
    # print(projects)
    return render(request, 'manager/viewallprojects.html', {'projects': projects})

def viewproject(request):
    # Assuming the manager is identified by their user ID
    manager_id = request.user
    try:
        manager = Manager.objects.get(mID=manager_id)
        print(manager)
        projects = Project.objects.filter(project_manager=manager.mID)
        print(projects)
    except Manager.DoesNotExist:
        projects = []
        messages.error(request, "Employee details not found.")
    
    return render(request, 'manager/viewproject.html', {'projects': projects})


@login_required(login_url='/')
def viewallmanagers(request):
    managers = Manager.objects.all()
    return render(request, 'manager/viewallmanagers.html', {'managers': managers})

@login_required(login_url='/')
def manleaverequest(request):
    form = ManLeaveApplicationForm(request.POST)
    if form.is_valid():
        selected_employee_id = form.cleaned_data.get('manager').mID
        if request.user.username != selected_employee_id:
            messages.error(request, "Invalid ID selected.")
            return redirect('manleaverequest')

        form.save()
        subject = 'New Request Submission'
        message = f'''Dear Admin,

A new leave request has been submitted. Please have a look at it and give its status an update at your earliest.

Thank You!
Best Regards
            '''
        from_email = "mansimishra510@gmail.com"  # Ensure you have set this in your settings
        recipient_list = ['mansimishra2314@gmail.com']  # Replace with the recipient's email

            # Send email
        send_mail(subject, message, from_email, recipient_list)


        # Redirect or perform other actions after successful form submission
        return redirect('manviewleaverequest')  # Redirect to a success page
    else:
        form = ManLeaveApplicationForm()
    return render(request, "manager/manleaverequest.html", {"form" : form})

@login_required(login_url='/')
def manviewleaverequest(request):
    requests = ManagerLeaveApplication.objects.filter(manager=request.user.username)
    return render(request,"manager/viewleaverequest.html",{"requests":requests})


@login_required(login_url='/')
def manleaverequestdetails(request,wid):
    requestdetail = ManagerLeaveApplication.objects.get(id=wid)
    return render(request,"manager/manrequestdetails.html",{"requestdetail":requestdetail})


@login_required(login_url='/')
def manleaveupdaterequest(request, wid):
    request_instance = get_object_or_404(ManagerLeaveApplication, id=wid)
    form = ManLeaveApplicationForm(request.POST or None, instance=request_instance)
    flag = ""
    if form.is_valid():
        form.save()
        flag = "Request Updated Successfully!!"
        return redirect('viewleaverequest')
    return render(request, "manager/updaterequest.html", {'form': form, 'flag': flag})

@login_required(login_url='/')
def manleavedeleterequest(request, wid):
    request = get_object_or_404(ManagerLeaveApplication, id=wid)
    # if request.method == 'POST':
    request.delete()
    return redirect('manviewleaverequest')


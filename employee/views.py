from django.shortcuts import redirect, render, get_object_or_404
from requests import Session
from .forms import *
from employee.models import *
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import List

@login_required(login_url='/')
def dashboard(request):
    info = Employee.objects.filter(eID=request.user.username)
    return render(request,"employee/dashboard.html",{'info':info})


@login_required(login_url='/')
def updateskills(request):
    if request.method == 'POST':
        skills = request.POST.get('skills')
        employee_id = request.user.username
        employee = Employee.objects.get(eID=employee_id)
        employee.skills = skills
        employee.save()
        messages.success(request, 'Skills updated successfully.')
    return redirect('dashboard')

@login_required(login_url='/')
def attendance(request):
    attendance=Employee_Attendance.objects.filter(eId=request.user.username)
    return render(request,"employee/attendance.html",{"info":attendance})    

@login_required(login_url='/')
def notice(request):
    notices  = Notice.objects.all()
    return render(request,"employee/notice.html",{"notices":notices})

@login_required(login_url='/')
def noticedetail(request,id):
    noticedetail = Notice.objects.get(Id=id)
    return render(request,"employee/noticedetail.html",{"noticedetail":noticedetail})

@login_required(login_url='/')
def myproject(request):
    user = request.user
    employee = Employee.objects.get(eID=user)
    projects = Project.objects.filter(tasker_id=employee.eID)
    return render(request, 'employee/myproject.html', {'projects': projects})

@login_required(login_url='/')
def projectdetails(request,wid):
    projectdetails = Project.objects.get(id=wid);
    return render(request,"employee/projectdetails.html",{"projectdetails":projectdetails})

@login_required(login_url='/')
def viewallemployees(request):
    employees = Employee.objects.all()
    return render(request, 'employee/viewallemployees.html', {'employees': employees})

@login_required(login_url='/')
def viewallmanagers(request):
    managers = Manager.objects.all()
    return render(request, 'employee/viewallmanagers.html', {'managers': managers})

@login_required(login_url='/')
def empleaverequest(request):
    form = LeaveApplicationForm(request.POST)
    if form.is_valid():
        selected_employee_id = form.cleaned_data.get('employee').eID
        if request.user.username != selected_employee_id:
            messages.error(request, "Invalid ID selected.")
            return redirect('empleaverequest')

        form.save()
        subject = 'New Request Submission'
        message = f'''Dear Admin,

                A new leave request has been submitted. Please have a look at it and give its status an update at your earliest.

                Thank You!
                Best Regards
            '''
        from_email = "mansimishra510@gmail.com"  
        recipient_list = ['mansimishra2314@gmail.com']  
        send_mail(subject, message, from_email, recipient_list)
        return redirect('viewleaverequest')
    else:
        form = LeaveApplicationForm()
    return render(request, "employee/empleaverequest.html", {"form" : form})

@login_required(login_url='/')
def viewleaverequest(request):
    requests = EmployeeLeaveApplication.objects.filter(employee=request.user.username)
    return render(request,"employee/viewleaverequest.html",{"requests":requests})


@login_required(login_url='/')
def leaverequestdetails(request,wid):
    requestdetail = EmployeeLeaveApplication.objects.get(id=wid)
    return render(request,"employee/requestdetails.html",{"requestdetail":requestdetail})



@login_required(login_url='/')
def leavedeleterequest(request, wid):
    request = get_object_or_404(EmployeeLeaveApplication, id=wid)
    request.delete()
    return redirect('viewleaverequest')


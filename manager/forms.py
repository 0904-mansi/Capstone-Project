from tkinter import Widget
from django import forms
from employee.models import  *
from django.contrib.auth.models import User

# class workform(forms.ModelForm):
#     class Meta:
#         model=workAssignments
#         widgets={
#             "assignDate" : forms.DateInput(attrs={'type':'datetime-local'}),
#             "dueDate" : forms.DateInput(attrs={'type':'datetime-local'}),
#             }
#         labels={"assignerId" : "Select Your Id"}
        
#         fields=[
#             "assignerId",
#             "work",
#             "assignDate",
#             "dueDate",
#             "taskerId",

#         ]
        
class makeRequestForm(forms.ModelForm):
    admin_id = forms.ModelChoiceField(queryset=User.objects.filter(is_superuser=True), label="Select Admin")
    class Meta:
        model=Request
        widgets={
            "created_at" : forms.DateInput(attrs={'type':'datetime-local'}),
            }
        labels = {
        "manager": "Select Your Id",
        "admin_id": "Select Admin",
        }
    
        fields=[
            "manager",
            "message",
            "created_at",
            "employees",
            "project",
        ]


class ManLeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = ManagerLeaveApplication
        fields = [
            'manager',
            'start_date',
            'end_date',
            'reason',
          
        ]
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
            'reason': forms.Textarea(attrs={'rows': 4}),

        }
        labels = {
            "manager": "Select Your Id",
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'reason': 'Reason for Leave',
        }

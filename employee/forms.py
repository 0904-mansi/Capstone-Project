from tkinter import Widget
from django import forms
from .models import *

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
        # model=Requests
        widgets={
            "requestDate" : forms.DateInput(attrs={'type':'datetime-local'}),
            }
        labels={"manager" : "Select Your Id"}
        
        fields=[
            "manager",
            "requestMessage",
            "requestDate",
        ]

class LeaveApplicationForm(forms.ModelForm):
    class Meta:
        model = EmployeeLeaveApplication
        fields = [
            'employee',
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
            "employee": "Select Your Id",
            'start_date': 'Start Date',
            'end_date': 'End Date',
            'reason': 'Reason for Leave',
        }

from django.contrib import admin
from employee.models import * 
from django.contrib.auth.models import *

admin.site.register(Employee)
admin.site.register(Employee_Attendance)
admin.site.register(Manager)
admin.site.register(Manager_Attendance)
admin.site.register(Notice)
admin.site.register(Project)


class RequestAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return False

admin.site.register(Request, RequestAdmin)
admin.site.register(EmployeeLeaveApplication,RequestAdmin )
admin.site.register(ManagerLeaveApplication,RequestAdmin )

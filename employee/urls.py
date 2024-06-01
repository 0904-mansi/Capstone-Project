from django.urls import path
from . import views

 
urlpatterns = [
    path('dashboard',views.dashboard,name="dashboard"),
    path('attendance',views.attendance,name="attendance"),
    path('notice',views.notice,name="notice"),
    path('noticedetail/?P<id>/',views.noticedetail,name="noticedetail"),
    # path('assignwork',views.assignwork,name="assignwork"),
    path('myproject',views.myproject,name="myproject"),
    path('projectdetails/?P<wid>/',views.projectdetails,name="projectdetails"),
    path('viewallemployees', views.viewallemployees, name='viewallemployees'),
    path('updateskills', views.updateskills, name='updateskills'),
    path('viewallmanagers', views.viewallmanagers, name='viewallmanagers'),
    path('leavedeleterequest/?P<wid>/',views.leavedeleterequest,name="leavedeleterequest"),
    # path('leaveupdaterequest/?P<wid>',views.leaveupdaterequest,name="leaveupdaterequest"),
    path('empleaverequest',views.empleaverequest,name="empleaverequest"),
    path('viewleaverequest',views.viewleaverequest,name="viewleaverequest"),
    path('leaverequestdetails/?P<wid>/',views.leaverequestdetails,name="leaverequestdetails"),
    
    # path('manager_details',views.manager_details,name="manager_details"),

]
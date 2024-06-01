from django.urls import path
from . import views

 
urlpatterns = [
    path('m_dashboard',views.m_dashboard,name="m_dashboard"),
    path('attendance',views.attendance,name="attendance"),
    path('notice',views.notice,name="notice"),
    path('noticedetail/?P<id>/',views.noticedetail,name="noticedetail"),
    # path('assignwork',views.assignWork,name="assignwork"),
    # path('mywork',views.mywork,name="mywork"),
    # path('workdetails/?P<wid>/',views.workdetails,name="workdetails"),
    # path('editAW',views.assignedworklist,name="assignedworklist"),
    path('deleterequest/?P<wid>/',views.deleterequest,name="deleterequest"),
    path('updaterequest/?P<wid>',views.updaterequest,name="updaterequest"),
    path('managerrequest',views.managerrequest,name="managerrequest"),
    path('viewRequest',views.viewRequest,name="viewRequest"),
    path('requestdetails/?P<wid>/',views.requestdetails,name="requestdetails"),
    # path('projectdetails/?P<wid>/',views.projectdetails,name="projectdetails"),
    path('viewallemployees', views.viewallemployees, name='viewallemployees'),
    path('viewallprojects', views.viewallprojects, name='viewallprojects'),
    path('viewproject', views.viewproject, name='viewproject'),
    # path('myproject', views.myproject, name='myproject'),
    path('viewallmanagers', views.viewallmanagers, name='viewallmanagers'),
    path('filteredemployees', views.filteredemployees, name='filteredemployees'),
    path('filteredassignedemployees/', views.filteredassignedemployees, name='filteredassignedemployees'),  # New URL pattern
    path('manleavedeleterequest/?P<wid>/',views.manleavedeleterequest,name="manleavedeleterequest"),
    path('manleaveupdaterequest/?P<wid>',views.manleaveupdaterequest,name="manleaveupdaterequest"),
    path('manleaverequest',views.manleaverequest,name="manleaverequest"),
    path('manviewleaverequest',views.manviewleaverequest,name="manviewleaverequest"),
    path('manleaverequestdetails/?P<wid>/',views.manleaverequestdetails,name="manleaverequestdetails"),
    # path('viewleaverequest', views.viewleaverequest, name='viewleaverequest'),  # New URL pattern
    
]
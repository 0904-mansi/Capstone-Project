from django.contrib import admin
from django.urls import include, path

from . import views

urlpatterns = [
    path('',views.login_user,name="login_user"),
    path('logout',views.logout_user,name="logout_user"),
    path('signup',views.signup,name="signup"),
    path('api/stats/',views.countview,name="countview"),
    path('viewallmanagers',views.viewallmanagers, name='viewallmanagers'),
    path('viewallemployees',views.viewallemployees, name='viewallemployees'),
    path('viewallprojects',views.viewallprojects, name='viewallprojects'),
    path('viewallrequests',views.viewallrequests, name='viewallrequests'),
    path('viewallnotices',views.viewallnotices, name='viewallnotices'),

]   
"""EmployeeLeaveManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from employeeleave.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',index, name='index'),
    path('admin_login',admin_login, name='admin_login'),
    path('dashboard/',dashboard, name='dashboard'),
    path('add_department',add_department, name='add_department'),
    path('manage_department',manage_department, name='manage_department'),
    path('edit_department/<int:pid>',edit_department,name='edit_department'),
    path('delete_department/<int:pid>',delete_department,name='delete_department'),
    path('add_leavetype',add_leavetype, name='add_leavetype'),
    path('manage_leavetype',manage_leavetype, name='manage_leavetype'),
    path('edit_leavetype/<int:pid>',edit_leavetype,name='edit_leavetype'),
    path('delete_leavetype/<int:pid>',delete_leavetype,name='delete_leavetype'),
    path('changepasswordadmin',changepasswordadmin, name='changepasswordadmin'),
    path('changepassworduser',changepassworduser, name='changepassworduser'),
    path('logout/',Logout, name='logout'),
    path('add_employee',add_employee, name='add_employee'),
    path('manage_employee',manage_employee, name='manage_employee'),
    path('delete_employee/<int:pid>',delete_employee,name='delete_employee'),
    path('edit_employee/<int:pid>',edit_employee,name='edit_employee'),
    path('active_employee/<int:pid>',active_employee,name='active_employee'),
    path('inactive_employee/<int:pid>',inactive_employee,name='inactive_employee'),
    path('myprofile',myprofile, name='myprofile'),
    path('apply_leave',apply_leave, name='apply_leave'),
    path('leavehistory',leavehistory, name='leavehistory'),
    path('leave_details/<int:pid>',leave_details,name='leave_details'),
    path('all_leaves',all_leaves, name='all_leaves'),
    path('pending_leaves',pending_leaves, name='pending_leaves'),
    path('approved_leaves',approved_leaves, name='approved_leaves'),
    path('unapproved_leaves',unapproved_leaves, name='unapproved_leaves'),
    
]

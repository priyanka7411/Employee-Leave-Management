from django.db.models import Q
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from datetime import date
from datetime import datetime, timedelta, time
import random
from .models import Employee, Department
from django.contrib.auth.decorators import login_required


def index(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'index.html', d)

@login_required
def myprofile(request):
    user = request.user
    employee = get_object_or_404(Employee, user=user)

    department = Department.objects.all()
    error = ""

    if request.method == 'POST':
        ec = request.POST.get('empcode')
        fn = request.POST.get('firstName')
        ln = request.POST.get('lastName')
        em = request.POST.get('email')
        gen = request.POST.get('gender')
        dob = request.POST.get('dob')
        dept = request.POST.get('department')
        addr = request.POST.get('address')
        city = request.POST.get('city')
        country = request.POST.get('country')
        mn = request.POST.get('mobileno')

        if employee:
            employee.empid = ec
            employee.user.first_name = fn
            employee.user.last_name = ln
            employee.user.email = em
            employee.gender = gen
            employee.dob = dob
            employee.department = dept
            employee.address = addr
            employee.city = city
            employee.country = country
            employee.phoneno = mn
            try:
                employee.user.save()
                employee.save()
                error = "no"
            except Exception as e:
                error = "yes"
                print(f"Error saving employee: {e}")
        else:
            error = "no_employee"

    context = {'employee': employee, 'department': department, 'error': error}
    return render(request, 'myprofile.html', context)
def admin_login(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request,user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'admin_login.html',d)


def dashboard(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    empcount = Employee.objects.all().count()
    deptcount = Department.objects.all().count()
    ltcount = Leavetype.objects.all().count()
    leaves = Leaves.objects.all().order_by('-id')[:4]
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    d = {'empcount':empcount,'deptcount':deptcount,'ltcount': ltcount,'leaves': leaves,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'dashboard.html',d)


def add_department(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    error = ""
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    if request.method=="POST":
        dn = request.POST['departmentname']
        dsn = request.POST['departmentshortname']
        dc = request.POST['deptcode']
        try:
            Department.objects.create(deptname=dn,deptshortname=dsn,deptcode=dc,creationdate=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'add_department.html', d)


def manage_department(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    department = Department.objects.all()
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    d = {'department':department,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'manage_department.html', d)

def edit_department(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    department = Department.objects.get(id=pid)
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    error = ""
    if request.method == 'POST':
        dn = request.POST['departmentname']
        dsn = request.POST['departmentshortname']
        dc = request.POST['deptcode']
        department.deptname = dn
        department.deptshortname = dsn
        department.deptcode = dc
        try:
            department.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'department':department,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'edit_department.html',d)


def delete_department(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    department = Department.objects.get(id=pid)
    department.delete()
    return redirect('manage_department')


def add_leavetype(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    error = ""
    if request.method=="POST":
        lt = request.POST['leavetype']
        des = request.POST['description']
        try:
            Leavetype.objects.create(leavetypename=lt,description=des,creationdate=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'add_leavetype.html', d)


def manage_leavetype(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    leavetype = Leavetype.objects.all()
    d = {'leavetype':leavetype,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'manage_leavetype.html', d)


def edit_leavetype(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    leavetype = Leavetype.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        lt = request.POST['leavetype']
        des = request.POST['description']
        leavetype.leavetypename = lt
        leavetype.description = des

        try:
            leavetype.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'leavetype':leavetype,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'edit_leavetype.html',d)


def delete_leavetype(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    leavetype = Leavetype.objects.get(id=pid)
    leavetype.delete()
    return redirect('manage_leavetype')


def Logout(request):
    logout(request)
    return redirect('admin_login')


def changepasswordadmin(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    error = ""
    
    if request.method == "POST":
        currentpassword = request.POST.get('currentpassword')
        newpassword = request.POST.get('newpassword')
        confirmpassword = request.POST.get('confirmpassword')

        if not currentpassword or not newpassword or not confirmpassword:
            messages.error(request, "All fields are required")
            return redirect('changepasswordadmin')

        if newpassword != confirmpassword:
            messages.error(request, "New password and Confirm password do not match")
            return redirect('changepasswordadmin')

        try:
            user = User.objects.get(username=request.user.username)
            
            if not user.check_password(currentpassword):
                messages.error(request, "Current password is incorrect")
                return redirect('changepasswordadmin')

            user.set_password(newpassword)
            user.save()
            messages.success(request, "Password changed successfully")
            return redirect('admin_login')
        
        except User.DoesNotExist:
            messages.error(request, "User does not exist")
            return redirect('changepasswordadmin')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
            return redirect('changepasswordadmin')

    context = {'error': error, 'leavescount': leavescount, 'unreadleaves': unreadleaves}
    return render(request, 'changepasswordadmin.html', context)

def changepassworduser(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""    
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error}
    return render(request,'changepassworduser.html',d)




def add_employee(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    error = ""
    department = Department.objects.all()
    if request.method=="POST":
        ec = request.POST['empcode']
        fn = request.POST['firstName']
        ln = request.POST['lastName']
        em = request.POST['email']
        pwd = request.POST['password']
        gen = request.POST['gender']
        dob = request.POST['dob']
        dept = request.POST['department']
        addr = request.POST['address']
        city = request.POST['city']
        country = request.POST['country']
        mn = request.POST['mobileno']
        try:
            user = User.objects.create_user(username=em, password=pwd, first_name=fn, last_name=ln)
            Employee.objects.create(user = user,empid = ec,gender = gen,dob = dob,department=dept,address=addr,city=city,country=country,phoneno=mn,status="1",regdate=date.today())
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'department':department,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'add_employee.html', d)


def manage_employee(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    employee = Employee.objects.all()
    d = {'employee':employee,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'manage_employee.html', d)


def edit_employee(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    department = Department.objects.all()
    user = User.objects.get(id=pid)
    employee = Employee.objects.get(user=user)
    error = ""
    if request.method == 'POST':
        ec = request.POST['empcode']
        fn = request.POST['firstName']
        ln = request.POST['lastName']
        em = request.POST['email']
        gen = request.POST['gender']
        dob = request.POST['dob']
        dept = request.POST['department']
        addr = request.POST['address']
        city = request.POST['city']
        country = request.POST['country']
        mn = request.POST['mobileno']
        employee.empid = ec
        employee.user.first_name = fn
        employee.user.last_name = ln
        employee.user.username = em
        employee.gender = gen
        employee.dob = dob
        employee.department = dept
        employee.address = addr
        employee.city = city
        employee.country = country
        employee.phoneno = mn
        try:
            employee.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'department':department,'employee':employee,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'edit_employee.html',d)


def delete_employee(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = User.objects.get(id=pid)
    user.delete()
    return redirect('manage_employee')

def active_employee(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = User.objects.get(id=pid)
    employee = Employee.objects.get(user=user)
    employee.status = "1"
    employee.save()
    return redirect('manage_employee')

def inactive_employee(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    user = User.objects.get(id=pid)
    employee = Employee.objects.get(user=user)
    employee.status = "0"
    employee.save()
    return redirect('manage_employee')



def apply_leave(request):
    if not request.user.is_authenticated:
        return redirect('index')
    error = ""
    leavetypes = Leavetype.objects.all()
    if request.method=="POST":
        lt = request.POST['leavetype']
        fd = request.POST['fromdate']
        td = request.POST['todate']
        des = request.POST['description']
        user = User.objects.get(id=request.user.id)
        employee = Employee.objects.get(user=user)
        try:
            Leaves.objects.create(leavetype=lt,todate=td,fromdate=fd,description=des,postingdate=date.today(),isread="no",emp=employee)
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'leavetypes':leavetypes}
    return render(request, 'apply_leave.html', d)


def leavehistory(request):
    if not request.user.is_authenticated:
        return redirect('index')
    user = User.objects.get(id=request.user.id)
    employee = Employee.objects.get(user=user)
    leave = Leaves.objects.filter(emp = employee)
    d = {'leave':leave}
    return render(request, 'leavehistory.html', d)


def leave_details(request,pid):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    leave = Leaves.objects.get(id=pid)
    error = ""
    if request.method == 'POST':
        st = request.POST['status']
        des = request.POST['description']
        leave.status = st
        leave.adminremark = des
        leave.adminremarkdate = date.today()
        leave.isread = "yes"
        try:
            leave.save()
            error = "no"
        except:
            error = "yes"
    d = {'error': error,'leave':leave,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'leave_details.html',d)


def all_leaves(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    leaves = Leaves.objects.all()
    d = {'leaves':leaves,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'all_leaves.html', d)

def pending_leaves(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    leaves = Leaves.objects.filter(status=None)
    d = {'leaves':leaves,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'pending_leaves.html', d)

def approved_leaves(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    leaves = Leaves.objects.filter(status="Accept")
    d = {'leaves':leaves,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'approved_leaves.html', d)

def unapproved_leaves(request):
    if not request.user.is_authenticated:
        return redirect('admin_login')
    leavescount = Leaves.objects.filter(isread="no").count()
    unreadleaves = Leaves.objects.filter(isread="no")
    leaves = Leaves.objects.filter(status="Reject")
    d = {'leaves':leaves,'leavescount':leavescount,'unreadleaves':unreadleaves}
    return render(request, 'unapproved_leaves.html', d)


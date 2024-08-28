from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# Create your models here.

class Department(models.Model):
    deptname = models.CharField(max_length=100)
    deptshortname = models.CharField(max_length=15)
    deptcode = models.CharField(max_length=10)
    creationdate = models.DateField()
    def __str__(self):
        return self.deptname


class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    empid = models.CharField(max_length=20)
    gender = models.CharField(max_length=30)
    dob = models.CharField(max_length=50)
    department = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    phoneno = models.CharField(max_length=15)
    status = models.CharField(max_length=15, null=True)
    regdate = models.DateField()

    def __str__(self):
        return self.user.username

class Leavetype(models.Model):
    leavetypename = models.CharField(max_length=70)
    description = models.CharField(max_length=500)
    creationdate = models.DateField()
    def __str__(self):
        return self.leavetypename


class Leaves(models.Model):
    leavetype = models.CharField(max_length=100)
    todate = models.DateField()
    fromdate = models.DateField()
    description = models.CharField(max_length=500)
    postingdate = models.DateField()
    adminremark = models.CharField(max_length=100,null=True)
    adminremarkdate = models.DateField(null=True)
    status = models.CharField(max_length=50,null=True)
    isread = models.CharField(max_length=50)
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.id

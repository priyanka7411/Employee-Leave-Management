from django import template
from employeeleave.models import *
register = template.Library()




@register.simple_tag()
def employeeid(pid,*args, **kwargs):
    user = User.objects.get(id=pid)
    employee = Employee.objects.get(user = user)
    return employee.empid
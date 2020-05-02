import requests, json
from django.urls import reverse
from django.shortcuts import render
from rest_framework import viewsets
# from django.core import serializers
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.db import connection
from django.contrib.auth.models import User
from hrm.serializers import EmployeeTypeSerializer, ProductSerializer
from hrm.models import EmployeeType, Product
# Create your views here.


@login_required
def index(request):
    cursor = connection.cursor()
    cursor.execute('''
    select type.name, emp.type_count from hrm_employeetype as type,
    (select count(type_id) as type_count, type_id from hrm_employee group by type_id) as emp
    where emp.type_id = type.id 
    ''')
    row = cursor.fetchall()
    data = [['Product', 'Type per Emp']]+[list(i) for i in row]
    return render(request, 'hrm/home.html', {'data': json.dumps(data)})
    # if request.user.is_authenticated:
    #     return render(request, 'hrm/home.html')
    # else:
    #     return render(request, 'hrm/login.html')


@login_required
def user_logout(request):
    logout(request)
    return render(request, 'hrm/login.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'hrm/login.html')


def user_register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            User.objects.create_user(username=username, email=email, password=password, is_staff=True)
        except:
            return HttpResponse("User creation data is wrong.")
        return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'hrm/register.html')


def user_restpassword(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user_obj = User.objects.get(username=username)
            user_obj.set_password(password)
            user_obj.save()
        except:
            return HttpResponse("User Does Not Exist")
        return HttpResponseRedirect(reverse('login'))
    else:
        return render(request, 'hrm/password.html')


def employee_table(request):
    url_path = request.build_absolute_uri(reverse('emp_record'))
    response = requests.get(url_path, params=request.GET, json={})
    tabledetails = response.json()
    return render(request,'hrm/employee_table.html',{'tabledetails': tabledetails})


def employee_form(request, pk=''):
    emp_type = EmployeeType.objects.values_list('name', flat=True)
    product_list = Product.objects.values_list('name', flat=True)
    return render(request, 'hrm/employee_form.html', {'pk': pk, 'emp_type': emp_type,'product_list':product_list})


class EmployeeTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSets define the view behavior.
    API endpoint that allows EmployeeType to be viewed or edited.
    """
    lookup_field = 'id'
    serializer_class = EmployeeTypeSerializer

    def get_queryset(self):
        return EmployeeType.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSets define the view behavior.
    API endpoint that allows Product to be viewed or edited.
    """
    lookup_field = 'id'
    serializer_class = ProductSerializer

    def get_queryset(self):
        return Product.objects.all()
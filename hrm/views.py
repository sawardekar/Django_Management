import requests
# from django.http import HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
# from django.core import serializers
from hrm.serializers import EmployeeTypeSerializer, ProductSerializer
from hrm.models import EmployeeType, Product
# Create your views here.


def index(request):
    # return HttpResponse("Successfully created Employee app")
    return render(request, 'hrm/home.html')


def employee_table(request):
    from django.urls import reverse
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
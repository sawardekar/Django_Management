from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser
from rest_framework import status
from django.http import Http404
# from django.shortcuts import get_object_or_404
from hrm.models import Employee
from hrm.serializers import EmployeeSerializer


class EmployeeDetail(APIView):
    """
    Serializers define the API representation.
    """
    parser_class = (FileUploadParser,)

    def get_object(self, pk):
        try:
            return Employee.objects.select_related('type').prefetch_related('product').get(pk=pk)
        except Employee.DoesNotExist:
            raise Http404

    def get(self, request, pk=None):
        if pk:
            employee = self.get_object(pk)
            serializer = EmployeeSerializer(employee)
        else:
            employee = Employee.objects.all().select_related('type').prefetch_related('product')
            serializer = EmployeeSerializer(employee, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        if request.data.__contains__('product'):
            if isinstance(request.data['product'], str) and len(request.data['product']):
                product_list = (request.data['product']).split(",")
                request.data.setlist('product', product_list)
            if not len(request.data['product']):
                request.data.pop('product')
        if request.data.__contains__('type'):
            if isinstance(request.data['type'], str) and not len(request.data['type']):
                request.data['type'] = None
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        if not request.POST._mutable:
            request.POST._mutable = True
        employee = self.get_object(pk)
        if request.data.__contains__('product'):
            if isinstance(request.data['product'], str) and len(request.data['product']):
                product_list = (request.data['product']).split(",")
                request.data.setlist('product', product_list)
            if not len(request.data['product']):
                request.data.pop('product')
        if request.data.__contains__('type'):
            if isinstance(request.data['type'], str) and not len(request.data['type']):
                request.data['type'] = None
        serializer = EmployeeSerializer(employee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        employee = self.get_object(pk)
        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

from django.urls import path, include
from rest_framework import routers
from hrm import views
from hrm.apiviews import EmployeeDetail

router = routers.DefaultRouter()
router.register(r'type', views.EmployeeTypeViewSet, basename="type")
router.register(r'product', views.ProductViewSet, basename="product")

urlpatterns = [
    path('index', views.index, name='index'),
    path('employee', views.employee_table, name="employee_table"),
    path('employee/', views.employee_form, name="employee_create"),
    path('employee/<int:pk>', views.employee_form, name="employee_modified"),
    path('', include(router.urls)),
    path('emp/', EmployeeDetail.as_view(), name="emp_record"),
    path('emp/<int:pk>/', EmployeeDetail.as_view(), name="emp_modified"),
]


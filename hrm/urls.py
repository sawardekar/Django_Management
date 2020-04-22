from django.urls import path, include
from rest_framework import routers
from hrm import views
from hrm.apiviews import EmployeeDetail

router = routers.DefaultRouter()
router.register(r'type', views.EmployeeTypeViewSet, basename="type")
router.register(r'product', views.ProductViewSet, basename="product")

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    path('register', views.user_register, name='register'),
    path('restpassword', views.user_restpassword, name='restpassword'),
    path('employee', views.employee_table, name="employee_table"),
    path('employee/', views.employee_form, name="employee_create"),
    path('employee/<int:pk>', views.employee_form, name="employee_modified"),
    path('viewset/', include(router.urls)),
    path('emp/', EmployeeDetail.as_view(), name="emp_record"),
    path('emp/<int:pk>/', EmployeeDetail.as_view(), name="emp_modified"),
]


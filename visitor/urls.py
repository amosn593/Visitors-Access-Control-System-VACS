from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="home" ),
    path('visitor_register', views.visitor_register, name="register" ),
    path('check_out', views.check_out, name="check_out" ),
    path('profile_view', views.profile, name="profile" ),
    path('staff_cars', views.car_index, name="staff_cars" ),
    path('staff_car_register', views.car_register, name="car_register" ),
    path('car_check_out', views.car_check_out, name="car_check_out" ),
    path('interns_index', views.interns_index, name="interns" ),
    path('intern_register', views.intern_register, name="intern_register" ),
    path('intern_check_out', views.intern_check_out, name="intern_check_out" ),
    path('reports', views.report_index, name="reports" ),
    path('report_generation', views.report_generate, name="report_generation" ),
]
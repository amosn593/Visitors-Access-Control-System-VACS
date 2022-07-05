from django.db import models
from django.conf import settings

# Create your models here.

# Station Model


class Station(models.Model):
    station_name = models.CharField(max_length=40)

    def __str__(self):
        return self.station_name

# Profile model


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True,  on_delete=models.SET_NULL)
    station = models.ForeignKey(Station, null=True,  on_delete=models.SET_NULL)
    full_name = models.CharField(
        max_length=40, blank=True, default="Full Name")
    id_number = models.CharField(
        max_length=15, blank=True, default="ID Number")
    staff_number = models.CharField(
        max_length=20, blank=True, default="Staff Number")
    staff_phone = models.CharField(
        max_length=15, blank=True, default="Staff Phone")

    def __str__(self):
        return self.user.username

# Visitor


class Visitor(models.Model):
    full_name = models.CharField(max_length=40)
    id_number = models.CharField(max_length=40)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=100)
    target_office = models.CharField(max_length=40)
    purpose = models.CharField(max_length=100)
    vehicle_reg = models.CharField(max_length=20, default="None")
    vehicle_occupants = models.CharField(max_length=20, default=0, null=True)
    time_in = models.DateTimeField(auto_now_add=True, null=True)
    time_out = models.DateTimeField(blank=True, null=True)
    station = models.ForeignKey(Station, null=True,  on_delete=models.SET_NULL)
    staff_checkedin = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,  on_delete=models.SET_NULL)
    staff_checkedout = models.CharField(max_length=40, blank=True,  null=True)
    status = models.CharField(max_length=40, default="OPEN")

    def __str__(self):
        return f"{self.full_name} - {self.phone_number} - {self.id_number}"

# Car


class Car(models.Model):
    plate_number = models.CharField(max_length=40)
    vehicle_occupants = models.CharField(max_length=10, default=1)
    driver = models.CharField(max_length=70)
    purpose = models.CharField(max_length=30, default="Staff")
    time_in = models.DateTimeField(auto_now_add=True, null=True)
    time_out = models.DateTimeField(blank=True, null=True)
    station = models.ForeignKey(Station, null=True,  on_delete=models.SET_NULL)
    staff_checkedin = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,  on_delete=models.SET_NULL)
    staff_checkedout = models.CharField(max_length=40, blank=True,  null=True)
    status = models.CharField(max_length=40, default="OPEN")

    def __str__(self):
        return f"{self.plate_number}, - {self.driver}, - {self.time_in}"

# Student


class Student(models.Model):
    name = models.CharField(max_length=50)
    id_card = models.CharField(max_length=15, unique=True)
    phone = models.CharField(max_length=15)
    email = models.CharField(max_length=40)
    department = models.CharField(max_length=30)
    supervisor = models.CharField(max_length=30)
    status = models.CharField(max_length=40, default="ACTIVE")

    def __str__(self):
        return f"{self.name}, - {self.id_card}, - {self.status}"

# Register


class Register(models.Model):
    student = models.ForeignKey(Student, null=True,  on_delete=models.SET_NULL)
    time_in = models.DateTimeField(auto_now_add=True, null=True)
    time_out = models.DateTimeField(blank=True, null=True)
    station = models.ForeignKey(Station, null=True,  on_delete=models.SET_NULL)
    staff_checkedin = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True,  on_delete=models.SET_NULL)
    staff_checkedout = models.CharField(max_length=40, blank=True,  null=True)
    status = models.CharField(max_length=40, default="OPEN")

    def __str__(self):
        return f"{self.student.name}, - {self.time_in}, - {self.status}"

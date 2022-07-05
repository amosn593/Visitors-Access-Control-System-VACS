from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from .models import *
from .filter import *
from datetime import datetime
import csv

# Create your views here.

# Visitors Views


@login_required()
def index(request):
    station = request.user.profile.station
    station_name = station.station_name
    if request.method == "GET":
        visitors = Visitor.objects.filter(
            station=station, status="OPEN").order_by('-time_in')
        count = visitors.count()
        date = datetime.now()
        context = {
            'visitors': visitors,
            'count': count,
            'date': date,
            'station_name': station_name,
        }
        return render(request, 'visitor/home.html', context)
    if request.method == "POST":
        id_number = request.POST['id_number'].strip()
        try:
            visitors = Visitor.objects.filter(
                id_number=id_number, station=station, status="OPEN").order_by('-time_in')
            count = visitors.count()
            if count > 0:
                date = datetime.now()
                context = {
                    'visitors': visitors,
                    'count': count,
                    'date': date,
                    'station_name': station_name,
                }
                return render(request, 'visitor/home.html', context)
            else:
                messages.error(
                    request, 'Visitor not found, Kindly confirm ID No. !!!')
                return redirect("home")

        except:
            messages.error(request, 'Something went wrong, try again!!!')
            return redirect("home")
    else:
        return HttpResponse("Invalid URL")


@login_required()
def visitor_register(request):
    if request.method == "POST":
        user = request.user
        station = user.profile.station
        name = request.POST["full_name"].strip()
        id = request.POST["id_number"].strip()
        mobile = request.POST["mobile_number"].strip()
        address = request.POST["address"].strip()
        vehicle = request.POST["vehicle_reg"].strip()
        vehicle_occupants = request.POST["vehicle_occupants"].strip()
        dpt = request.POST["visit_dpt"].strip()
        purpose = request.POST["purpose_visit"].strip()

        try:
            visitor = Visitor(full_name=name, id_number=id, phone_number=mobile, address=address, target_office=dpt,
                              purpose=purpose, vehicle_reg=vehicle, vehicle_occupants=vehicle_occupants, station=station, staff_checkedin=user)
            visitor.save()
            messages.success(request, 'Visitor Booked Successfully!!!')

            return redirect("home")
        except:
            messages.error(request, 'Something went wrong, try again!!!')
            return redirect("home")

    if request.method == "GET":
        return HttpResponse("Invalid URL")

    else:
        return HttpResponse("Invalid URL")


@login_required()
def check_out(request):
    if request.method == "GET":
        user = request.user.profile.full_name
        date = datetime.now()
        id = request.GET["id"]
        if Visitor.objects.get(id=id).status == "OPEN":
            visitor = Visitor.objects.filter(id=id)
            visitor.update(time_out=date, staff_checkedout=user,
                           status="Checked Out")
            messages.success(request, 'Visitor Checked Out Successfully!!!')
            return redirect("home")
        else:
            messages.error(request, 'Something went wrong, try again!!!')
            return redirect("home")
    if request.method == "POST":
        return HttpResponse("Invalid URL")
    else:
        return HttpResponse("Invalid URL")


@login_required()
def profile(request):
    if request.method == "GET":
        try:
            user = request.user
            context = {
                'user': user,

            }
            return render(request, 'visitor/profile/profile.html', context)
        except:
            messages.error(request, 'Something went wrong, try again!!!')
            return redirect("home")
    else:
        return HttpResponse("Invalid URL")


# Cars viws
@login_required()
def car_index(request):
    station = request.user.profile.station
    station_name = station.station_name
    if request.method == "GET":
        cars = Car.objects.filter(
            station=station, status="OPEN").order_by('-time_in')
        count = cars.count()
        date = datetime.now()
        context = {
            'cars': cars,
            'count': count,
            'date': date,
            'station_name': station_name,
        }
        return render(request, 'visitor/cars/index.html', context)
    if request.method == "POST":
        id_number = request.POST['id_number'].strip()
        try:
            cars = Car.objects.filter(
                plate_number=id_number, station=station, status="OPEN").order_by('-time_in')
            count = cars.count()
            if count > 0:
                date = datetime.now()
                context = {
                    'cars': cars,
                    'count': count,
                    'date': date,
                    'station_name': station_name,
                }
                return render(request, 'visitor/cars/index.html', context)
            else:
                messages.error(
                    request, 'Car not found, Kindly confirm Plate No. !!!')
                return redirect("staff_cars")
        except:
            messages.error(request, 'Something went wrong, try again!!!')
            return redirect("staff_cars")
    else:
        return HttpResponse("Invalid URL")


# Staff & Organization car registrations
@login_required()
def car_register(request):
    if request.method == "POST":
        user = request.user
        station = user.profile.station
        plate = request.POST["plate_number"].strip()
        driver = request.POST["driver"].strip()
        vehicle_occupants = request.POST["vehicle_occupants"].strip()
        try:
            car = Car(plate_number=plate, driver=driver,
                      vehicle_occupants=vehicle_occupants,
                      station=station, staff_checkedin=user)
            car.save()
            messages.success(request, 'Staff Car Booked Successfully!!!')
            return redirect("staff_cars")
        except:
            messages.error(request, 'Something went wrong, try again!!!')
            return redirect("staff_cars")

    if request.method == "GET":
        return HttpResponse("Invalid URL")
    else:
        return HttpResponse("Invalid URL")


@login_required()
def car_check_out(request):
    if request.method == "GET":
        user = request.user.profile.full_name
        date = datetime.now()
        id = request.GET["id"]
        try:
            if Car.objects.get(id=id).status == "OPEN":
                car = Car.objects.filter(id=id)
                car.update(time_out=date, staff_checkedout=user,
                           status="Checked Out")
                messages.success(
                    request, 'Staff Car checked Out successfully!!!')
                return redirect("staff_cars")
            else:
                messages.error(
                    request, 'Something went Wrong, kindly try again!!!')
                return redirect("staff_cars")
        except:
            messages.error(
                request, 'Something went Wrong, kindly try again!!!')
            return redirect("staff_cars")
    if request.method == "POST":
        return HttpResponse("Invalid URL")
    else:
        return HttpResponse("Invalid URL")


# STUDENTS views
@login_required()
def interns_index(request):
    station = request.user.profile.station
    station_name = station.station_name
    if request.method == "GET":
        registers = Register.objects.filter(
            station=station, status="OPEN").order_by('-time_in')
        count = registers.count()
        date = datetime.now()
        context = {
            'registers': registers,
            'count': count,
            'date': date,
            'station_name': station_name,
        }
        return render(request, 'visitor/interns/index.html', context)
    if request.method == "POST":
        id_number = request.POST['id_number'].strip()
        try:
            student = Student.objects.get(id_card=id_number, status="ACTIVE")
        except:
            student = None
        try:
            registers = Register.objects.filter(
                student=student, station=station, status="OPEN").order_by('-time_in')
        except:
            registers = None
        if registers:
            count = registers.count()
            date = datetime.now()
            context = {
                'registers': registers,
                'count': count,
                'date': date,
                'station_name': station_name,
            }
            return render(request, 'visitor/interns/index.html', context)
        else:
            messages.error(
                request, 'Something went wrong, Check ID No. and try again!!!')
            return redirect("interns")

    else:
        return HttpResponse("Invalid URL")


@login_required()
def intern_register(request):
    if request.method == "POST":
        user = request.user
        station = user.profile.station
        id_card = request.POST["id_number"].strip()
        try:
            student = Student.objects.get(id_card=id_card, status="ACTIVE")
        except:
            student = None
        if student:
            try:
                register = Register(
                    station=station, staff_checkedin=user, student=student)
                register.save()
                messages.success(request, 'Student registered successfully!!!')
                return redirect("interns")
            except:
                messages.error(
                    request, 'Something went Wrong, kindly try again!!!')
                return redirect("interns")
        else:
            messages.error(
                request, 'Student inactive or Already Registered, confirm ID No.!!!')
            return redirect("interns")

    if request.method == "GET":
        return HttpResponse("Invalid URL")

    else:
        return HttpResponse("Invalid URL")


@login_required()
def intern_check_out(request):
    if request.method == "GET":
        user = request.user.profile.full_name
        date = datetime.now()
        id = request.GET["id"]
        try:
            if Register.objects.get(id=id).status == "OPEN":
                register = Register.objects.filter(id=id)
                register.update(
                    time_out=date, staff_checkedout=user, status="Checked Out")
                messages.success(
                    request, 'Student checked Out successfully!!!')
                return redirect("interns")
            else:
                messages.error(
                    request, 'Something went Wrong, kindly try again!!!')
                return redirect("interns")
        except:
            messages.error(
                request, 'Something went Wrong, kindly try again!!!')
            return redirect("interns")
    if request.method == "POST":
        return HttpResponse("Invalid URL")
    else:
        return HttpResponse("Invalid URL")


# Reports
@login_required()
def report_index(request):
    if request.method == "GET":
        try:
            return render(request, 'visitor/reports/index.html')
        except:
            messages.error(
                request, 'Something went wrong, contact administrator!!!')
            return redirect("home")

    else:
        return HttpResponse("Invalid URL")


@login_required()
def report_generate(request):
    if request.method == "POST":
        # Getting posted data
        report_type = request.POST["report_type"].strip()
        start_date = request.POST["start_date"]
        end_date = request.POST["end_date"]

        # Checking if start_date <= end_date
        if start_date > end_date:
            messages.error(
                request, "End date must be greater or equal to Start date!!!")
            return redirect("reports")
        elif start_date <= end_date:

            # Checking report type to generate
            # Visitors CSV report
            if report_type == '1':
                try:
                    visitors = Visitor.objects.filter(
                        time_in__range=(start_date, end_date))
                except:
                    messages.error(
                        request, "Unable to connect with database, kindly try again!!!")
                    return redirect("reports")

                # Generating report only if records found
                if visitors.count() > 0:
                    header = ['Full Name', 'ID NO.', 'Phone No.', 'Address', 'Vehicle Plate', 'Visiting Office',
                              'Purpose', 'Station', 'Time In', 'Time Out', 'Staff Checking In', 'Staff Checking Out', 'Status']
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="Visitors_Report.csv"'
                    writer = csv.writer(response)
                    writer.writerow(header)
                    for v in visitors:
                        writer.writerow([v.full_name, v.id_number, v.phone_number, v.address, v.vehicle_reg, v.target_office, v.purpose,
                                        v.station.station_name, v.time_in, v.time_out, v.staff_checkedin.profile.full_name, v.staff_checkedout, v.status])

                    print(f"{report_type}, {start_date}, {end_date}")
                    return response
                else:
                    messages.error(
                        request, "No Records Found, kindly try another dates!!!")
                    return redirect("reports")

            # Interns/Attachees CSV report
            elif report_type == '2':
                try:
                    registers = Register.objects.filter(
                        time_in__range=(start_date, end_date))
                except:
                    messages.error(
                        request, "Unable to connect with database, kindly try again!!!")
                    return redirect("reports")

                # Generating report only if records found
                if registers.count() > 0:
                    header = ['Full Name', 'ID NO.', 'Phone No.', 'Email', 'Department', 'Supervisor',
                              'Station', 'Time In', 'Time Out', 'Staff Checking In', 'Staff Checking Out', 'Status']
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="Interns_Attachees_Report.csv"'
                    writer = csv.writer(response)
                    writer.writerow(header)
                    for r in registers:
                        writer.writerow([r.student.name, r.student.id_card, r.student.phone, r.student.email, r.student.department, r.student.supervisor,
                                        r.station.station_name, r.time_in, r.time_out, r.staff_checkedin.profile.full_name, r.staff_checkedout, r.status])
                    return response
                else:
                    messages.error(
                        request, "No Records Found, kindly try another dates!!!")
                    return redirect("reports")

            # Staff Cars  CSV Reports
            elif report_type == '3':
                try:
                    cars = Car.objects.filter(
                        time_in__range=(start_date, end_date))
                except:
                    messages.error(
                        request, "Unable to connect with database, kindly try again!!!")
                    return redirect("reports")

                # Generating report only if records found
                if cars.count() > 0:
                    header = ['Driver', 'Plate NO.', 'Purpose', 'Station', 'Time In',
                              'Time Out', 'Staff Checking In', 'Staff Checking Out', 'Status']
                    response = HttpResponse(content_type='text/csv')
                    response['Content-Disposition'] = 'attachment; filename="Staff_Cars_Report.csv"'
                    writer = csv.writer(response)
                    writer.writerow(header)
                    for c in cars:
                        writer.writerow([c.driver, c.plate_number, c.purpose, c.station.station_name, c.time_in,
                                        c.time_out, c.staff_checkedin.profile.full_name, c.staff_checkedout, c.status])
                    return response
                else:
                    messages.error(
                        request, "No Records Found, kindly try another dates!!!")
                    return redirect("reports")

            else:
                messages.error(request, "Select valid report type!!!")
                return redirect("reports")

        else:
            messages.error(
                request, "Something went wrong, kindly try again!!!")
            return redirect("reports")
    else:
        return HttpResponse("Invalid URL")

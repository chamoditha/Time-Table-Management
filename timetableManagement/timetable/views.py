from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from timetable.models import Schedule, TimeSlot, Year, Subject, Hall, Lecturer
from .forms import ScheduleForm
from django.db import IntegrityError
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User

def login_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate the user
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:  # Check if the user is a superuser
                login(request, user)
                return redirect('dashboard')  # Redirect to the dashboard
            else:
                error = "Only superusers are allowed to log in."
        else:
            error = "Invalid username or password."

    return render(request, 'login.html', {'error': error})



def dashboard_view(request):
    # Fetch all required data
    lecturers = Lecturer.objects.all()  # Get all lecturers
    time_slots = TimeSlot.objects.all()
    years = Year.objects.all()
    subjects = Subject.objects.all()
    halls = Hall.objects.all()
    schedules = Schedule.objects.all().order_by('year__name', 'timeslot__start_time')
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

    context = {
        'lecturers': lecturers,  # Pass lecturers to the template
        'time_slots': time_slots,
        'years': years,
        'subjects': subjects,
        'halls': halls,
        'schedules': schedules,
        'days': days,
    }
    return render(request, 'dashboard.html', context)

   



def get_date_from_day(day_name):
    today = datetime.now()
    days_map = {
        "Monday": 0,
        "Tuesday": 1,
        "Wednesday": 2,
        "Thursday": 3,
        "Friday": 4,
    }
    # Find the next occurrence of the selected day
    target_day = days_map[day_name]
    days_ahead = (target_day - today.weekday() + 7) % 7
    return today + timedelta(days=days_ahead)



def add_schedule(request):
    if request.method == 'POST':
        day = request.POST.get('day')
        timeslot_id = request.POST.get('timeslot')
        year_id = request.POST.get('year')
        subject_id = request.POST.get('subject')
        hall_id = request.POST.get('hall')
        lecturer_id = request.POST.get('lecturer')

        try:
            # Attempt to save the schedule
            Schedule.objects.create(
                day=day,
                timeslot_id=timeslot_id,
                year_id=year_id,
                subject_id=subject_id,
                hall_id=hall_id,
                lecturer_id=lecturer_id,
            )
            return redirect('dashboard')  # Redirect to dashboard if successful
        except IntegrityError as e:
            # Handle the unique constraint violation
            error_message = "The selected year already has a lecture at this time.: "
            if 'unique_schedule_per_timeslot' in str(e):
                error_message += "The selected year already has a lecture at this time."
            elif 'unique_lecturer_per_timeslot' in str(e):
                error_message += "The selected lecturer is already teaching another lecture at this time."
            elif 'unique_hall_per_timeslot' in str(e):
                error_message += "The selected hall is already being used for another lecture at this time."
            else:
                error_message += ""

            # Re-render the dashboard with an error message
            return render(request, 'dashboard.html', {
                'error': error_message,
                'days': ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
                'time_slots': TimeSlot.objects.all(),
                'years': Year.objects.all(),
                'subjects': Subject.objects.all(),
                'halls': Hall.objects.all(),
                'lecturers': Lecturer.objects.all(),
                'schedules': Schedule.objects.all(),
            })

def edit_schedule(request):
    if request.method == 'POST':
        schedule_id = request.POST.get('schedule_id')
        schedule = get_object_or_404(Schedule, id=schedule_id)
        schedule.subject_id = request.POST.get('subject')
        schedule.hall_id = request.POST.get('hall')
        schedule.lecturer_id = request.POST.get('lecturer')
        schedule.save()

    return redirect('dashboard')


def register_view(request):
    error = None
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check for validation errors
        if password != password2:
            error = "Passwords do not match."
        elif len(password) < 6:
            error = "Password must be at least 6 characters long."
        elif User.objects.filter(username=username).exists():
            error = "Username already exists."
        elif User.objects.filter(email=email).exists():
            error = "Email already exists."
        else:
            # Create the superuser
            User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            return redirect('login')  # Redirect to login after successful registration

    return render(request, 'register.html', {'error': error})
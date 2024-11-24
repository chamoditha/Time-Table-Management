from django.db import models

# Year model for organizing students by year
class Year(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# Subject model with subject code
class Subject(models.Model):
    subject_code = models.CharField(max_length=10, unique=True)  # Subject code added
    name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.subject_code} - {self.name}"


# Lecturer model with name, email, and role
class Lecturer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=100)

    def __str__(self):
        return self.name


# Hall model with hall name
class Hall(models.Model):
    name = models.CharField(max_length=20)  # Hall name

    def __str__(self):
        return self.name


# TimeSlot model for time periods
class TimeSlot(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.start_time} - {self.end_time}"


# Schedule model for creating a timetable



class Schedule(models.Model):
    day = models.CharField(
        max_length=10,
        choices=[
            ("Monday", "Monday"),
            ("Tuesday", "Tuesday"),
            ("Wednesday", "Wednesday"),
            ("Thursday", "Thursday"),
            ("Friday", "Friday"),
        ]
    )
    timeslot = models.ForeignKey('TimeSlot', on_delete=models.CASCADE)
    year = models.ForeignKey('Year', on_delete=models.CASCADE)
    subject = models.ForeignKey('Subject', on_delete=models.CASCADE)
    hall = models.ForeignKey('Hall', on_delete=models.CASCADE)
    lecturer = models.ForeignKey('Lecturer', on_delete=models.CASCADE)

    class Meta:
        constraints = [
           
            models.UniqueConstraint(fields=['day', 'timeslot', 'year'], name='unique_schedule_per_timeslot'),
            models.UniqueConstraint(fields=['day', 'timeslot', 'lecturer'], name='unique_lecturer_per_timeslot'),
            models.UniqueConstraint(fields=['day', 'timeslot', 'hall'], name='unique_hall_per_timeslot'),
        ]

    def __str__(self):
        return f"{self.day} | {self.timeslot} | {self.year}"





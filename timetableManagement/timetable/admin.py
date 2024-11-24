from django.contrib import admin
from .models import Year, Subject, Lecturer, Hall, TimeSlot, Schedule

# Registering all models
admin.site.register(Year)
admin.site.register(Subject)
admin.site.register(Lecturer)
admin.site.register(Hall)
admin.site.register(TimeSlot)
admin.site.register(Schedule)
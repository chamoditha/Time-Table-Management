from django import forms
from .models import Schedule

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['day', 'timeslot', 'year', 'subject', 'hall', 'lecturer']

    def clean(self):
        cleaned_data = super().clean()
        day = cleaned_data.get('day')
        timeslot = cleaned_data.get('timeslot')
        year = cleaned_data.get('year')
        lecturer = cleaned_data.get('lecturer')
        hall = cleaned_data.get('hall')

        # Check for conflicts
        if Schedule.objects.filter(day=day, timeslot=timeslot, year=year).exists():
            raise forms.ValidationError("The selected year already has a lecture at this time.")
        if Schedule.objects.filter(day=day, timeslot=timeslot, lecturer=lecturer).exists():
            raise forms.ValidationError("The selected lecturer is already teaching another lecture at this time.")
        if Schedule.objects.filter(day=day, timeslot=timeslot, hall=hall).exists():
            raise forms.ValidationError("The selected hall is already being used for another lecture at this time.")

        return cleaned_data
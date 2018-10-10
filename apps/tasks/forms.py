from django import forms

from djcelery.models import CrontabSchedule, IntervalSchedule, PeriodicTask

__all__ = ['PeriodicTaskForm', 'CrontabScheduleForm', 'IntervalScheduleForm']


class PeriodicTaskForm(forms.ModelForm):
    class Meta:
        model = PeriodicTask
        fields = '__all__'


class CrontabScheduleForm(forms.ModelForm):
    class Meta:
        model = CrontabSchedule
        fields = '__all__'


class IntervalScheduleForm(forms.ModelForm):
    class Meta:
        model = IntervalSchedule
        fields = '__all__'

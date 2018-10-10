from django import forms

from apps.jobs.models import JobInfo, JobType

__all__ = ['JobTypeForm', 'JobForm']


class JobTypeForm(forms.ModelForm):
    class Meta:
        model = JobType
        fields = '__all__'


class JobForm(forms.ModelForm):
    class Meta:
        model = JobInfo
        fields = '__all__'

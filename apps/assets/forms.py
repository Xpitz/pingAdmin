from django import forms

from apps.assets.models import AssetInfo, AssetGroup

__all__ = ['FileForm', 'AssetGroupForm', 'AssetForm']


class FileForm(forms.Form):
    file = forms.FileField()


class AssetGroupForm(forms.ModelForm):
    class Meta:
        model = AssetGroup
        fields = '__all__'


class AssetForm(forms.ModelForm):
    class Meta:
        model = AssetInfo
        exclude = ['os', 'os_release', 'mem_total', 'cpu_model', 'cpu_count', 'sn']

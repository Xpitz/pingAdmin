from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class JobType(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Job Type Name'), unique=True)
    comment = models.TextField(verbose_name=_('Comment'), blank=True, null=True)

    class Meta:
        db_table = 'JobType'
        verbose_name = _('Job Type')
        verbose_name_plural = _('Job Type')

    def __str__(self):
        return self.name


class JobInfo(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Job Name'), unique=True)
    content = models.TextField(verbose_name=_('Content'), blank=True, null=True)
    comment = models.TextField(verbose_name=_('Comment'), blank=True, null=True)
    types = models.ForeignKey(to='JobType', on_delete=models.CASCADE, blank=True, verbose_name=_('Job Type'))

    class Meta:
        db_table = 'JobInfo'
        verbose_name = _('Job Info')
        verbose_name_plural = _('Job Info')

    def __str__(self):
        return self.name

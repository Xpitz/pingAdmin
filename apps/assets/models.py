from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.

class AssetGroup(models.Model):
    name = models.CharField(max_length=64, verbose_name=_('Asset Group Name'), unique=True)
    comment = models.TextField(verbose_name=_('Comment'), blank=True, null=True)

    class Meta:
        db_table = 'AssetGroup'
        verbose_name = _('Asset Group')
        verbose_name_plural = _('Asset Group')

    def __str__(self):
        return self.name


class AssetInfo(models.Model):
    # basic info
    hostname = models.CharField(max_length=64, verbose_name=_('Hostname'), unique=True)
    outer_ip = models.GenericIPAddressField(max_length=32, verbose_name=_('Outer IP'), null=True, blank=True)
    inner_ip = models.GenericIPAddressField(max_length=32, verbose_name=_('Inner IP'), null=True, blank=True)
    port = models.IntegerField(default=22, verbose_name=_('Port'), null=True, blank=True)
    username = models.CharField(max_length=64, verbose_name=_('Username'), null=True, blank=True)
    password = models.CharField(max_length=128, verbose_name=_('Auth Password'), default='', blank=True)
    groups = models.ForeignKey(to='AssetGroup', verbose_name=_('Asset Group'), on_delete=models.SET_NULL, blank=True, null=True)
    # system info from salt
    os = models.CharField(max_length=64, verbose_name=_('OS'), null=True, blank=True)
    os_release = models.CharField(max_length=32, verbose_name=_('OS Release'), null=True, blank=True)
    cpu_model = models.CharField(max_length=64, verbose_name=_('CPU Model'), null=True, blank=True)
    cpu_count = models.IntegerField(null=True, verbose_name=_('CPU Count'))
    mem_total = models.CharField(max_length=64, verbose_name=_('Memory Total'), null=True, blank=True)
    sn = models.CharField(max_length=64, verbose_name=_('Serial Number'), null=True, blank=True)

    class Meta:
        db_table = 'AssetInfo'
        verbose_name = _('Asset Info')
        verbose_name_plural = _('Asset Info')

    def __str__(self):
        return self.hostname

# -*- coding: utf-8 -*-
def get_object_or_none(model, **kwargs):
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None
    return obj


def get_queryset_or_none(model, **kwargs):
    try:
        obj_queryset = model.objects.filter(**kwargs)
    except model.DoesNotExist:
        return None
    return obj_queryset

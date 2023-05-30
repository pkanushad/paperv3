import django_filters

from .models import *


class HistoryFilter(django_filters.FilterSet):
    class Meta:
        model =FutureBlotterModel
        fields ='__all__'

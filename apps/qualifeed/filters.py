from django_filters import rest_framework as filters
from .models import Product,ProductCategory, Caracterstic , Brand, Control, Defect, DefectType, CheckControl, Box
from django_filters.rest_framework import DjangoFilterBackend
from django.db import models


        
class ControlFilterSet(filters.FilterSet):
    class Meta:
        model = Control
        fields = ['photo_control','details_control','date_control','time_control','state_control','serial_code','user']
        filter_overrides = {
            models.ImageField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }
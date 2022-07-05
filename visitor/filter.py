import django_filters
from .models import *

class IdFilter(django_filters.FilterSet):
    id_number = django_filters.CharFilter(lookup_expr='icontains', label="ID NO.")
    
    class Meta:
        model = Visitor
        fields = ['id_number']
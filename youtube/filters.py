from .models import User, Video
import django_filters
from django.db import models

class VideoFilter(django_filters.FilterSet):
    class Meta:
        model = Video
        fields = ['caption']
        filter_overrides = {
             models.CharField: {
                 'filter_class': django_filters.CharFilter,
                 'extra': lambda f: {
                     'lookup_expr': 'icontains',
                 },
             },
         }


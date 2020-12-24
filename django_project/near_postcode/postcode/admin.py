from django.contrib import admin
from .models import Postcode, Coordinate


@admin.register(Postcode)
class PostcodeAdmin(admin.ModelAdmin):
    list_display = ['code', 'country', 'nhs_ha']


@admin.register(Coordinate)
class CoordinateAdmin(admin.ModelAdmin):
    list_display = ['lat', 'lon']

from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.urls import path

from django.contrib import admin
from .models import Class, Pupil, Dish, DailyMenu, WeeklyBreakfasts


@admin.register(Pupil)
class PupilAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'class_group']
    list_filter = ['class_group']
    search_fields = ['last_name', 'first_name']


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


@admin.register(DailyMenu)
class DailyMenuAdmin(admin.ModelAdmin):
    list_display = ['date', 'option_1', 'option_2']
    list_filter = ['date']
    date_hierarchy = 'date'


@admin.register(WeeklyBreakfasts)
class WeeklyBreakfastAdmin(admin.ModelAdmin):
    list_display = ['pupil', 'get_class_group', 'monday', 'tuesday', 'wednesday', 'thursday', 'friday',
                    'week_start_date', 'choices_count']
    list_filter = ['pupil__class_group', 'week_start_date']
    search_fields = ['pupil__first_name', 'pupil__last_name']

    def get_class_group(self, obj):
        return obj.pupil.class_group

    get_class_group.short_description = 'Класс'

    def choices_count(self, obj):
        count = sum([1 for field in [obj.monday, obj.tuesday, obj.wednesday,
                                     obj.thursday, obj.friday] if field])
        return f"{count}/5"

    choices_count.short_description = 'Выбрано'

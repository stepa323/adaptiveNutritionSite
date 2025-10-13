from django.contrib import admin
from .models import Class, Pupil, Dish, DailyMenu, BreakfastChoice

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

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

@admin.register(BreakfastChoice)
class BreakfastChoiceAdmin(admin.ModelAdmin):
    list_display = ['pupil', 'date', 'chosen_dish']
    list_filter = ['date', 'pupil__class_group']
    date_hierarchy = 'date'

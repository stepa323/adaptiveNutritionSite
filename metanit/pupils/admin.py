from datetime import datetime, timedelta

from django.http import HttpResponseRedirect
from django.urls import path

from django.contrib import admin
from django.db.models import Count
from django.shortcuts import render
from django.utils.html import format_html

from .models import Class, Pupil, Dish, DailyMenu, BreakfastChoice


@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']


    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('weekly-reports/', self.weekly_reports, name='weekly-reports'),
        ]
        return custom_urls + urls

    def weekly_reports(self, request):
        today = datetime.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        week_dates = [start_of_week + timedelta(days=i) for i in range(5)]

        selected_classes = request.GET.getlist('classes')
        all_classes = Class.objects.all().order_by('name')

        if not selected_classes:
            classes_to_show = all_classes
        else:
            classes_to_show = all_classes.filter(id__in=selected_classes)

        report_data = []
        for class_obj in classes_to_show:
            class_data = {
                'class': class_obj,
                'pupils': []
            }

            pupils = class_obj.pupil_set.all().order_by('last_name', 'first_name')

            for pupil in pupils:
                pupil_data = {
                    'pupil': pupil,
                    'daily_choices': []
                }

                for date in week_dates:
                    try:
                        choice = BreakfastChoice.objects.get(pupil=pupil, date=date)
                        pupil_data['daily_choices'].append(choice.chosen_dish.name)
                    except BreakfastChoice.DoesNotExist:
                        pupil_data['daily_choices'].append('—')

                class_data['pupils'].append(pupil_data)

            report_data.append(class_data)

        # Статистика
        dish_statistics_list = []
        for date in week_dates:
            stats = BreakfastChoice.objects.filter(date=date).values(
                'chosen_dish__name'
            ).annotate(
                total=Count('id')
            ).order_by('-total')

            dish_statistics_list.append({
                'date': date,
                'stats': list(stats)
            })

        context = {
            'week_dates': week_dates,
            'report_data': report_data,
            'all_classes': all_classes,
            'selected_classes': [int(c) for c in selected_classes],
            'dish_statistics': dish_statistics_list,
            'week_start': start_of_week,
            'week_end': week_dates[-1],
            'opts': self.model._meta,
            **self.admin_site.each_context(request),
        }

        return render(request, 'weekly_reports.html', context)


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

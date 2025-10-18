from django.db.models import Count
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from django.http import HttpRequest, JsonResponse
from django.shortcuts import render
from django.contrib import messages

from .models import Class, Pupil, Dish, DailyMenu, BreakfastChoice
from django.contrib.auth.decorators import login_required


def pooling(request: HttpRequest):
    if request.method == 'POST':
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            class_id = request.POST.get('class_name')

            pupil, created = Pupil.objects.get_or_create(
                first_name=first_name,
                last_name=last_name,
                class_group_id=class_id
            )

            saved_choices = 0
            for key, value in request.POST.items():
                if key.startswith('breakfast_'):
                    date_str = key.replace('breakfast_', '')
                    date = datetime.strptime(date_str, '%Y-%m-%d').date()

                    BreakfastChoice.objects.filter(
                        pupil=pupil,
                        date=date
                    ).delete()

                    if value and value != "none" and value != "":
                        BreakfastChoice.objects.create(
                            pupil=pupil,
                            date=date,
                            chosen_dish_id=value
                        )
                        saved_choices += 1

            messages.success(request, f'Сохранено {saved_choices} выборов для {first_name}!')
            return redirect('/pool/')

        except Exception as e:
            messages.error(request, f'Ошибка при сохранении: {str(e)}')
            return redirect('/pool/')

    else:
        dishes = Dish.objects.all().order_by('name')
        classes = Class.objects.all().order_by('name')

        today = datetime.now().date()
        current_weekday = today.weekday()
        if current_weekday >= 4:
            days_until_monday = (7 - current_weekday) % 7
            start_date = today + timedelta(days=days_until_monday)
            week_dates = [start_date + timedelta(days=i) for i in range(5)]
        else:
            week_dates = [today + timedelta(days=i - current_weekday) for i in range(current_weekday + 1, 5)]

        # Создаем список вместо словаря
        week_data = []
        for date in week_dates:
            try:
                menu = DailyMenu.objects.get(date=date)
                week_data.append({
                    'date': date,
                    'menu': menu,
                    'has_menu': True
                })
            except DailyMenu.DoesNotExist:
                week_data.append({
                    'date': date,
                    'menu': None,
                    'has_menu': False
                })

        context = {
            'today': today,
            'classes': classes,
            'week_data': week_data,
            'week_dates': week_dates
        }

        return render(request, 'pool.html', context)


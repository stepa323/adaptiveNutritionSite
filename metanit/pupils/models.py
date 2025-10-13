from django.db import models


class Class(models.Model):
    name = models.CharField(max_length=10, verbose_name='Название класса')

    def __str__(self):
        return self.name


class Pupil(models.Model):
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    class_group = models.ForeignKey(Class, on_delete=models.CASCADE, verbose_name='Класс')

    def __str__(self):
        return f"{self.last_name} {self.first_name}"


class Dish(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название блюда')

    def __str__(self):
        return self.name


class DailyMenu(models.Model):
    """Меню на конкретный день - ссылается на блюда"""
    date = models.DateField(verbose_name='Дата')
    option_1 = models.ForeignKey(Dish, on_delete=models.CASCADE,
                                 related_name='menu_option_1', verbose_name='Вариант завтрака 1')
    option_2 = models.ForeignKey(Dish, on_delete=models.CASCADE,
                                 related_name='menu_option_2', verbose_name='Вариант завтрака 2')

    class Meta:
        unique_together = ['date']

    def __str__(self):
        return f"Меню на {self.date}"


class BreakfastChoice(models.Model):
    """Выбор ученика на конкретный день"""
    pupil = models.ForeignKey(Pupil, on_delete=models.CASCADE, verbose_name='Ученик')
    date = models.DateField(verbose_name='Дата')
    chosen_dish = models.ForeignKey(Dish, on_delete=models.CASCADE, verbose_name='Выбранное блюдо')

    class Meta:
        unique_together = ['pupil', 'date']

    def __str__(self):
        return f"{self.pupil} - {self.date} - {self.chosen_dish}"

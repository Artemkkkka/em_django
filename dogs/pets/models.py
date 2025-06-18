"""
Модуль с моделями собак и пород для API.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from .constants import (
    MIN_RATING,
    MAX_RATING,
    MAX_COLOR,
    MAX_GENDER,
    MAX_LENGTH,
    )


class Breed(models.Model):
    """
    Модель, представляющая породу собак с различными характеристиками.

    Атрибуты:
        name (CharField): Название породы.
        size (CharField): Размеры породы, например, миниатюрная, маленькая, средняя, крупная.
        friendliness (IntegerField): Оценка дружелюбия от 1 до 5.
        trainability (IntegerField): Оценка обучаемости от 1 до 5.
        shedding_amount (IntegerField): Оценка линьки от 1 до 5.
        exercise_needs (IntegerField): Оценка кол-ва упражений от 1 до 5.
    """
    SIZE_CHOICES = [
        ('Tiny', 'Tiny'),
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    ]

    name = models.CharField(max_length=MAX_LENGTH)
    size = models.CharField(max_length=MAX_LENGTH, choices=SIZE_CHOICES)
    friendliness = models.IntegerField(
        validators=[MinValueValidator(MIN_RATING), MaxValueValidator(MAX_RATING)]
    )
    trainability = models.IntegerField(
        validators=[MinValueValidator(MIN_RATING), MaxValueValidator(MAX_RATING)]
    )
    shedding_amount = models.IntegerField(
        validators=[MinValueValidator(MIN_RATING), MaxValueValidator(MAX_RATING)]
    )
    exercise_needs = models.IntegerField(
        validators=[MinValueValidator(MIN_RATING), MaxValueValidator(MAX_RATING)]
    )

    def __str__(self):
        """
        Возвращает строковое представление породы.

        Returns:
            str: Название породы.
        """
        return self.name


class Dog(models.Model):
    """
    Модель, представляющая собаку с различными атрибутами, связанными с породой.

    Attributes:
        name (CharField): Кличка собаки.
        age (IntegerField): Возраст собаки в годах.
        breed (ForeignKey): Ссылка на модель породы.
        gender (CharField): Пол собаки.
        color (CharField): Цвет собаки.
        favorite_food (CharField): Любимая еда собаки.
        favorite_toy (CharField): Любимая игрушка собаки.
    """
    name = models.CharField(max_length=MAX_LENGTH)
    age = models.IntegerField()
    breed = models.ForeignKey(Breed, related_name='dogs', on_delete=models.CASCADE)
    gender = models.CharField(max_length=MAX_GENDER)
    color = models.CharField(max_length=MAX_COLOR)
    favorite_food = models.CharField(max_length=MAX_LENGTH)
    favorite_toy = models.CharField(max_length=MAX_LENGTH)

    def __str__(self):
        """
        Возвращает строковое представление собаки.

        Returns:
            str: Кличка собаки.
        """
        return self.name

"""
Модуль с сериализаторами для моделей собак и пород.
"""
from rest_framework import serializers
from .models import Dog, Breed


class DogListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для составления списка экземпляров собак, включая средний возраст их породы.
    """
    avg_age_of_breed = serializers.FloatField(read_only=True)

    class Meta:
        model = Dog
        fields = ['id', 'name', 'age', 'breed', 'gender', 'color', 'favorite_food', 'favorite_toy', 'avg_age_of_breed']


class DogDetailSerializer(serializers.ModelSerializer):
    """
    Сериализатор для получения подробной информации о собаках, включая количество собак одной породы.
    """
    same_breed_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Dog
        fields = ['id', 'name', 'age', 'breed', 'gender', 'color', 'favorite_food', 'favorite_toy', 'same_breed_count']


class BreedListSerializer(serializers.ModelSerializer):
    """
    Сериализатор для составления списка экземпляров пород, включая количество связанных с ними собак.
    """
    dogs_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Breed
        fields = [
            'id', 'name', 'size', 'friendliness', 'trainability', 'shedding_amount', 'exercise_needs', 'dogs_count'
        ]


class BreedSerializer(serializers.ModelSerializer):
    """
    Сериализатор для создания, извлечения, обновления и удаления операций Breed.
    """
    class Meta:
        model = Breed
        fields = ['id', 'name', 'size', 'friendliness', 'trainability', 'shedding_amount', 'exercise_needs']

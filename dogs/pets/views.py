"""
Модуль, определяющий наборы представлений для конечных точек API для собак и пород.
"""
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import OuterRef, Subquery, Avg, Count, IntegerField
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from .models import Dog, Breed
from .serializers import (
    DogListSerializer, DogDetailSerializer,
    BreedListSerializer, BreedSerializer
)


class DogViewSet(viewsets.ViewSet):
    """
    ViewSet для моделей собак.

    Методы:
        list: Обрабатывает запросы GET для получения списка всех собак со средним возрастом для каждой породы.
        create: Обрабатывает запросы POST для создания новой собаки.
        retrieve: Обрабатывает запросы GET для одной собаки, включая количество собак той же породы.
        update: Обрабатывает запросы PUT для обновления существующей собаки.
        destroy: Обрабатывает запросы DELETE для удаления собаки.
    """

    def list(self, request):
        """
        Выводит список всех экземпляров собак с указанием среднего возраста их породы.

        Args:
            request (rest_framework.request.Request): Входящий HTTP-запрос.

        Returns:
            rest_framework.response.Response: Систематизированный список собак с указанием среднего возраста.
        """
        queryset = Dog.objects.all()
        avg_subq = Dog.objects.filter(breed=OuterRef('breed')).values('breed')
        avg_subq = avg_subq.annotate(avg_age=Avg('age')).values('avg_age')
        queryset = queryset.annotate(avg_age_of_breed=Subquery(avg_subq))
        serializer = DogListSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=DogDetailSerializer,
        responses={201: DogDetailSerializer},
    )
    def create(self, request):
        """
        Создаёт запись о новой собаке.

        Args:
            request (rest_framework.request.Request): Входящий HTTP-запрос с данными о собаке.

        Returns:
            rest_framework.response.Response: Сериализованные данные о собаках и статус HTTP 201 об успешном выполнении.

        Raises:
            rest_framework.exceptions.ValidationError: Если входные данные неверны.
        """
        serializer = DogDetailSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        dog = serializer.save()
        output = DogDetailSerializer(dog)
        return Response(output.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        Возвращает запись об одной собаке.

        Args:
            request (rest_framework.request.Request): Входящий HTTP-запрос.
            pk (int): Первичный ключ для извлечения собаки.

        Returns:
            rest_framework.response.Response: Сериализованные данные о собаке.

        Raises:
            django.http.Http404: Если собак с заданным pk не существует.
        """
        count_subq = (
            Dog.objects
               .filter(breed=OuterRef('breed'))
               .values('breed')
               .annotate(cnt=Count('id'))
               .values('cnt')[:1]
        )
        dog = get_object_or_404(
            Dog.objects.annotate(
                same_breed_count=Subquery(count_subq, output_field=IntegerField())
            ),
            pk=pk
        )
        serializer = DogDetailSerializer(dog)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=DogDetailSerializer,
        responses={200: DogDetailSerializer},
    )
    def update(self, request, pk=None):
        """
        Обновляет данные о собаке.

        Args:
            request (rest_framework.request.Request): Входящий HTTP-запрос с обновленными данными.
            pk (int): Первичный ключ Dog для обновления.

        Returns:
            rest_framework.response.Response: Сериализованные обновленные данные о собаке.

        Raises:
            django.http.Http404: Если собака с заданным pk не существует.
            rest_framework.exceptions.ValidationError: Если входные данные неверны.
        """
        dog = Dog.objects.get(id=pk)
        serializer = DogDetailSerializer(dog, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Удаляет данные о собаке.

        Args:
            request (rest_framework.request.Request): Входящий HTTP-запрос.
            pk (int): Первичный ключ Dog для удаления.

        Returns:
            rest_framework.response.Response: HTTP 204 No Content on success.

        Raises:
            django.http.Http404: Если собака с заданным pk не существует.
        """
        dog = Dog.objects.get(id=pk)
        dog.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BreedViewSet(viewsets.ViewSet):
    """
    ViewSet для моделей пород.

    Методы:
        list: Обрабатывает запросы GET для составления списка всех пород с указанием количества собак.
        create: Обрабатывает запросы POST для создания новой породы.
        retrieve: Обрабатывает запросы GET для одной породы.
        update: Обрабатывает запросы PUT для обновления существующей породы.
        destroy: Обрабатывает запросы DELETE на удаление, чтобы удалить породу.
    """

    def list(self, request):
        """
        Выводит все экземпляры породы с аннотированным количеством связанных с ней собак.

        Args:
            request (rest_framework.request.Request): Входящий HTTP-запрос.

        Returns:
            rest_framework.response.Response: Сериализированный список пород с указанием количества собак.
        """
        queryset = Breed.objects.all()
        count_subq = Dog.objects.filter(breed=OuterRef('pk')).values('breed')
        count_subq = count_subq.annotate(c=Count('id')).values('c')
        queryset = queryset.annotate(dogs_count=Subquery(count_subq))
        serializer = BreedListSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=BreedSerializer,
        responses={201: BreedSerializer}
    )
    def create(self, request):
        """
        Создаёт запись о новой породе.

        Args:
            request (rest_framework.request.Request): Входящий HTTP-запрос с данными о породе.

        Returns:
            rest_framework.response.Response: Сериализованные данные о породе и статус HTTP 201 об успешном завершении.

        Raises:
            rest_framework.exceptions.ValidationError: Если входные данные неверны.
        """
        serializer = BreedSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        breed = serializer.save()
        output = BreedSerializer(breed)
        return Response(output.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        """
        Возвращает запись об одной породе.

        Args:
            request (rest_framework.request.Request): Входящий HTTP-запрос.
            pk (int): Первичный ключ для извлечения породы.

        Returns:
            rest_framework.response.Response: Сериализованные данные о породе.

        Raises:
            django.http.Http404: Если пород с заданным pk не существует.
        """
        breed = Breed.objects.get(id=pk)
        serializer = BreedSerializer(breed)
        return Response(serializer.data)

    @swagger_auto_schema(
        request_body=BreedSerializer,
        responses={200: BreedSerializer}
    )
    def update(self, request, pk=None):
        """
        ОБновляет данные о породе.

        Args:
            request (rest_framework.request.Request): Входящий HTTP-запрос с обновленными данными.
            pk (int): Первичный ключ для извлечения породы.

        Returns:
            rest_framework.response.Response: Сериализованные обновлённые данные о породе.

        Raises:
            django.http.Http404: Если пород с заданным pk не существует.
            rest_framework.exceptions.ValidationError: Если входные данные неверны.
        """
        breed = Breed.objects.get(id=pk)
        serializer = BreedSerializer(breed, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Удаляет данные о породе.

        Args:
            request (rest_framework.request.Request): Входящий HTTP-запрос.
            pk (int): Primary key of the Breed to delete.

        Returns:
            rest_framework.response.Response: HTTP 204 No Content on success.

        Raises:
            django.http.Http404: Если пород с заданным pk не существует.
        """
        breed = Breed.objects.get(id=pk)
        breed.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

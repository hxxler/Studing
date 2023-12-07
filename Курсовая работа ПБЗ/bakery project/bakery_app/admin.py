from django.contrib import admin
from .models import Клиент, Выпечка, Доставка, Пекарь, Заказ

@admin.register(Клиент)
class КлиентAdmin(admin.ModelAdmin):
    list_display = ('id', 'Имя', 'Адрес', 'Телефон')
    search_fields = ('Имя', 'Адрес', 'Телефон')
    list_editable = ('Имя', 'Адрес', 'Телефон')

@admin.register(Выпечка)
class ВыпечкаAdmin(admin.ModelAdmin):
    list_display = ('id', 'Название', 'Тип', 'Стоимость', 'Описание')
    search_fields = ('Название', 'Тип', 'Стоимость', 'Описание')
    list_editable = ('Название', 'Тип', 'Стоимость', 'Описание')

@admin.register(Доставка)
class ДоставкаAdmin(admin.ModelAdmin):
    list_display = ('id', 'Заказ_id', 'Адрес_Доставки', 'Дата_Доставки', 'Статус_Доставки')
    search_fields = ('Адрес_Доставки', 'Дата_Доставки', 'Статус_Доставки')
    list_filter = ('Статус_Доставки',)
    list_editable = ('Адрес_Доставки', 'Дата_Доставки', 'Статус_Доставки')

@admin.register(Пекарь)
class ПекарьAdmin(admin.ModelAdmin):
    list_display = ('id', 'Имя', 'Фамилия', 'Контактный_Телефон')
    search_fields = ('Имя', 'Фамилия', 'Контактный_Телефон')
    list_editable = ('Имя', 'Фамилия', 'Контактный_Телефон')

@admin.register(Заказ)
class ЗаказAdmin(admin.ModelAdmin):
    list_display = ('id', 'Клиент_id', 'Выпечка_id', 'Пекарь_id', 'Количество', 'Сумма_Заказа', 'Дата_Заказа')
    search_fields = ('Клиент_id__Имя', 'Выпечка_id__Название', 'Пекарь_id__Имя', 'Количество', 'Сумма_Заказа', 'Дата_Заказа')
    list_filter = ('Дата_Заказа',)
    list_editable = ('Клиент_id', 'Выпечка_id', 'Пекарь_id', 'Количество', 'Сумма_Заказа', 'Дата_Заказа')

# timetable/views.py

from django.shortcuts import render
from .models import Library  # Изменил импорт

def index(request):
    libraries = Library.objects.all()  # Изменил название переменной
    return render(
        request,
        'timetable/index.html',
        {'libraries': libraries}  # Изменил название переменной
    )

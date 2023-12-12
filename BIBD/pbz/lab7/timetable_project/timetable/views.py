# timetable/views.py

from django.shortcuts import render
from .models import Class, ClassSubject, Teacher

def index(request):
    classes = Class.objects.all()
    class_subjects = ClassSubject.objects.all()
    teachers = Teacher.objects.all()

    return render(
        request,
        'timetable/index.html',
        {'classes': classes, 'class_subjects': class_subjects, 'teachers': teachers}
    )

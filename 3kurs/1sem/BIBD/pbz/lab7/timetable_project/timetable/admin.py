# timetable/admin.py

from django.contrib import admin
from .models import Class, ClassSubject, Teacher

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('ClassID', 'Subject', 'HoursPerWeek')
    search_fields = ('Subject',)
    list_filter = ('Subject', 'HoursPerWeek')

@admin.register(ClassSubject)
class ClassSubjectAdmin(admin.ModelAdmin):
    list_display = ('ClassID', 'ClassLetter', 'Subject', 'TeacherID')
    search_fields = ('Subject',)
    list_filter = ('ClassID', 'ClassLetter', 'Subject', 'TeacherID')

@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('TeacherID', 'TeacherName', 'Specialization', 'Experience')
    search_fields = ('TeacherName',)
    list_filter = ('Specialization', 'Experience')

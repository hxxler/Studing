# timetable/models.py

from django.db import models

class Class(models.Model):
    ClassID = models.AutoField(primary_key=True)
    Subject = models.CharField(max_length=255)
    HoursPerWeek = models.IntegerField()

class ClassSubject(models.Model):
    ClassID = models.IntegerField()
    ClassLetter = models.CharField(max_length=1)
    Subject = models.CharField(max_length=255)
    TeacherID = models.IntegerField()

class Teacher(models.Model):
    TeacherID = models.AutoField(primary_key=True)
    TeacherName = models.CharField(max_length=255)
    Specialization = models.CharField(max_length=255)
    Experience = models.IntegerField()

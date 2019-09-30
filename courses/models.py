from django.db import models
from django.contrib.auth.models import User


class Course(models.Model):
    title = models.CharField(max_length=256, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.PositiveIntegerField()
    date_start = models.DateTimeField()
    duration = models.PositiveIntegerField()
    teachers = models.ManyToManyField('Teacher', related_name='courses', blank=True)
    students = models.ManyToManyField(User, related_name='courses', blank=True)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=256)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    homework = models.TextField(null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.date.strftime("%d-%m-%Y %H:%M") + " " + self.title


class Teacher(models.Model):
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

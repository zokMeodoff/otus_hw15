'''from django.db import models
from django.contrib.auth.models import User
from courses.models import Lesson


class UserProfile(models.Model):
   user = models.OneToOneField(User)
   is_superuser = models.BooleanField()
   lessons = models.ManyToManyField('Lesson', related_name='user_profile')

   def __str__(self):
       return self.user.username'''


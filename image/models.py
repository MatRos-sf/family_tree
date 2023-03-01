from django.db import models

class ProfileImage(models.Model):

    image = models.ImageField(default='media/default.png')
    created = models.DateTimeField(auto_now_add=True)
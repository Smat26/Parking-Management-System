from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Camera(models.Model):
    name = models.CharField(max_length=30)
    url = models.CharField(max_length=200)
    fps = models.IntegerField()
    height = models.IntegerField()
    width = models.IntegerField()

    def __str__(self):
        return self.name


class Roi(models.Model):
    name = models.CharField(max_length=30)
    min_x = models.IntegerField()
    min_y = models.IntegerField()
    max_x = models.IntegerField()
    max_y = models.IntegerField()
    camera = models.ForeignKey(Camera, on_delete=models.CASCADE)
    occupied = models.BooleanField()

    class Meta:
        verbose_name = 'Parking Slot' 
        verbose_name_plural = 'Parking Slots'

    def __str__(self):
        return self.name

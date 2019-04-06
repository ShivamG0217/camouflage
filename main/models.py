from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver

# Create your models here.
class Images(models.Model):
    message = models.CharField(max_length=255)
    key = models.CharField(max_length=255)
    img = models.ImageField(upload_to='')

    def __str__(self):
        return self.key

    def delete(self, *args, **kwargs):
        self.img.delete()
        super().delete(*args, **kwargs)

class ImageDecrypt(models.Model):
    EncImage = models.ImageField(upload_to="encrypted_img/")
    key = models.CharField(max_length=255)
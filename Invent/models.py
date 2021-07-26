from typing import AbstractSet
from django.db import models
from django.db.models.aggregates import Max
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw


class User(AbstractUser):
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


class Items(models.Model):
    itemName = models.CharField(max_length=50, unique=True)
    Price = models.FloatField()
    quantity = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    file = models.FileField(upload_to='static/uploads', null=True, blank=True)

    def __str__(self):
        return str(self.itemName)


class QR(models.Model):
    qr_code = models.ImageField(upload_to='static/uploads', blank=True)
    item = models.OneToOneField(Items, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.item)

    def save(self, *args, **kwargs):
        qrcode_img = qrcode.make(self.item)
        canvas = Image.new('RGB', (290,290), 'white')
        draw = ImageDraw.Draw(canvas)
        canvas.paste(qrcode_img)
        fname = f'qr_code-{self.item}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()
        super().save(*args, **kwargs)

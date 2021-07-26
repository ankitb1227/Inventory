from django.contrib import admin
from .models import User, Items, QR
# Register your models here.

admin.site.register(User)
admin.site.register(Items)
admin.site.register(QR)

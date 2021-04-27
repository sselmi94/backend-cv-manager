from django.contrib import admin
from .models import Songs
from .models import MyFile

# Register your models here.
admin.site.register(Songs)
admin.site.register(MyFile)
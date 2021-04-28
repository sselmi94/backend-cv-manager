from django.contrib import admin
from .models import Songs
from .models import MyFile
from .models import Category
from .models import Terme
from .models import Profil
from .models import ProfilCategoryScore

# Register your models here.
admin.site.register(Songs)
admin.site.register(MyFile)
admin.site.register(Category)
admin.site.register(Terme)
admin.site.register(Profil)
admin.site.register(ProfilCategoryScore)
from django.db import models

# Create your models here.
class Songs(models.Model):
    # song title
    title = models.CharField(max_length=255, null=False)
    # name of artist or group/band
    artist = models.CharField(max_length=255, null=False)

    def __str__(self):
        return "{} - {}".format(self.title, self.artist)

class MyFile(models.Model):

    resume = models.FileField(blank=False, null=False)

    uploaded_at = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name =  models.CharField(max_length=255,null=False)

class Terme(models.Model):
    title =  models.CharField(max_length=255,null=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    def as_dict(self):
        return {
            #"id": self.id,
            "title": self.title,
            "category": self.category.name
            # other stuff
        }

class Profil(models.Model):
    firstname = models.CharField(max_length=255, null=False)
    lastname = models.CharField(max_length=255)
    dateOfBirth = models.DateField
    yearsOfExperience = models.DecimalField(blank=True, null=True, max_digits=2,  decimal_places=1,default=1.0)
    profilLabel = models.CharField(max_length=255)
    attachment = models.ForeignKey(MyFile,on_delete=models.CASCADE)


class ProfilCategoryScore(models.Model):
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    profil = models.ForeignKey(Profil,on_delete=models.CASCADE)
    score = models.DecimalField(blank=True, null=True, max_digits=4,  decimal_places=2,default=1.0)









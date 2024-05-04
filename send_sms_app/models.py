from django.db import models

class Mutualist(models.Model):

    full_name = models.CharField("Nom et Prénom", max_length=100)
    phone = models.CharField("Numéro de téléĥone", max_length=10)

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Mutualiste"
        verbose_name_plural = "Mutualistes"



class Sms(models.Model):

    content = models.TextField("contenu")
    

    def __str__(self):
        return f"{self.id}"
    
    class Meta:
        verbose_name = "Sms"
        verbose_name_plural = "Sms"
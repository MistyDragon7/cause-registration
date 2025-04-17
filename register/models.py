from django.db import models

class Supporter(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    phno = models.CharField(max_length=15)
    email = models.EmailField()
    support = models.BooleanField()

    def __str__(self):
        return f"{self.name} ({self.phno})"

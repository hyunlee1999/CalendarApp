from django.db import models

class DummyModel(models.Model):
    dummyText = models.CharField(max_length=200)

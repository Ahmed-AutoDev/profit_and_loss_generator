from django.db import models

# Create your models here.

class TrialBalance(models.Model):
    file = models.FileField(upload_to='upload/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


from django.db import models
from users.models import CustomUser

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date_sent = models.DateTimeField(auto_now_add=True)
    text = models.TextField()
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)

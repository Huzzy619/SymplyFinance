from django.db import models
from uuid import uuid4

models.AutoField
class Blacklist (models.Model):
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)
    trials = models.PositiveSmallIntegerField(default=0)
    ip_address = models.GenericIPAddressField()
    created_on = models.DateTimeField(auto_now_add=True)

    

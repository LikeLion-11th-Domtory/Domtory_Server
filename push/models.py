from django.db import models

class Token(models.Model):
    push_token = models.CharField(max_length=255)
    is_valid = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'tokens'
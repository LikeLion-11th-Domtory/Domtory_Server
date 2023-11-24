from django.db import models


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    date_code = models.CharField(max_length=6)  # yymmdd: 231125
    date_detail = models.CharField(max_length=15)  # 23.11.19 (일)
    breakfast = models.CharField(max_length=1000)
    lunch = models.CharField(max_length=1000)
    dinner = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.date
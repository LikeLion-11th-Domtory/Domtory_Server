from django.db import models


class Menu(models.Model):
    date_code = models.CharField(primary_key=True, max_length=6)  # yymmdd: 231125
    date_detail = models.CharField(max_length=15)  # 23.11.19 (일)
    breakfast = models.CharField(max_length=1000)
    lunch = models.CharField(max_length=1000)
    dinner = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.date

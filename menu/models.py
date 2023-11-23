from django.db import models


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    date_code = models.CharField()  # yymmdd: 231125
    date_detail = models.CharField()  # 23.11.19 (일)
    breakfast = models.CharField()
    lunch = models.CharField()
    dinner = models.CharField()
    
    def __str__(self):
        return self.date
from django.db import models


class Menu(models.Model):
    date_code = models.CharField(primary_key=True, max_length=6)  # yymmdd: 231125
    date_detail = models.CharField(max_length=15)  # 23.11.19 (일)

    def __str__(self):
        return self.date_code


class Breakfast(models.Model):
    id = models.AutoField(primary_key=True)
    date_code = models.ForeignKey(Menu, on_delete=models.CASCADE)
    menu = models.CharField(max_length=512)
    
    def __str__(self):
        return self.menu


class Lunch(models.Model):
    id = models.AutoField(primary_key=True)
    date_code = models.ForeignKey(Menu, on_delete=models.CASCADE)
    menu = models.CharField(max_length=512)
    
    def __str__(self):
        return self.menu


class Dinner(models.Model):
    id = models.AutoField(primary_key=True)
    date_code = models.ForeignKey(Menu, on_delete=models.CASCADE)
    menu = models.CharField(max_length=512)
    
    def __str__(self):
        return self.menu

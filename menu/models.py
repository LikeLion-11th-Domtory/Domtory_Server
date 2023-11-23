from django.db import models


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.CharField()

    def __str__(self):
        return self.date


class Breakfast(models.Model):
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    menu = models.CharField(max_length=100)
    
    def __str__(self):
        return self.menu


class Lunch(models.Model):
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    menu = models.CharField(max_length=100)
    
    def __str__(self):
        return self.menu


class Dinner(models.Model):
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE)
    menu = models.CharField(max_length=100)
    
    def __str__(self):
        return self.menu

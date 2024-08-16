from django.db import models
from .dorm_list import DormList

class Dorm(models.Model):
    """
    기숙사 모델
    """
    DORM_LIST = DormList.get_choices()

    dorm_name = models.CharField(max_length = 255, choices = DORM_LIST, verbose_name = "기숙사 이름", unique = True, null = False)
    descriptions = models.CharField(max_length= 3*300, default = "", verbose_name = "비고") # 한글 300자
    
    def __str__(self):
        return self.dorm_name
    
    class Meta:
        db_table = 'dorm'
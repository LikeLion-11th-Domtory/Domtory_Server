from django.db import models

class Board(models.Model):
    """
    게시판 모델
    """
    name = models.CharField(max_length = 60, null = False, unique = True, verbose_name = '게시판 이름') # 한글 20글자
    description = models.TextField(null = True, blank = True, verbose_name = '설명')

    def save(self, *args, **kwargs):
        if self.description == None or self.description == "":
            self.description = f"{self.name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'board'
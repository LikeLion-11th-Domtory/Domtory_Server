from django.db import models
from datetime import datetime
from uuid import uuid4
import os
from dorm.domains import Dorm
from django.core.exceptions import ValidationError

def path_and_rename(instance, filename):
    upload_to = 'personal_info_excel'
    formatted_date = datetime.now().strftime('%y%m%d')
    uuid = uuid4().hex
    ext = filename.split('.')[-1]
    if instance.dorm:
        dorm_name = instance.dorm.dorm_name
    else:
        dorm_name = 'unknown_dorm'
            
    filename = '{}-{}-{}.{}'.format(dorm_name, formatted_date, uuid, ext)
    return os.path.join(upload_to, filename)

class PersonalInfoExcelFile(models.Model):
    excel_file = models.FileField(upload_to=path_and_rename)
    created_at = models.DateTimeField(auto_now_add = True)
    dorm = models.ForeignKey(Dorm, null=True, on_delete=models.SET_NULL)
    
    class Meta:
        db_table = 'personal_info_excel_file'
    
    def clean(self):
        if self.dorm and self.dorm.pk == 1:
            raise ValidationError("엑셀 파일 이름은 전체 기숙사가 될 수 없습니다.")
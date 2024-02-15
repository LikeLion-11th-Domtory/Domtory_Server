from django.db import models
from datetime import datetime
from uuid import uuid4
import os

def path_and_rename(instance, filename):
    upload_to = 'personal_info_excel'
    formatted_date = datetime.now().strftime('%y%m%d')
    uuid = uuid4().hex
    ext = filename.split('.')[-1]
    filename = '{}-{}.{}'.format(formatted_date, uuid, ext)
    return os.path.join(upload_to, filename)

class PersonalInfoExcelFile(models.Model):
    excel_file = models.FileField(upload_to=path_and_rename)
    created_at = models.DateTimeField(auto_now_add = True)
    
    class Meta:
        db_table = 'personal_info_excel_file'
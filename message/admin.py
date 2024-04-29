from django.contrib import admin

from message.domains.message_block_models import MessageBlock
from message.domains.message_models import Message

# Register your models here.
admin.site.register(Message)
admin.site.register(MessageBlock)

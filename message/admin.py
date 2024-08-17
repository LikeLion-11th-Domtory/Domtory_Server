from django.contrib import admin
from django.utils import timezone
from message.domains.message_block_models import MessageBlock
from message.domains.message_models import Message, MessageRoom


class MessageAdmin(admin.ModelAdmin):
    list_display = ('body', 'get_post_title', 'get_sender_name', 'get_receiver_name', 'get_created_at')
    search_fields = ['body', 'sender__name', 'receiver__name']

    def get_model_perms(self, request):
        if request.user.is_superuser:
            return super().get_model_perms(request)
        return {}

    def get_post_title(self, obj):
        return obj.message_room.post.title
    get_post_title.short_description = '시작 게시글 제목'

    def get_sender_name(self, obj):
        return obj.sender.name
    get_sender_name.short_description = '발신자'

    def get_receiver_name(self, obj):
        return obj.receiver.name
    get_receiver_name.short_description = '수신자'

    def get_created_at(self, obj):
        return timezone.localtime(obj.created_at)
    get_created_at.short_description = '작성 시각'


class MessageRoomAdmin(admin.ModelAdmin):
    list_display = ('get_first_sender_name', 'get_first_receiver_name')
    search_fields = ['post_title', 'first_sender__name', 'first_receiver__name']

    def get_model_perms(self, request):
        if request.user.is_superuser:
            return super().get_model_perms(request)
        return {}

    def get_first_sender_name(self, obj):
        return obj.first_sender.name
    get_first_sender_name.short_description = '최초 발신자'

    def get_first_receiver_name(self, obj):
        return obj.first_receiver.name
    get_first_receiver_name.short_description = '최초 수신자'


class MessageBlockAdmin(admin.ModelAdmin):
    list_display = ('get_requester_name', 'get_target_name')
    search_fields = ['requester__name', 'target__name']

    def get_model_perms(self, request):
        if request.user.is_superuser:
            return super().get_model_perms(request)
        return {}

    def get_requester_name(self, obj):
        return obj.requester.name
    get_requester_name.short_description = '차단한 사람'

    def get_target_name(self, obj):
        return obj.target.name
    get_target_name.short_description = '차단당한 사람'


admin.site.register(Message, MessageAdmin)
admin.site.register(MessageRoom, MessageRoomAdmin)
admin.site.register(MessageBlock, MessageBlockAdmin)
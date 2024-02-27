from django.contrib import admin
from .models import *
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Register your models here.

class BoardFilter(admin.SimpleListFilter):
    # 필터의 타이틀과 파라미터 이름 설정
    title = _('board')
    parameter_name = 'board'

    def lookups(self, request, model_admin):
        return Board.objects.all().values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(board_id=self.value())
        return queryset
    

class BoardAdmin(admin.ModelAdmin):
    list_display = ('name',)
    

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_member_name', 'board', 'get_created_at')
    list_filter = (BoardFilter,)
    search_fields = ['title', 'member__name']

    def get_member_name(self, obj):
        return obj.member.name
    get_member_name.short_description = '작성자'

    def get_created_at(self, obj):
        return timezone.localtime(obj.created_at)
    get_created_at.short_description = '작성 시각'


class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'get_member_name')
    search_fields = ['post__title']

    def get_member_name(self, obj):
        return obj.post.member.name
    get_member_name.short_description = '작성자'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'get_member_name', 'post', 'get_created_at')
    list_display_links = ('body', 'post', 'get_member_name')
    search_fields = ['post__title', 'member__name']
    
    def get_member_name(self, obj):
        return obj.member.name
    get_member_name.short_description = '작성자'

    def get_created_at(self, obj):
        return timezone.localtime(obj.created_at)
    get_created_at.short_description = '작성 시각'


admin.site.register(Board, BoardAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(Comment, CommentAdmin)

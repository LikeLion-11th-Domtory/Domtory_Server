from django.contrib import admin, messages
from django.db.models import Q

from dorm.domains import Dorm
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

    def get_queryset(self, request):
        if request.user.is_superuser or request.user.dorm_id == Dorm.DORM_LIST[0][1]:
            return super().get_queryset(request)
        queryset = super().get_queryset(request)
        return queryset.filter(Q(dorm_id = request.user.dorm.id)|Q(board_id = 7))

    def get_member_name(self, obj):
        return obj.member.name
    get_member_name.short_description = '작성자'

    def get_created_at(self, obj):
        return timezone.localtime(obj.created_at)
    get_created_at.short_description = '작성 시각'


class PostImageAdmin(admin.ModelAdmin):
    list_display = ('post', 'get_member_name')
    search_fields = ['post__title']

    def get_queryset(self, request):
        if request.user.is_superuser or request.user.dorm_id == Dorm.DORM_LIST[0][1]:
            return super().get_queryset(request)
        queryset = PostImage.objects.select_related('post').filter(Q(dorm_id = request.user.dorm.id)|Q(post__board_id = 7))
        return queryset

    def get_member_name(self, obj):
        return obj.post.member.name
    get_member_name.short_description = '작성자'


class CommentAdmin(admin.ModelAdmin):
    list_display = ('body', 'get_member_name', 'post', 'get_created_at')
    list_display_links = ('body', 'post', 'get_member_name')
    search_fields = ['post__title', 'member__name']
    fields = ('post', 'parent', 'body')

    def get_queryset(self, request):
        if request.user.is_superuseror or request.user.dorm_id == Dorm.DORM_LIST[0][1]:
            return super().get_queryset(request)
        queryset = Comment.objects.select_related('post').filter(Q(dorm_id = request.user.dorm.id)|Q(post__board_id = 7))
        return queryset
    
    def get_member_name(self, obj):
        return obj.member.name
    get_member_name.short_description = '작성자'

    def get_created_at(self, obj):
        return timezone.localtime(obj.created_at)
    get_created_at.short_description = '작성 시각'

    def save_model(self, request, obj, form, change):
        if obj.parent:
            post = obj.post
            if obj.parent.post != obj.post:
                self.message_user(request, "선택한 게시글에 작성된 댓글을 선택해주세요.", level=messages.ERROR)
                return
        if change and 'is_deleted' in form.changed_data:
            if obj.is_deleted == True and post.comment_cnt > 0:
                post.comment_cnt -= 1
            else:
                post.comment_cnt += 1
            post.save()
        if not change:
            post.comment_cnt += 1
            post.save()

            comments = post.comment.all()
            anonymous_number = 0

            if request.user != post.member:
                flag = False

                for comment in comments:
                    if comment.member == request.user:
                        anonymous_number = comment.anonymous_number
                        flag = True
                        break
                    if anonymous_number < comment.anonymous_number:
                        anonymous_number = comment.anonymous_number

                if flag == False:
                    anonymous_number += 1
            obj.member = request.user
            obj.anonymous_number = anonymous_number

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        post = obj.post
        if post.comment_cnt > 0:
            post.comment_cnt -= 1
            post.save()
        super().delete_model(request, obj)

    def delete_queryset(self, request, queryset):
        for obj in queryset:
            post = obj.post
            if post.comment_cnt > 0:
                post.comment_cnt -= 1
                post.save()
            obj.delete()
        

admin.site.register(Board, BoardAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(PostImage, PostImageAdmin)
admin.site.register(Comment, CommentAdmin)

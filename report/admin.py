from django.contrib import admin
from report.models.report_models import Report
from member.domains.member import Member
from board.models.post_models import Post
from board.models.comment_models import Comment

from django.urls import reverse
from django.utils.html import format_html

# Register your models here.

# class PostInline(admin.TabularInline):
#     model = Post
#     fields = ('status',)

# class CommentInline(admin.TabularInline):
#     model = Comment
#     fields = ('status',)


class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'reported_at', 'target', 'user_status',]
    list_display_links = ['status', 'target', 'user_status',]
    list_filter = ['status']

    # actions = ["action_change_valid", "action_change_invalid", "action_change_banned"]

    fields = ('status', 'reported_at', 'target_body',)
    readonly_fields = ('reported_at', 'target_body',)

    # inlines = [PostInline, CommentInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # 필요한 경우 추가적인 데이터 처리
        return queryset.select_related('parent')  

    # 가져올 쿼리셋 정의
    def get_form_queryset(self, obj):
        return self.model.objects.filter(email=obj.email)
	
    # Inline에서 정의한 모델이 저장되는 경우에 동작
    def save_new_instance(self, parent, instance):
        instance.email = parent.email


    ## 신고 detail
    def status_user(self, obj):
        if obj.post:
            member = Member.objects.get(pk=obj.post.member.id)
            return member.status #쿼리가..
        elif obj.comment:
            member = Member.objects.get(pk=obj.comment.member.id)
            return member.status
    status_user.short_description = '유저 정지'

    def target_body(self, obj):
        if obj.post:
            return obj.post.body
        elif obj.comment:
            return obj.comment.body
    target_body.short_description = '신고 내용'

    


    ## 신고 목록 필드
    def target(self, obj):
        if obj.post:
            link = reverse('admin:board_post_change', args=[obj.post.id])
            return format_html('<a href="{}">{}</a>', link, f"게시글 신고 : {obj.post.body}")
        elif obj.comment:
            link = reverse('admin:board_comment_change', args=[obj.comment.id])
            return format_html('<a href="{}">{}</a>', link, f"댓글 신고 : {obj.comment.body}")
        
    target.short_description = '신고글'

    def user_status(self, obj):
        if obj.post:
            link = reverse('admin:member_member_change', args=[obj.post.id])
            return format_html('<a href="{}">{}</a>', link, f"유저")
        elif obj.comment:
            link = reverse('admin:member_member_change', args=[obj.comment.id])
            return format_html('<a href="{}">{}</a>', link, f"유저")
    
    

    ### Report의 상태를 바꿈 
    def action_change_valid(self, request, queryset):
        for report in queryset:
            report.status=Report.ReportType.VALID
            self.save_model(request, report, None, True)

    action_change_valid.short_description = "선택한 신고의 상태를 유효한 신고로 바꿉니다."
    
    def action_change_invalid(self, request, queryset):
        queryset.update(status=Report.ReportType.INVALID)
    
    action_change_invalid.short_description = "선택한 신고의 상태를 유효하지 않은 신고로 바꿉니다."


    ### 유저 밴
    # def action_change_banned(self, request, queryset):
    #     for report in queryset:
    #         if report.post:
    #             report.post.member.status = Member.MEMBER_STATUS_CHOICES['BANNED']
    #         elif report.comment:
    #             report.comment.member.status = Member.MEMBER_STATUS_CHOICES['BANNED']
    #         self.save_model(request, report, None, True)

    # action_change_valid.short_description = "선택한 유저를 차단합니다."
    
    # def action_change_active(self, request, queryset):
    #     queryset.update(status_user=Member.MEMBER_STATUS_CHOICES['BANNED'])
    
    # action_change_invalid.short_description = "선택한 유저의 차단을 해제합니다."




    def save_model(self, request, obj, form, change):
        if change:
            if obj.post:
                if obj.status == Report.ReportType.VALID:
                    obj.post.is_blocked = True
                obj.post.save()
            if obj.comment:
                if obj.status == Report.ReportType.VALID:
                    obj.comment.is_blocked = True
                obj.comment.save()

        super().save_model(request, obj, form, change)


admin.site.register(Report, ReportAdmin)
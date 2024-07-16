from django.contrib import admin
from report.models.report_models import Report
from member.domains.member import Member
from board.models.post_models import Post
from board.models.comment_models import Comment

from django.urls import reverse
from django.utils.html import format_html

# Register your models here.


class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'reported_at', 'target',]
    list_display_links = ['status', 'target',]
    list_filter = ['status']

    actions = ["action_change_valid", "action_change_invalid", ##Report.status의 상태변화
               "action_change_banned", "action_change_active"] ##Report.ismemberblocked의 상태변화 

    fields = ('status', 'reported_at', 'target_body', 'member_status',)
    readonly_fields = ('reported_at', 'target_body',)

    # inlines = [PostInline, CommentInline]


    ## 신고 detail
    # def status_member(self, obj):
    #     if obj.post:
    #         member = Member.objects.get(pk=obj.post.member.id)
    #         return member.status #쿼리가..
    #     elif obj.comment:
    #         member = Member.objects.get(pk=obj.comment.member.id)
    #         return member.status
    # status_user.short_description = '유저 정지'

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

    # def user_status(self, obj):
    #     if obj.post:
    #         link = reverse('admin:member_member_change', args=[obj.post.id])
    #         return format_html('<a href="{}">{}</a>', link, f"유저")
    #     elif obj.comment:
    #         link = reverse('admin:member_member_change', args=[obj.comment.id])
    #         return format_html('<a href="{}">{}</a>', link, f"유저")
    
    

    ### Report의 상태를 바꿈 
    def action_change_valid(self, request, queryset):
        for report in queryset:
            report.status=Report.ReportType.VALID
            self.save_model(request, report, None, True)

    action_change_valid.short_description = "선택한 신고의 상태를 유효한 신고로 바꿉니다."
    
    # def action_change_invalid(self, request, queryset):
    #     queryset.update(status=Report.ReportType.INVALID)
    
    # action_change_invalid.short_description = "선택한 신고의 상태를 유효하지 않은 신고로 바꿉니다."


    ### 유저 밴
    def action_change_banned(self, request, queryset):
        for report in queryset:
            if report.post:
                report.member_status = Report.MemberType.BANNED
            elif report.comment:
                report.member_status = Report.MemberType.BANNED
            self.save_model(request, report, None, True)

    action_change_banned.short_description = "작성자 유저를 차단합니다."
    
    # def action_change_active(self, request, queryset):
    #     for report in queryset:
    #         if report.post:
    #             report.is_member_blocked = False
    #             report.post.member.status = Member.MEMBER_STATUS_CHOICES['ACTIVE']
    #         elif report.comment:
    #             report.is_member_blocked = False
    #             report.comment.member.status = Member.MEMBER_STATUS_CHOICES['ACTIVE']
    #         self.save_model(request, report, None, True)
    
    # action_change_active.short_description = "작성자 유저의 차단을 해제합니다."


    def save_model(self, request, obj, form, change):
        if change:
            if obj.post:
                if obj.status == Report.ReportType.VALID: # 유효한 신고일 때 - 신고글 정지
                    obj.post.is_blocked = True

                if obj.member_status == Report.MemberType.BANNED: # 유저 정지 했을때 - 유저, 신고글 함께 정지
                    obj.post.member.status = Member.MEMBER_STATUS_CHOICES[1]
                    obj.status = Report.ReportType.VALID
                    obj.post.is_blocked = True
                
                obj.post.save()
                obj.post.member.save()
            
            if obj.comment:
                if obj.status == Report.ReportType.VALID: # 유효한 신고일 때 - 신고글 정지
                    obj.comment.is_blocked = True

                if obj.member_status == Report.MemberType.BANNED: # 유저 정지 했을때 - 유저, 신고글 함께 정지
                    obj.comment.member.status = Member.MEMBER_STATUS_CHOICES[1]
                    obj.status = Report.ReportType.VALID
                    obj.comment.is_blocked = True
                obj.comment.save()
                obj.comment.member.save()

        super().save_model(request, obj, form, change)

    """"
    MEMBER_STATUS_CHOICES = (
        ('ACTIVE','활동'),
        ('BANNED', '정지'),
        ('WITHDRAWAL', '탈퇴')
    )
    """


admin.site.register(Report, ReportAdmin)
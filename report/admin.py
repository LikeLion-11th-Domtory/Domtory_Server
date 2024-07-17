from django.contrib import admin, messages
from report.models.report_models import Report
from member.domains.member import Member
from board.models.post_models import Post
from board.models.comment_models import Comment

from report.services.unban_member_status import unban_member_status

from django.urls import reverse
from django.utils.html import format_html

# Register your models here.


class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'reported_at', 'target',]
    list_display_links = ['status', 'target',]
    list_filter = ['status']

    actions = ["action_change_report_status", ##Report.status의 상태변화
               "action_change_member_status"] ##Report.member_status의 상태변화 

    fields = ('status', 'reported_at', 'target_body', 'member_status')
    readonly_fields = ('reported_at', 'target_body')


    # 신고 객체에서 신고 내용 확인
    def target_body(self, obj):
        if obj.post:
            return obj.post.body
        elif obj.comment:
            return obj.comment.body
    target_body.short_description = '신고 내용'



    ## 신고 목록 필드 중 신고당한 글 객체 필드
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
    
    
    """
    admin에서 관리자가 설정하는 값을 객체에 넣음
    """
    ### 차단 / 차단 해제
    def action_change_report_status(self, request, queryset):
        for report in queryset:
            report_status = request.POST.get('status') ## VALID, INVALID
            report.status = report_status
            self.save_model(request, report, None, True)
            self.message_user(request, f"신고글 상태가 {report_status}로 업데이트 되었습니다.", messages.SUCCESS)

    action_change_report_status.short_description = "선택한 신고의 밴 여부를 결정합니다."
    

    ### 유저 밴 설정
    def action_change_member_status(self, request, queryset):
        for report in queryset:
            member_status = request.POST.get('member_status')
            report.member_status = member_status
            self.save_model(request, report, None, True)
            self.message_user(request, f"신고글 작성자 상태가 {member_status}로 업데이트 되었습니다.", messages.SUCCESS)

    action_change_member_status.short_description = "작성자 유저 밴 여부 및 기간을 설정합니다."


    """
    신고 객체 DB 저장
    """
    def save_model(self, request, obj, form, change):
        if change:
            if obj.post:
                if obj.status == Report.REPORT_TYPE_CHOICES[2][0]: # 유효한 신고일 때 - 신고글 정지
                    obj.post.is_blocked = True

                    obj.post.save()

                if obj.member_status != Report.MEMBER_BLOCK_CHOICES[0][0]: # 유저 정지 했을때 - 유저, 신고글 함께 정지
                    obj.post.member.status = Member.MEMBER_STATUS_CHOICES[1][0]
                    obj.status = Report.REPORT_TYPE_CHOICES[2][0]
                    obj.post.is_blocked = True

                    obj.post.save()
                    obj.post.member.save()

                    #n일 후에 차단 해제되는 로직 실행
                    unban_member_status(obj.post.member.id, int(obj.member_status))

                    
            
            if obj.comment:
                if obj.status == Report.REPORT_TYPE_CHOICES[2][0]: # 유효한 신고일 때 - 신고글 정지
                    obj.comment.is_blocked = True

                    obj.comment.save()

                if obj.member_status != Report.MEMBER_BLOCK_CHOICES[0][0]: # 유저 정지 했을때 - 유저, 신고글 함께 정지
                    obj.comment.member.status = Member.MEMBER_STATUS_CHOICES[1][0]
                    obj.status = Report.REPORT_TYPE_CHOICES[2][0]
                    obj.comment.is_blocked = True

                    obj.comment.save()
                    obj.comment.member.save()

                    #n일 후에 차단 해제되는 로직 실행
                    unban_member_status(obj.post.member.id, int(obj.member_status))

        super().save_model(request, obj, form, change)

    """"
    MEMBER_STATUS_CHOICES = (
        ('ACTIVE','활동'),
        ('BANNED', '정지'),
        ('WITHDRAWAL', '탈퇴')
    )
    """


admin.site.register(Report, ReportAdmin)
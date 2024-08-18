from django.contrib import admin, messages
from report.models.report_models import Report
from member.domains.member import Member
from board.models.post_models import Post
from board.models.comment_models import Comment

from report.services.unban_member_status import async_unban_member_status

from django.urls import reverse
from django.utils.html import format_html

# Register your models here.


class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'reported_at', 'target', 'member_name', 'member_status']
    list_display_links = ['status', 'target',]
    list_filter = ['status', 'member_status']

    actions = ["action_change_report_status", ##Report.status의 상태변화
               "action_change_member_status"] ##Report.member_status의 상태변화 

    fields = ('status', 'reported_at', 'target_body', 'member_name', 'member_status')
    readonly_fields = ('reported_at', 'target_body', 'member_name')


    # 신고 객체에서 신고 내용 확인
    def target_body(self, obj):
        if obj.post:
            return obj.post.body
        elif obj.comment:
            return obj.comment.body
        elif obj.message:
            return obj.message.body
    target_body.short_description = '신고 내용'

    ## 신고 목록 필드 중 신고당한 글 객체 필드
    def target(self, obj):
        if obj.post:
            link = reverse('admin:board_post_change', args=[obj.post.id])
            return format_html('<a href="{}">{}</a>', link, f"게시글 신고 : {obj.post.body}")
        elif obj.comment:
            link = reverse('admin:board_comment_change', args=[obj.comment.id])
            return format_html('<a href="{}">{}</a>', link, f"댓글 신고 : {obj.comment.body}")
        elif obj.message:
            link = reverse('admin:message_message_change', args=[obj.message.id])
            return format_html('<a href="{}">{}</a>', link, f"쪽지 신고 : {obj.message.body}")

    target.short_description = '신고글'

    def member_name(self, obj):
        if obj.post:
            return obj.post.member.name
        elif obj.comment:
            return obj.comment.member.name
        elif obj.message:
            return obj.message.sender.name
    member_name.short_description = '신고 대상'


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
                elif obj.status == Report.REPORT_TYPE_CHOICES[3][0]: # 유효한 신고 취소
                    obj.post.is_blocked = False

                if obj.member_status != Report.MEMBER_BLOCK_CHOICES[0][0]: # 유저 정지 했을때 - 유저, 신고글 함께 정지
                    obj.post.member.status = Member.MEMBER_STATUS_CHOICES[1][0]
                    obj.status = Report.REPORT_TYPE_CHOICES[2][0]
                    obj.post.is_blocked = True

                    #n일 후에 차단 해제되는 로직 실행
                    async_unban_member_status(obj.id, obj.member_status)
                else: # 유저 정지 취소
                    obj.post.member.status = Member.MEMBER_STATUS_CHOICES[0][0]
                
                obj.post.save()
                obj.post.member.save()
                    
            
            if obj.comment:
                if obj.status == Report.REPORT_TYPE_CHOICES[2][0]: # 유효한 신고일 때 - 신고글 정지
                    obj.comment.is_blocked = True
                elif obj.status == Report.REPORT_TYPE_CHOICES[3][0]: # 유효한 신고 취소
                    obj.comment.is_blocked = False

                if obj.member_status != Report.MEMBER_BLOCK_CHOICES[0][0]: # 유저 정지 했을때 - 유저, 신고글 함께 정지
                    obj.comment.member.status = Member.MEMBER_STATUS_CHOICES[1][0]
                    obj.status = Report.REPORT_TYPE_CHOICES[2][0]
                    obj.comment.is_blocked = True

                    #n일 후에 차단 해제되는 로직 실행
                    async_unban_member_status(obj.id, obj.member_status)
                else: # 유저 정지 취소
                    obj.comment.member.status = Member.MEMBER_STATUS_CHOICES[0][0]
                
                obj.comment.save()
                obj.comment.member.save()

            if obj.message:
                if obj.member_status != Report.MEMBER_BLOCK_CHOICES[0][0]: # 유저 정지 했을때 - 유저 정지
                    obj.message.sender.status = Member.MEMBER_STATUS_CHOICES[1][0]

        super().save_model(request, obj, form, change)

    """"
    MEMBER_STATUS_CHOICES = (
        ('ACTIVE','활동'),
        ('BANNED', '정지'),
        ('WITHDRAWAL', '탈퇴')
    )
    """
    """
    MEMBER_BLOCK_CHOICES = (
        (0, '정지하지 않음'),
        (3, '3일 정지'),
        (7, '7일 정지'),
        (30, '30일 정지')
    )
    """
    """
    REPORT_TYPE_CHOICES = (
        ("WAITING", "검사 대기"),
        ("PENDING", "관리자 확인 대기"),
        ("VALID", "유효한 신고"),
        ("INVALID", "유효하지 않은 신고")
    )"""


admin.site.register(Report, ReportAdmin)
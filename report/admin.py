from django.contrib import admin
from .models import Report
from board.models.post_models import Post
from board.models.comment_models import Comment

from django.urls import reverse
from django.utils.html import format_html

# Register your models here.


class ReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'reported_at', 'target']
    list_display_links = ['status', 'target']
    list_filter = ['status']

    actions = ["action_change_valid", "action_change_invalid"]

    fields = ('status', 'reported_at', 'target_body')
    readonly_fields = ('reported_at', 'target_body')

    def target_body(self, obj):
        if obj.post:
            return obj.post.body
        elif obj.comment:
            return obj.comment.body
    target_body.short_description = '신고 내용'
    
    def target(self, obj):
        if obj.post:
            link = reverse('admin:board_post_change', args=[obj.post.id])
            return format_html('<a href="{}">{}</a>', link, f"게시글 신고 : {obj.post.body}")
        elif obj.comment:
            link = reverse('admin:board_comment_change', args=[obj.comment.id])
            return format_html('<a href="{}">{}</a>', link, f"댓글 신고 : {obj.comment.body}")
        
    target.short_description = '신고글'
    
    def action_change_valid(self, request, queryset):
        for report in queryset:
            report.status=Report.ReportType.VALID
            self.save_model(request, report, None, True)

    action_change_valid.short_description = "선택한 신고의 상태를 유효한 신고로 바꿉니다."
    
    def action_change_invalid(self, request, queryset):
        queryset.update(status=Report.ReportType.INVALID)
    
    action_change_invalid.short_description = "선택한 신고의 상태를 유효하지 않은 신고로 바꿉니다."

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
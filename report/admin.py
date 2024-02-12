from django.contrib import admin
from .models import Report
from board.models.post_models import Post
from board.models.comment_models import Comment

# Register your models here.


class ReportAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if change:
            if obj.post:
                if obj.status == Report.ReportType.VALID:
                    obj.post.is_blocked = True
                elif obj.status == Report.ReportType.INVALID:
                    obj.post.is_blocked = False
                obj.post.save()
            if obj.comment:
                if obj.status == Report.ReportType.VALID:
                    obj.comment.is_blocked = True
                elif obj.status == Report.ReportType.INVALID:
                    obj.comment.is_blocked = False
                obj.comment.save()

        super().save_model(request, obj, form, change)


admin.site.register(Report, ReportAdmin)
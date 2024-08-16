from django.urls import path
from report.views.report_views import *
from report.views.block_views import *

app_name = 'report'

urlpatterns = [
    path('<str:target_type>/<int:target_id>/', CreateReportView.as_view()),
    path('block/', blockPostOrCommentView.as_view())
]
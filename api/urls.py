from django.urls import path
from .views import (
    report_api_view,
    report_add_view,
    report_detail_view,
    report_attachment_media,
    UserLoginApiView,
    UserRegisterApiView
)

urlpatterns = [
    path('report/',report_api_view),
    path('report/<int:pk>/',report_detail_view),
    path('report/add/',report_add_view),
    path('report-attachment/<path:path>',report_attachment_media),
    path('users/register/',UserRegisterApiView.as_view()),
    path('users/login/',UserLoginApiView.as_view()),
]
from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    # Comment management
    path('approve/<int:comment_id>/', views.approve_comment, name='approve_comment'),
    path('reject/<int:comment_id>/', views.reject_comment, name='reject_comment'),
    path('report/<int:comment_id>/', views.report_comment, name='report_comment'),
    
    # Reply management
    path('reply/approve/<int:reply_id>/', views.approve_reply, name='approve_reply'),
    path('reply/reject/<int:reply_id>/', views.reject_reply, name='reject_reply'),
    path('reply/report/<int:reply_id>/', views.report_reply, name='report_reply'),
    
    # Admin moderation dashboard (staff only)
    path('moderation/', views.moderation_dashboard, name='moderation_dashboard'),
    path('moderation/reported/', views.reported_comments, name='reported_comments'),
    path('moderation/pending/', views.pending_comments, name='pending_comments'),
] 
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Profile management
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('profile/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    
    # User dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('dashboard/posts/', views.UserPostsView.as_view(), name='user_posts'),
    path('dashboard/drafts/', views.UserDraftsView.as_view(), name='user_drafts'),
    path('dashboard/comments/', views.UserCommentsView.as_view(), name='user_comments'),
    
    # Authentication (supplementary to allauth)
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('register/', views.CustomRegisterView.as_view(), name='register'),
    
    # Public profile
    path('user/<str:username>/', views.PublicProfileView.as_view(), name='public_profile'),
] 
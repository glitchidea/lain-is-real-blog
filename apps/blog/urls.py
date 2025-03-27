from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Post list and filtering
    path('', views.PostListView.as_view(), name='post_list'),
    path('search/', views.search_view, name='search'),
    path('category/<slug:category_slug>/', views.PostListView.as_view(), name='category'),
    path('tag/<slug:tag_slug>/', views.PostListView.as_view(), name='tag'),
    path('author/<str:username>/', views.PostListView.as_view(), name='author_posts'),
    
    # Post detail
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # Post creation and management - DISABLED
    # path('new/', views.PostCreateView.as_view(), name='new_post'),
    # path('edit/<slug:slug>/', views.PostUpdateView.as_view(), name='post_edit'),
    # path('delete/<slug:slug>/', views.PostDeleteView.as_view(), name='delete_post'),
    # path('publish/<slug:slug>/', views.publish_post, name='publish_post'),
    
    # Comment management
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/reply/', views.add_reply, name='add_reply'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('reply/<int:reply_id>/delete/', views.delete_reply, name='delete_reply'),
    
    # Category and tag listings
    path('categories/', views.CategoryListView.as_view(), name='categories'),
    path('tags/', views.TagListView.as_view(), name='tags'),
    
    # About page
    path('about/', views.about_view, name='about'),
    
    # API endpoints for AJAX requests
    path('api/images/upload/', views.upload_image, name='image_upload'),
    path('api/images/gallery/', views.get_gallery, name='image_gallery'),
] 
from django.urls import path
from . import views

app_name = 'media'

urlpatterns = [
    # Media management 
    path('', views.media_dashboard, name='dashboard'),
    path('upload/', views.upload_media, name='upload'),
    path('browse/', views.browse_media, name='browse'),
    path('delete/<int:media_id>/', views.delete_media, name='delete'),
    path('edit/<int:media_id>/', views.edit_media, name='edit'),
    
    # API endpoints for AJAX requests
    path('api/upload/', views.api_upload, name='api_upload'),
    path('api/list/', views.api_list_media, name='api_list'),
    path('api/delete/<int:media_id>/', views.api_delete_media, name='api_delete'),
    
    # Galleries
    path('galleries/', views.gallery_list, name='gallery_list'),
    path('galleries/create/', views.gallery_create, name='gallery_create'),
    path('galleries/<int:gallery_id>/', views.gallery_detail, name='gallery_detail'),
    path('galleries/<int:gallery_id>/edit/', views.gallery_edit, name='gallery_edit'),
    path('galleries/<int:gallery_id>/delete/', views.gallery_delete, name='gallery_delete'),
    
    # Gallery items
    path('galleries/<int:gallery_id>/add-items/', views.gallery_add_items, name='gallery_add_items'),
    path('galleries/item/<int:item_id>/remove/', views.gallery_remove_item, name='gallery_remove_item'),
    path('galleries/item/<int:item_id>/set-order/<int:order>/', views.gallery_set_item_order, name='gallery_set_item_order'),
] 
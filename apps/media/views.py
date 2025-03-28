from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.http import require_POST, require_http_methods
from django.core.files.storage import default_storage
from django.conf import settings
import os
import mimetypes
from pathlib import Path

from .models import MediaFile, Gallery, GalleryItem
from .forms import MediaFileForm, BulkUploadForm, GalleryForm, GalleryItemForm, GalleryItemBulkForm

import logging
import json

logger = logging.getLogger('apps')


@login_required
def media_dashboard(request):
    """Dashboard for managing media files."""
    media_files = MediaFile.objects.filter(uploaded_by=request.user).order_by('-created_at')
    galleries = Gallery.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Filter by type
    media_type = request.GET.get('type')
    if media_type:
        media_files = media_files.filter(upload_type=media_type)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        media_files = media_files.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(alt_text__icontains=search_query)
        )
    
    # Pagination for media files
    paginator = Paginator(media_files, 20)
    page = request.GET.get('page')
    try:
        files = paginator.page(page)
    except PageNotAnInteger:
        files = paginator.page(1)
    except EmptyPage:
        files = paginator.page(paginator.num_pages)
    
    # Statistics
    stats = {
        'total_files': MediaFile.objects.filter(uploaded_by=request.user).count(),
        'images': MediaFile.objects.filter(uploaded_by=request.user, upload_type='images').count(),
        'documents': MediaFile.objects.filter(uploaded_by=request.user, upload_type='documents').count(),
        'videos': MediaFile.objects.filter(uploaded_by=request.user, upload_type='videos').count(),
        'audio': MediaFile.objects.filter(uploaded_by=request.user, upload_type='audio').count(),
        'galleries': galleries.count(),
    }
    
    context = {
        'files': files,
        'galleries': galleries[:5],  # Show only the 5 most recent galleries
        'stats': stats,
        'media_type': media_type,
        'search_query': search_query,
    }
    
    return render(request, 'media/dashboard.html', context)


@login_required
@require_http_methods(["POST"])
def upload_media(request):
    if 'upload' not in request.FILES:
        return JsonResponse({'error': 'No file was uploaded.'}, status=400)
    
    uploaded_file = request.FILES['upload']
    content_type = uploaded_file.content_type
    
    if content_type not in settings.MEDIA_LIBRARY_ALLOWED_TYPES:
        return JsonResponse({'error': 'File type not allowed.'}, status=400)
    
    # Generate a unique filename
    filename = uploaded_file.name
    path = os.path.join(settings.MEDIA_LIBRARY_UPLOAD_PATH, filename)
    
    # Save the file
    path = default_storage.save(path, uploaded_file)
    url = default_storage.url(path)
    
    return JsonResponse({
        'url': url,
        'fileName': filename,
        'uploaded': True
    })


@login_required
def browse_media(request):
    files = []
    media_path = Path(settings.MEDIA_ROOT) / settings.MEDIA_LIBRARY_UPLOAD_PATH
    
    if media_path.exists():
        for file_path in media_path.rglob('*'):
            if file_path.is_file():
                rel_path = file_path.relative_to(settings.MEDIA_ROOT)
                url = settings.MEDIA_URL + str(rel_path)
                mime_type, _ = mimetypes.guess_type(str(file_path))
                
                if mime_type in settings.MEDIA_LIBRARY_ALLOWED_TYPES:
                    files.append({
                        'url': url,
                        'fileName': file_path.name,
                        'fileSize': file_path.stat().st_size,
                        'type': mime_type
                    })
    
    return JsonResponse({
        'files': files
    })


@login_required
def edit_media(request, media_id):
    """Edit a media file."""
    media_file = get_object_or_404(MediaFile, id=media_id)
    
    # Check if user is the owner
    if media_file.uploaded_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to edit this file.")
    
    if request.method == 'POST':
        form = MediaFileForm(request.POST, request.FILES, instance=media_file)
        if form.is_valid():
            form.save()
            messages.success(request, "File updated successfully.")
            return redirect('media:dashboard')
    else:
        form = MediaFileForm(instance=media_file)
    
    context = {
        'form': form,
        'media_file': media_file,
    }
    
    return render(request, 'media/edit_form.html', context)


@login_required
def delete_media(request, media_id):
    """Delete a media file."""
    media_file = get_object_or_404(MediaFile, id=media_id)
    
    # Check if user is the owner
    if media_file.uploaded_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to delete this file.")
    
    if request.method == 'POST':
        media_file.delete()
        messages.success(request, "File deleted successfully.")
        return redirect('media:dashboard')
    
    context = {
        'media_file': media_file,
    }
    
    return render(request, 'media/delete_confirm.html', context)


@login_required
def gallery_list(request):
    """List all galleries."""
    galleries = Gallery.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        galleries = galleries.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(galleries, 12)  # Show 12 galleries per page
    page = request.GET.get('page')
    try:
        gallery_items = paginator.page(page)
    except PageNotAnInteger:
        gallery_items = paginator.page(1)
    except EmptyPage:
        gallery_items = paginator.page(paginator.num_pages)
    
    context = {
        'galleries': gallery_items,
        'search_query': search_query,
    }
    
    return render(request, 'media/gallery_list.html', context)


@login_required
def gallery_create(request):
    """Create a new gallery."""
    if request.method == 'POST':
        form = GalleryForm(request.POST)
        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.created_by = request.user
            gallery.save()
            messages.success(request, "Gallery created successfully.")
            return redirect('media:gallery_add_items', gallery_id=gallery.id)
    else:
        form = GalleryForm()
    
    context = {
        'form': form,
    }
    
    return render(request, 'media/gallery_form.html', context)


@login_required
def gallery_detail(request, gallery_id):
    """View a gallery's details and items."""
    gallery = get_object_or_404(Gallery, id=gallery_id)
    
    # Check if user can view this gallery
    if not gallery.is_public and gallery.created_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to view this gallery.")
    
    items = gallery.items.all().order_by('order', 'created_at')
    
    context = {
        'gallery': gallery,
        'items': items,
    }
    
    return render(request, 'media/gallery_detail.html', context)


@login_required
def gallery_edit(request, gallery_id):
    """Edit a gallery."""
    gallery = get_object_or_404(Gallery, id=gallery_id)
    
    # Check if user is the owner
    if gallery.created_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to edit this gallery.")
    
    if request.method == 'POST':
        form = GalleryForm(request.POST, instance=gallery)
        if form.is_valid():
            form.save()
            messages.success(request, "Gallery updated successfully.")
            return redirect('media:gallery_detail', gallery_id=gallery.id)
    else:
        form = GalleryForm(instance=gallery)
    
    context = {
        'form': form,
        'gallery': gallery,
    }
    
    return render(request, 'media/gallery_form.html', context)


@login_required
def gallery_delete(request, gallery_id):
    """Delete a gallery."""
    gallery = get_object_or_404(Gallery, id=gallery_id)
    
    # Check if user is the owner
    if gallery.created_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to delete this gallery.")
    
    if request.method == 'POST':
        gallery.delete()
        messages.success(request, "Gallery deleted successfully.")
        return redirect('media:gallery_list')
    
    context = {
        'gallery': gallery,
    }
    
    return render(request, 'media/gallery_delete_confirm.html', context)


@login_required
def gallery_add_items(request, gallery_id):
    """Add items to a gallery."""
    gallery = get_object_or_404(Gallery, id=gallery_id)
    
    # Check if user is the owner
    if gallery.created_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to modify this gallery.")
    
    if request.method == 'POST':
        # Bulk add form
        form = GalleryItemBulkForm(request.POST, user=request.user)
        if form.is_valid():
            media_files = form.cleaned_data['media_files']
            
            # Get the highest current order
            highest_order = 0
            if gallery.items.exists():
                highest_order = gallery.items.order_by('-order').first().order
            
            # Add items to gallery
            for i, media_file in enumerate(media_files):
                # Skip if already in the gallery
                if not GalleryItem.objects.filter(gallery=gallery, media_file=media_file).exists():
                    GalleryItem.objects.create(
                        gallery=gallery,
                        media_file=media_file,
                        order=highest_order + i + 1
                    )
            
            messages.success(request, f"{len(media_files)} items added to gallery.")
            return redirect('media:gallery_detail', gallery_id=gallery.id)
    else:
        form = GalleryItemBulkForm(user=request.user)
    
    # Get already added items
    items = gallery.items.all().order_by('order')
    
    context = {
        'form': form,
        'gallery': gallery,
        'items': items,
    }
    
    return render(request, 'media/gallery_add_items.html', context)


@login_required
def gallery_remove_item(request, item_id):
    """Remove an item from a gallery."""
    item = get_object_or_404(GalleryItem, id=item_id)
    gallery = item.gallery
    
    # Check if user is the owner
    if gallery.created_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to modify this gallery.")
    
    if request.method == 'POST':
        item.delete()
        messages.success(request, "Item removed from gallery.")
    
    return redirect('media:gallery_detail', gallery_id=gallery.id)


@login_required
@require_POST
def gallery_set_item_order(request, item_id, order):
    """Set the order of a gallery item."""
    item = get_object_or_404(GalleryItem, id=item_id)
    gallery = item.gallery
    
    # Check if user is the owner
    if gallery.created_by != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to modify this gallery.")
    
    item.order = order
    item.save()
    
    return JsonResponse({'success': True})


@login_required
@require_POST
def api_upload(request):
    """API endpoint for uploading files via AJAX."""
    if not request.FILES.get('file'):
        return JsonResponse({'success': False, 'error': 'No file provided'})
    
    file = request.FILES.get('file')
    title = request.POST.get('title', '')
    description = request.POST.get('description', '')
    alt_text = request.POST.get('alt_text', '')
    upload_type = request.POST.get('upload_type', 'images')
    is_public = request.POST.get('is_public', 'true') == 'true'
    
    try:
        # Determine upload_type if not provided
        if not upload_type:
            mime_type, _ = mimetypes.guess_type(file.name)
            if mime_type:
                if mime_type.startswith('image/'):
                    upload_type = 'images'
                elif mime_type.startswith('video/'):
                    upload_type = 'videos'
                elif mime_type.startswith('audio/'):
                    upload_type = 'audio'
                else:
                    upload_type = 'documents'
        
        # Create the media file
        media_file = MediaFile.objects.create(
            title=title or file.name,
            description=description,
            file=file,
            upload_type=upload_type,
            alt_text=alt_text,
            uploaded_by=request.user,
            is_public=is_public,
            mime_type=mimetypes.guess_type(file.name)[0] or ''
        )
        
        return JsonResponse({
            'success': True,
            'id': media_file.id,
            'url': media_file.file.url,
            'title': media_file.title,
            'mime_type': media_file.mime_type,
            'upload_type': media_file.upload_type,
            'is_image': media_file.is_image,
            'size': media_file.human_readable_size
        })
    except Exception as e:
        logger.error(f"Error in api_upload: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})


@login_required
def api_list_media(request):
    """API endpoint for listing media files."""
    upload_type = request.GET.get('type', 'images')
    search = request.GET.get('search', '')
    page = int(request.GET.get('page', 1))
    per_page = int(request.GET.get('per_page', 24))
    
    # Get media files, including public ones from other users
    media_files = MediaFile.objects.filter(
        Q(uploaded_by=request.user) | Q(is_public=True)
    )
    
    # Filter by type
    if upload_type != 'all':
        media_files = media_files.filter(upload_type=upload_type)
    
    # Search
    if search:
        media_files = media_files.filter(
            Q(title__icontains=search) |
            Q(description__icontains=search) |
            Q(alt_text__icontains=search)
        )
    
    # Order by creation date, newest first
    media_files = media_files.order_by('-created_at')
    
    # Paginate
    paginator = Paginator(media_files, per_page)
    try:
        page_obj = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)
    
    # Prepare data
    data = {
        'files': [
            {
                'id': media.id,
                'title': media.title,
                'url': media.file.url,
                'thumbnail': media.thumbnail_url if hasattr(media, 'thumbnail_url') else media.file.url,
                'type': media.upload_type,
                'mime_type': media.mime_type,
                'size': media.human_readable_size,
                'is_public': media.is_public,
                'created_at': media.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'is_image': media.is_image,
                'is_mine': media.uploaded_by == request.user,
            }
            for media in page_obj.object_list
        ],
        'total': paginator.count,
        'pages': paginator.num_pages,
        'current_page': page,
        'has_next': page_obj.has_next(),
        'has_prev': page_obj.has_previous(),
    }
    
    return JsonResponse(data)


@login_required
@require_POST
def api_delete_media(request, media_id):
    """API endpoint for deleting a media file."""
    media_file = get_object_or_404(MediaFile, id=media_id)
    
    # Check if user is the owner
    if media_file.uploaded_by != request.user and not request.user.is_staff:
        return JsonResponse({'success': False, 'error': 'Permission denied'}, status=403)
    
    try:
        media_file.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        logger.error(f"Error in api_delete_media: {str(e)}")
        return JsonResponse({'success': False, 'error': str(e)})

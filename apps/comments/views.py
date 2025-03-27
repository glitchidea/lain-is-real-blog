from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseForbidden

from .models import Comment, Reply
from .forms import CommentModerationForm, ReplyModerationForm
from apps.blog.models import Post

import logging

logger = logging.getLogger('apps')


def is_staff(user):
    """Check if the user is a staff member."""
    return user.is_staff


@login_required
@user_passes_test(is_staff)
def approve_comment(request, comment_id):
    """Approve a comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_approved = True
    comment.save()
    messages.success(request, f"Comment by {comment.author.username} has been approved.")
    
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect('blog:post_detail', slug=comment.post.slug)


@login_required
@user_passes_test(is_staff)
def reject_comment(request, comment_id):
    """Reject a comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_approved = False
    comment.save()
    messages.success(request, f"Comment by {comment.author.username} has been rejected.")
    
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect('blog:post_detail', slug=comment.post.slug)


@login_required
def report_comment(request, comment_id):
    """Report a comment as inappropriate."""
    comment = get_object_or_404(Comment, id=comment_id)
    
    # In a real application, you would save the report to a database
    # Here we'll just mark it as not approved and notify admins
    comment.is_approved = False
    comment.save()
    
    # Log the report
    logger.info(f"Comment {comment_id} reported by {request.user.username}")
    
    messages.success(request, "Thank you for reporting this comment. It has been sent for review.")
    return redirect('blog:post_detail', slug=comment.post.slug)


@login_required
@user_passes_test(is_staff)
def approve_reply(request, reply_id):
    """Approve a reply."""
    reply = get_object_or_404(Reply, id=reply_id)
    reply.is_approved = True
    reply.save()
    messages.success(request, f"Reply by {reply.author.username} has been approved.")
    
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect('blog:post_detail', slug=reply.comment.post.slug)


@login_required
@user_passes_test(is_staff)
def reject_reply(request, reply_id):
    """Reject a reply."""
    reply = get_object_or_404(Reply, id=reply_id)
    reply.is_approved = False
    reply.save()
    messages.success(request, f"Reply by {reply.author.username} has been rejected.")
    
    if request.GET.get('next'):
        return redirect(request.GET.get('next'))
    return redirect('blog:post_detail', slug=reply.comment.post.slug)


@login_required
def report_reply(request, reply_id):
    """Report a reply as inappropriate."""
    reply = get_object_or_404(Reply, id=reply_id)
    
    # In a real application, you would save the report to a database
    # Here we'll just mark it as not approved and notify admins
    reply.is_approved = False
    reply.save()
    
    # Log the report
    logger.info(f"Reply {reply_id} reported by {request.user.username}")
    
    messages.success(request, "Thank you for reporting this reply. It has been sent for review.")
    return redirect('blog:post_detail', slug=reply.comment.post.slug)


@login_required
@user_passes_test(is_staff)
def moderation_dashboard(request):
    """Dashboard for moderating comments and replies."""
    comments = Comment.objects.all().order_by('-created_at')
    replies = Reply.objects.all().order_by('-created_at')
    
    # Filter by approval status if specified
    filter_status = request.GET.get('status')
    if filter_status == 'approved':
        comments = comments.filter(is_approved=True)
        replies = replies.filter(is_approved=True)
    elif filter_status == 'pending':
        comments = comments.filter(is_approved=False)
        replies = replies.filter(is_approved=False)
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        comments = comments.filter(
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(post__title__icontains=search_query)
        )
        replies = replies.filter(
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(comment__content__icontains=search_query)
        )
    
    # Pagination for comments
    comment_paginator = Paginator(comments, 10)
    comment_page = request.GET.get('comment_page')
    try:
        comment_items = comment_paginator.page(comment_page)
    except PageNotAnInteger:
        comment_items = comment_paginator.page(1)
    except EmptyPage:
        comment_items = comment_paginator.page(comment_paginator.num_pages)
    
    # Pagination for replies
    reply_paginator = Paginator(replies, 10)
    reply_page = request.GET.get('reply_page')
    try:
        reply_items = reply_paginator.page(reply_page)
    except PageNotAnInteger:
        reply_items = reply_paginator.page(1)
    except EmptyPage:
        reply_items = reply_paginator.page(reply_paginator.num_pages)
    
    # Statistics
    stats = {
        'total_comments': Comment.objects.count(),
        'approved_comments': Comment.objects.filter(is_approved=True).count(),
        'pending_comments': Comment.objects.filter(is_approved=False).count(),
        'total_replies': Reply.objects.count(),
        'approved_replies': Reply.objects.filter(is_approved=True).count(),
        'pending_replies': Reply.objects.filter(is_approved=False).count(),
    }
    
    context = {
        'comments': comment_items,
        'replies': reply_items,
        'stats': stats,
        'filter_status': filter_status,
        'search_query': search_query,
    }
    
    return render(request, 'comments/moderation_dashboard.html', context)


@login_required
@user_passes_test(is_staff)
def reported_comments(request):
    """View for managing reported comments and replies."""
    # In a real application, you would have a ReportedComment model
    # Here we'll just show non-approved comments as "reported"
    comments = Comment.objects.filter(is_approved=False).order_by('-created_at')
    replies = Reply.objects.filter(is_approved=False).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        comments = comments.filter(
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(post__title__icontains=search_query)
        )
        replies = replies.filter(
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(comment__content__icontains=search_query)
        )
    
    # Pagination for comments
    comment_paginator = Paginator(comments, 10)
    comment_page = request.GET.get('comment_page')
    try:
        comment_items = comment_paginator.page(comment_page)
    except PageNotAnInteger:
        comment_items = comment_paginator.page(1)
    except EmptyPage:
        comment_items = comment_paginator.page(comment_paginator.num_pages)
    
    # Pagination for replies
    reply_paginator = Paginator(replies, 10)
    reply_page = request.GET.get('reply_page')
    try:
        reply_items = reply_paginator.page(reply_page)
    except PageNotAnInteger:
        reply_items = reply_paginator.page(1)
    except EmptyPage:
        reply_items = reply_paginator.page(reply_paginator.num_pages)
    
    context = {
        'comments': comment_items,
        'replies': reply_items,
        'search_query': search_query,
    }
    
    return render(request, 'comments/reported_comments.html', context)


@login_required
@user_passes_test(is_staff)
def pending_comments(request):
    """View for managing pending comments that need approval."""
    comments = Comment.objects.filter(is_approved=False).order_by('-created_at')
    replies = Reply.objects.filter(is_approved=False).order_by('-created_at')
    
    # Search functionality
    search_query = request.GET.get('q')
    if search_query:
        comments = comments.filter(
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(post__title__icontains=search_query)
        )
        replies = replies.filter(
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query) |
            Q(comment__content__icontains=search_query)
        )
    
    # Pagination for comments
    comment_paginator = Paginator(comments, 10)
    comment_page = request.GET.get('comment_page')
    try:
        comment_items = comment_paginator.page(comment_page)
    except PageNotAnInteger:
        comment_items = comment_paginator.page(1)
    except EmptyPage:
        comment_items = comment_paginator.page(comment_paginator.num_pages)
    
    # Pagination for replies
    reply_paginator = Paginator(replies, 10)
    reply_page = request.GET.get('reply_page')
    try:
        reply_items = reply_paginator.page(reply_page)
    except PageNotAnInteger:
        reply_items = reply_paginator.page(1)
    except EmptyPage:
        reply_items = reply_paginator.page(reply_paginator.num_pages)
    
    context = {
        'comments': comment_items,
        'replies': reply_items,
        'search_query': search_query,
    }
    
    return render(request, 'comments/pending_comments.html', context)

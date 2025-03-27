from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import JsonResponse, HttpResponseForbidden
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.utils import timezone

from .models import Post, Category, Image
from .forms import PostForm, SearchForm
from apps.comments.forms import CommentForm
from apps.comments.models import Comment

import json
import logging

logger = logging.getLogger('apps')

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = settings.BLOG_POSTS_PER_PAGE

    def get_queryset(self):
        # Şimdiki zaman filtrelemesi ekle
        now = timezone.now()
        
        # Yayınlanmış ve yayın tarihi şimdiden önce olan (veya eşit) yazıları getir
        queryset = Post.objects.filter(
            status='published',
            published_at__lte=now
        ).order_by('-published_at')
        
        # Handle search
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(excerpt__icontains=search_query)
            )
            
        # Handle category filter
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = queryset.filter(categories=category)
            
        # Handle tag filter
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
            
        # Handle author filter
        username = self.kwargs.get('username')
        if username:
            queryset = queryset.filter(author__username=username)
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = SearchForm(self.request.GET or None)
        
        # Add category context if filtering by category
        category_slug = self.kwargs.get('category_slug')
        if category_slug:
            context['current_category'] = get_object_or_404(Category, slug=category_slug)
            
        # Add tag context if filtering by tag
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            from taggit.models import Tag
            context['current_tag'] = get_object_or_404(Tag, slug=tag_slug)
            
        # Add author context if filtering by author
        username = self.kwargs.get('username')
        if username:
            from django.contrib.auth.models import User
            context['current_author'] = get_object_or_404(User, username=username)
            
        return context

class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_object(self):
        post = super().get_object()
        now = timezone.now()
        
        # İleri tarihli yayınlar için kontrol
        is_future_published = post.status == 'published' and post.published_at and post.published_at > now
        
        # Eğer yazı yayınlanmamış veya ileri tarihli ise ve kullanıcı yazarı veya yetkili değilse 404 ver
        if (post.status != 'published' or is_future_published) and not (
            self.request.user.is_authenticated and 
            (post.author == self.request.user or self.request.user.is_staff)
        ):
            from django.http import Http404
            raise Http404("Post not found")
            
        # Increment view count
        if self.request.user != post.author:
            post.increment_views()
            
        return post
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        
        # İleri tarihli yayın bilgisini kontrol et
        now = timezone.now()
        post = self.object
        
        # İleri tarihli yayın bilgisini context'e ekle
        if post.status == 'published' and post.published_at and post.published_at > now:
            context['is_future_published'] = True
            # Kalan süreyi hesapla
            time_diff = post.published_at - now
            context['days_until_publish'] = time_diff.days
            hours, remainder = divmod(time_diff.seconds, 3600)
            context['hours_until_publish'] = hours
            context['minutes_until_publish'] = remainder // 60
        else:
            context['is_future_published'] = False
        
        # Get comments for this post
        comments = Comment.objects.filter(
            post=self.object
        ).order_by('-created_at')
        
        context['comments'] = comments
        context['related_posts'] = self.object.related_posts
        
        return context

class PostCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        """Only allow superusers to create posts."""
        return self.request.user.is_superuser
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "Post created successfully.")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Post'
        return context
    
    def get_success_url(self):
        if self.object.status == 'draft':
            messages.info(self.request, "Post saved as draft.")
            return reverse('blog:post_edit', kwargs={'slug': self.object.slug})
        return reverse('blog:post_detail', kwargs={'slug': self.object.slug})

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def test_func(self):
        """Only allow superusers or post authors to edit posts."""
        post = self.get_object()
        return self.request.user.is_superuser or (post.author == self.request.user and self.request.user.is_superuser)
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Post updated successfully.")
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Post'
        return context
    
    def get_success_url(self):
        if self.object.status == 'draft':
            messages.info(self.request, "Post saved as draft.")
            return reverse('blog:post_edit', kwargs={'slug': self.object.slug})
        return reverse('blog:post_detail', kwargs={'slug': self.object.slug})

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')
    
    def test_func(self):
        """Only allow superusers or post authors to delete posts."""
        post = self.get_object()
        return self.request.user.is_superuser or (post.author == self.request.user and self.request.user.is_superuser)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted successfully.")
        return super().delete(request, *args, **kwargs)

class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return Category.objects.annotate(
            posts_count=Count('posts', filter=Q(posts__status=Post.Status.PUBLISHED))
        ).filter(posts_count__gt=0).order_by('name')

# AJAX Views
@login_required
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES.get('image')
        title = request.POST.get('title', 'Uploaded Image')
        alt_text = request.POST.get('alt_text', '')
        
        try:
            new_image = Image.objects.create(
                title=title,
                file=image,
                alt_text=alt_text,
                uploader=request.user
            )
            
            return JsonResponse({
                'success': True,
                'url': new_image.file.url,
                'id': new_image.id,
                'title': new_image.title
            })
        except Exception as e:
            logger.error(f"Error uploading image: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)})
    
    return JsonResponse({'success': False, 'error': 'No image provided'})

@login_required
def get_gallery(request):
    images = Image.objects.filter(uploader=request.user).order_by('-created_at')
    data = [{
        'id': img.id,
        'url': img.file.url,
        'title': img.title,
        'alt': img.alt_text,
        'date': img.created_at.strftime('%b %d, %Y')
    } for img in images]
    
    return JsonResponse({'images': data})

# Additional Views
def about_view(request):
    return render(request, 'blog/about.html')

def search_view(request):
    form = SearchForm(request.GET or None)
    results = []
    
    if form.is_valid() and form.cleaned_data.get('q'):
        query = form.cleaned_data.get('q')
        results = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) | 
            Q(excerpt__icontains=query),
            status='published'
        ).order_by('-created_at')
        
    paginator = Paginator(results, settings.BLOG_POSTS_PER_PAGE)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        
    return render(request, 'blog/search_results.html', {
        'form': form,
        'posts': posts,
        'query': form.cleaned_data.get('q', ''),
        'results_count': len(results)
    })

@login_required
def add_comment(request, post_id):
    """Add a comment to a post."""
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect('blog:post_detail', slug=post.slug)
        else:
            messages.error(request, "Error adding comment. Please check the form.")
    
    return redirect('blog:post_detail', slug=post.slug)

@login_required
def add_reply(request, comment_id):
    """Add a reply to a comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            # Create a Reply object instead of Comment with parent
            from apps.comments.models import Reply
            reply = Reply(
                comment=comment,
                author=request.user,
                content=form.cleaned_data['content'],
                is_approved=True
            )
            reply.save()
            messages.success(request, "Reply added successfully.")
            return redirect('blog:post_detail', slug=post.slug)
        else:
            messages.error(request, "Error adding reply. Please check the form.")
    
    return redirect('blog:post_detail', slug=post.slug)

@login_required
def delete_comment(request, comment_id):
    """Delete a comment."""
    comment = get_object_or_404(Comment, id=comment_id)
    post = comment.post
    
    # Check if user is authorized to delete the comment
    if comment.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to delete this comment.")
    
    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Comment deleted successfully.")
    
    return redirect('blog:post_detail', slug=post.slug)

@login_required
def delete_reply(request, reply_id):
    """Delete a reply to a comment."""
    from apps.comments.models import Reply
    reply = get_object_or_404(Reply, id=reply_id)
    comment = reply.comment
    post = comment.post
    
    # Check if user is authorized to delete the reply
    if reply.author != request.user and not request.user.is_staff:
        return HttpResponseForbidden("You do not have permission to delete this reply.")
    
    if request.method == 'POST':
        reply.delete()
        messages.success(request, "Reply deleted successfully.")
    
    return redirect('blog:post_detail', slug=post.slug)

class TagListView(ListView):
    """View to display all tags that have associated posts."""
    template_name = 'blog/tag_list.html'
    context_object_name = 'tags'
    
    def get_queryset(self):
        from taggit.models import Tag
        from django.db.models import Count
        from django.contrib.contenttypes.models import ContentType
        
        # Get the content type for Post model
        post_content_type = ContentType.objects.get_for_model(Post)
        
        # Get tags that have associated published posts and count them
        return Tag.objects.annotate(
            post_count=Count(
                'taggit_taggeditem_items',
                filter=Q(
                    taggit_taggeditem_items__content_type=post_content_type,
                    taggit_taggeditem_items__object_id__in=Post.objects.filter(
                        status=Post.Status.PUBLISHED
                    ).values_list('id', flat=True)
                )
            )
        ).filter(post_count__gt=0).order_by('name')

@login_required
def publish_post(request, slug):
    """View to publish a draft post directly from profile page."""
    post = get_object_or_404(Post, slug=slug, author=request.user)
    
    # Check if user is superuser
    if not request.user.is_superuser:
        messages.error(request, "You do not have permission to publish posts.")
        return redirect('accounts:profile')
    
    # Check if post is a draft
    if post.status == Post.Status.DRAFT:
        post.status = Post.Status.PUBLISHED
        post.published_at = timezone.now()
        post.save()
        messages.success(request, f"'{post.title}' has been published successfully.")
    else:
        messages.info(request, f"'{post.title}' is already published.")
    
    # Redirect back to profile
    return redirect('accounts:profile')

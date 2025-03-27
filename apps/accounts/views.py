from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, UpdateView, ListView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy
from django.db.models import Count, Sum

from .models import UserProfile
from .forms import UserProfileForm, CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordChangeForm
from apps.blog.models import Post
from apps.comments.models import Comment

import logging

logger = logging.getLogger('apps')


class ProfileView(LoginRequiredMixin, DetailView):
    """View to display a user's profile."""
    model = UserProfile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        """Return the current user's profile."""
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get user's posts (both published and drafts)
        posts = Post.objects.filter(author=user).order_by('-created_at')
        
        # Add all posts to context
        context['posts'] = posts[:10]  # Limit to 10 most recent posts
        context['post_count'] = posts.count()
        
        # Add published posts count
        context['published_post_count'] = Post.objects.filter(
            author=user, status=Post.Status.PUBLISHED
        ).count()
        
        # Add draft posts count
        context['draft_post_count'] = Post.objects.filter(
            author=user, status=Post.Status.DRAFT
        ).count()
        
        # Get user's comments
        context['comments'] = Comment.objects.filter(author=user).order_by('-created_at')[:5]
        context['comment_count'] = Comment.objects.filter(author=user).count()
        
        return context


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """View to edit a user's profile."""
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        """Return the current user's profile."""
        return self.request.user.profile

    def get_form_kwargs(self):
        """Pass user to the form."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_initial(self):
        """Set initial form values from user model and profile."""
        initial = super().get_initial()
        user = self.request.user
        profile = self.get_object()
        
        # User model fields
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        initial['email'] = user.email
        
        # Profile model fields
        for field in self.form_class.Meta.fields:
            if hasattr(profile, field) and getattr(profile, field):
                initial[field] = getattr(profile, field)
                
        return initial

    def form_valid(self, form):
        """Save user data and return success message."""
        form.save(user=self.request.user)
        messages.success(self.request, "Profiliniz başarıyla güncellendi.")
        return redirect(self.success_url)


class ChangePasswordView(LoginRequiredMixin, PasswordChangeView):
    """View to change user's password."""
    form_class = CustomPasswordChangeForm
    template_name = 'accounts/change_password.html'
    success_url = reverse_lazy('accounts:profile')

    def form_valid(self, form):
        messages.success(self.request, "Your password has been changed successfully.")
        return super().form_valid(form)


class DashboardView(LoginRequiredMixin, TemplateView):
    """View for the user dashboard."""
    template_name = 'accounts/dashboard.html'

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get post statistics
        context['post_count'] = Post.objects.filter(author=user).count()
        context['published_post_count'] = Post.objects.filter(
            author=user, status=Post.Status.PUBLISHED
        ).count()
        context['draft_post_count'] = Post.objects.filter(
            author=user, status=Post.Status.DRAFT
        ).count()
        
        # Get view statistics
        context['total_views'] = Post.objects.filter(author=user).aggregate(
            total_views=Sum('views_count')
        )['total_views'] or 0
        
        # Get comment statistics
        context['comment_count'] = Comment.objects.filter(author=user).count()
        context['comments_received'] = Comment.objects.filter(post__author=user).count()
        
        # Get recent activity
        context['recent_posts'] = Post.objects.filter(author=user).order_by('-created_at')[:5]
        context['recent_comments'] = Comment.objects.filter(author=user).order_by('-created_at')[:5]
        
        return context


class UserPostsView(LoginRequiredMixin, ListView):
    """View to display all posts by the current user."""
    model = Post
    template_name = 'accounts/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        """Return all posts by the current user."""
        return Post.objects.filter(author=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        context['published_count'] = Post.objects.filter(
            author=self.request.user, status=Post.Status.PUBLISHED
        ).count()
        context['draft_count'] = Post.objects.filter(
            author=self.request.user, status=Post.Status.DRAFT
        ).count()
        return context


class UserDraftsView(LoginRequiredMixin, ListView):
    """View to display all draft posts by the current user."""
    model = Post
    template_name = 'accounts/user_drafts.html'
    context_object_name = 'drafts'
    paginate_by = 10

    def get_queryset(self):
        """Return all draft posts by the current user."""
        return Post.objects.filter(
            author=self.request.user, status=Post.Status.DRAFT
        ).order_by('-created_at')
        
    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        
        # Get the oldest draft separately for stats
        oldest_draft = Post.objects.filter(
            author=self.request.user, status=Post.Status.DRAFT
        ).order_by('created_at').first()
        
        context['oldest_draft'] = oldest_draft
        context['draft_count'] = Post.objects.filter(
            author=self.request.user, status=Post.Status.DRAFT
        ).count()
        
        return context


class UserCommentsView(LoginRequiredMixin, ListView):
    """View to display all comments by the current user."""
    model = Comment
    template_name = 'accounts/user_comments.html'
    context_object_name = 'comments'
    paginate_by = 20

    def get_queryset(self):
        """Return all comments by the current user."""
        return Comment.objects.filter(author=self.request.user).order_by('-created_at')


class CustomLoginView(LoginView):
    """Custom login view with styled form."""
    form_class = CustomAuthenticationForm
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        """Add success message on login."""
        messages.success(self.request, "You have successfully logged in.")
        return super().form_valid(form)


class CustomLogoutView(LogoutView):
    """Custom logout view with redirect."""
    next_page = 'home'

    def dispatch(self, request, *args, **kwargs):
        """Add success message on logout."""
        messages.success(request, "You have successfully logged out.")
        return super().dispatch(request, *args, **kwargs)


class CustomRegisterView(TemplateView):
    """View for user registration."""
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm

    def get_context_data(self, **kwargs):
        """Add registration form to the context."""
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        """Handle form submission."""
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Your account has been created. You can now log in.")
            return redirect('accounts:login')
        return render(request, self.template_name, {'form': form})


class PublicProfileView(DetailView):
    """View to display a user's public profile."""
    model = User
    template_name = 'accounts/public_profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self, queryset=None):
        """Get the user by username from URL."""
        return get_object_or_404(User, username=self.kwargs['username'])
    
    def get_context_data(self, **kwargs):
        """Add additional context data."""
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        # Get published posts by this user
        context['posts'] = Post.objects.filter(
            author=user, status=Post.Status.PUBLISHED
        ).order_by('-created_at')[:10]
        
        # Get post statistics
        context['post_count'] = Post.objects.filter(
            author=user, status=Post.Status.PUBLISHED
        ).count()
        
        # Get popular posts
        context['popular_posts'] = Post.objects.filter(
            author=user, status=Post.Status.PUBLISHED
        ).order_by('-views_count')[:5]
        
        return context

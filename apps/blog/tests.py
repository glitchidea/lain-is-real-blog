from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from .models import Post, Category
from .context_processors import blog_context
from django.utils import timezone


class BlogContextProcessorTests(TestCase):
    """Tests for the blog context processor."""
    
    def setUp(self):
        """Set up test data."""
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword'
        )
        
        # Create categories
        self.category1 = Category.objects.create(
            name='Test Category 1',
            slug='test-category-1',
            description='Test category 1 description'
        )
        
        # Create posts
        self.post1 = Post.objects.create(
            title='Test Post 1',
            slug='test-post-1',
            author=self.user,
            content='Test content 1',
            status=Post.Status.PUBLISHED,
            published_at=timezone.now()
        )
        self.post1.categories.add(self.category1)
        self.post1.tags.add('test', 'django')
        
        # Create featured post
        self.featured_post = Post.objects.create(
            title='Featured Post',
            slug='featured-post',
            author=self.user,
            content='Featured content',
            status=Post.Status.PUBLISHED,
            is_featured=True,
            published_at=timezone.now()
        )
        self.featured_post.categories.add(self.category1)
        
        # Create draft post (should not appear in context)
        self.draft_post = Post.objects.create(
            title='Draft Post',
            slug='draft-post',
            author=self.user,
            content='Draft content',
            status=Post.Status.DRAFT
        )
    
    def test_context_keys(self):
        """Test that blog_context returns the expected context keys."""
        request = self.factory.get('/')
        context = blog_context(request)
        
        # Test that context contains expected keys
        self.assertIn('categories', context)
        self.assertIn('categories_list', context)
        self.assertIn('popular_tags', context)
        self.assertIn('latest_posts', context)
        self.assertIn('latest_posts_list', context)
        self.assertIn('featured_posts', context)
        self.assertIn('featured_posts_list', context)
        self.assertIn('blog_settings', context)
        
        # Test basic settings
        self.assertIn('posts_per_page', context['blog_settings'])
        self.assertIn('allow_comments', context['blog_settings'])

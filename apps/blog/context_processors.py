from django.conf import settings
from .models import Category, Post
from django.db.models import Count, Q
from taggit.models import Tag
from django.contrib.contenttypes.models import ContentType


def blog_context(request):
    """Context processor for blog app.
    
    Makes common blog data available to all templates.
    """
    # Get categories with post count (only published posts)
    categories = Category.objects.annotate(
        posts_count=Count('posts', filter=Q(posts__status=Post.Status.PUBLISHED))
    ).filter(posts_count__gt=0).order_by('-posts_count')
    
    # Get post content type for filtering
    post_content_type = ContentType.objects.get_for_model(Post)
    
    # Get popular tags (only from published posts)
    # We need to join through the ContentType and match on the Post model's ID
    popular_tags = Tag.objects.annotate(
        post_count=Count(
            'taggit_taggeditem_items',
            filter=Q(
                taggit_taggeditem_items__content_type=post_content_type,
                taggit_taggeditem_items__object_id__in=Post.objects.filter(
                    status=Post.Status.PUBLISHED
                ).values_list('id', flat=True)
            )
        )
    ).filter(post_count__gt=0).order_by('-post_count')[:10]
    
    # Get latest posts
    latest_posts = Post.objects.filter(status=Post.Status.PUBLISHED).order_by('-published_at')[:5]
    
    # Get featured posts
    featured_posts = Post.objects.filter(status=Post.Status.PUBLISHED, is_featured=True).order_by('-published_at')[:3]
    
    return {
        'categories': categories[:10],  # Top 10 categories
        'categories_list': categories[:10],  # For backward compatibility
        'popular_tags': popular_tags,
        'latest_posts': latest_posts,
        'latest_posts_list': latest_posts,  # For backward compatibility
        'featured_posts': featured_posts,
        'featured_posts_list': featured_posts,  # For backward compatibility
        'blog_settings': {
            'posts_per_page': getattr(settings, 'BLOG_POSTS_PER_PAGE', 10),
            'allow_comments': getattr(settings, 'BLOG_ALLOW_COMMENTS', True),
        }
    } 
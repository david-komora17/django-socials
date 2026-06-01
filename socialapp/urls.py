from django.urls import path
from socialapp.views import (
    RegisterView, LoginView, ProfileDetailView, PostListCreateView, 
    PostDetailView, CommentListCreateView, CommentDetailView, 
    CommentLikeView, FollowUserView, UserSearchView, NewsFeedView
)

urlpatterns = [
    # Auth
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),

    # Profiles
    path('profiles/<int:user_id>/', ProfileDetailView.as_view(), name='profile-detail'),

    # Posts & News Feed
    path('posts/', PostListCreateView.as_view(), name='post-list'),
    path('posts/feed/', NewsFeedView.as_view(), name='news-feed'),
    path('posts/<int:post_id>/', PostDetailView.as_view(), name='post-detail'),

    # Comments
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view(), name='comment-list'),
    path('comments/<int:comment_id>/', CommentDetailView.as_view(), name='comment-detail'),

    # Likes System
    path('comments/<int:comment_id>/like/', CommentLikeView.as_view(), name='comment-like'),

    # Follow System
    path('users/<int:user_id>/follow/', FollowUserView.as_view(), name='user-follow'),

    # Search
    path('search/users/', UserSearchView.as_view(), name='user-search'),
]

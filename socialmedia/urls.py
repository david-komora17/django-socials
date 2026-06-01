"""
URL configuration for socialmedia project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from socialapp.views import (
    RegisterView, LoginView, ProfileDetailView, PostListCreateView, 
    PostDetailView, CommentListCreateView, CommentDetailView, 
    PostLikeView, CommentLikeView, FollowUserView, UserSearchView, NewsFeedView
)

urlpatterns = [
    path('admin/', admin.site.urls),
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
    path('posts/<int:post_id>/like/', PostLikeView.as_view(), name='post-like'),
    path('comments/<int:comment_id>/like/', CommentLikeView.as_view(), name='comment-like'),
]

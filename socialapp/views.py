from django.shortcuts import render
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Profile, Post, Comment, PostLike, CommentLike
from .serializers import UserRegisterSerializer, ProfileSerializer, PostSerializer, CommentSerializer

# Create a permissions check.
class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user
    
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(views.APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': token.key, 'user_id': user.id})
        return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)
    
# --- PROFILES ---
class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'user_id'
    
    def get_permissions(self):
        if self.request.method in permissions.SAFE_METHODS:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
    
# POSTS
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')  
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_url_kwarg = 'post_id'
    permission_classes = [permissions.isAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

# News_feed
class NewsFeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_profile = self.request.user.profile
        # Extract user instances from profiles followed by active user
        followed_profiles = user_profile.following.all()
        followed_users = [prof.user for prof in followed_profiles]
        return Post.objects.filter(author__in=followed_users).order_by('-created_at')
    
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return  Comment.objects.filter(post_id=self.kwargs['post_id'])
    
    def perform_create(self, serializer):
        post_obj = get_object_or_404(Post, id=self.kwargs['post_id'])
        serializer.save(author=self.request.user, post=post_obj)

class commentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    class PostLikeView(views.APIView):
        permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id):
        post_obj = get_object_or_404(Post, id=post_id)
        like, created = PostLike.objects.get_or_create(user=request.user, post=post_obj)
        if not created:
            return Response({'detail': 'Already liked.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Post liked.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        post_obj = get_object_or_404(Post, id=post_id)
        like = PostLike.objects.filter(user=request.user, post=post_obj)
        if like.exists():
            like.delete()
            return Response({'detail': 'Like removed.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not liked yet.'}, status=status.HTTP_400_BAD_REQUEST)

class CommentLikeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, comment_id):
        comment_obj = get_object_or_404(Comment, id=comment_id)
        like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment_obj)
        if not created:
            return Response({'detail': 'Already liked.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'detail': 'Comment liked.'}, status=status.HTTP_201_CREATED)

    def delete(self, request, comment_id):
        comment_obj = get_object_or_404(Comment, id=comment_id)
        like = CommentLike.objects.filter(user=request.user, comment=comment_obj)
        if like.exists():
            like.delete()
            return Response({'detail': 'Like removed.'}, status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': 'Not liked yet.'}, status=status.HTTP_400_BAD_REQUEST)
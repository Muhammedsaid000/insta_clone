from rest_framework import routers
from .views import *
from django.urls import path, include

router=routers.SimpleRouter()
router.register(r'follow', FollowViewSet, basename='follow')
router.register(r'post_photos', PostPhotosViewSet, basename='post_photos')
router.register(r'post_like', PostLikeViewSet, basename='post_like')
router.register(r'comment', CommentViewSet, basename='comment')
router.register(r'comment_like', CommentLikeViewSet, basename='comment_like')
router.register(r'story', StoryViewSet, basename='story')


urlpatterns = [
    path('', include(router.urls)),
    path('post/', PostListAPIView.as_view()),
    path('save/', SaveListAPIView.as_view(), name='save'),
    path('save/<int:pk>/', SavePostAPIView.as_view(),  name='save_post'),
    path('user/', UserProfileListAPIView.as_view(), name='user_list'),
    path('user/<int:pk>/', UserProfileDetailAPIView.as_view(), name='user_detail'),
    path('post/create/', PostCreateAPIView.as_view(), name='post'),
    path('post/create/<int:pk>/', PostEDITAPIVIew.as_view(), name='post_edit'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]



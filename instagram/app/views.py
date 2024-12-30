from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, generics
from .permission import CheckPostEdit
from .serializers import *
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(generics.CreateAPIView):
    serializer_class = ProfileSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'is_registration': True})
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializers

    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail: Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user=serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"detail": "Refresh токен отсутствует."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "Вы вышли из системы."}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": "Ошибка обработки токена."}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileListAPIView(generics.ListAPIView):
        queryset = UserProfile.objects.all()
        serializer_class = UserProfileSerializer
        filter_backends = [ SearchFilter]
        search_fields = ['username']


class UserProfileDetailAPIView(generics.RetrieveUpdateAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileDetailSerializer

    def get_queryset(self):
        return UserProfile.objects.filter(id=self.request.user.id)

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class PostListAPIView(generics.ListAPIView):
     queryset = Post.objects.all()
     serializer_class = PostSerializer
     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
     search_fields = ['username', 'hashtag',]
     ordering_fields = ['post']

class PostCreateAPIView(generics.CreateAPIView):
     serializer_class = PostCreateSerializer

     def get_queryset(self):
        return Post.objects.filter(user=self.request.user)


class PostEDITAPIVIew(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = [CheckPostEdit]


class PostPhotosViewSet(viewsets.ModelViewSet):
    queryset = PostPhotos.objects.all()
    serializer_class = PostPhotosSerializer


class PostLikeViewSet(viewsets.ModelViewSet):
    queryset = PostLike.objects.all()
    serializer_class = PostLikeSerializer

    def get_queryset(self):
       return PostLike.objects.filter(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer

    def get_queryset(self):
        return CommentLike.objects.filter(user=self.request.user)


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    def get_queryset(self):
        return Story.objects.filter(user=self.request.user)


class SaveListAPIView(generics.ListAPIView):
    queryset = SavePost.objects.all()
    serializer_class = SaveSerializer

    def get_queryset(self):
        return SavePost.objects.filter(user=self.request.user)


class SavePostAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SaveItem.objects.all()
    serializer_class = SavePostSerializer

    def get_queryset(self):
        return SaveItem.objects.filter(id=self.request.user.id)

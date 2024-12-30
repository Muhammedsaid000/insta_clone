from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        # Проверяем, был ли вызван create
        if self.context.get('is_registration', False):
            refresh = RefreshToken.for_user(instance)
            return {
                'user': {
                    'username': instance.username,
                    'email': instance.email,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh)
            }
        return super().to_representation(instance)


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные или пользователь неактивен.")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except Exception as e:
            raise serializers.ValidationError({'detail': 'Недействительный или уже отозванный токен'})


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields=['username']


class FollowSerializer(serializers.ModelSerializer):
    follower=UserProfileSerializer(read_only=True)
    following=UserProfileSerializer(read_only=True)
    class Meta:
        model=Follow
        fields=['follower','following','created_at']



class PostPhotosSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostPhotos
        fields=['image']


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=PostLike
        fields=['user']

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model=CommentLike
        fields=['user','created_at','comment']


class CommentSerializer(serializers.ModelSerializer):
    comment_likes=CommentLikeSerializer(many=True, read_only=True)
    get_count_people=serializers.SerializerMethodField()
    class Meta:
        model=Comment
        fields=['text','created_at','post','user','parent_review','comment_likes','get_count_people']

    def get_count_people(self, obj):
        return obj.get_count_people

class PostSerializer(serializers.ModelSerializer):
    user=UserProfileSerializer()
    post_photos=PostPhotosSerializer(many=True, read_only=True)
    post_likes=PostLikeSerializer(many=True, read_only=True)
    get_like_count=serializers.SerializerMethodField()
    post_comments=CommentSerializer(many=True, read_only=True)
    get_count_comment=serializers.SerializerMethodField()
    class Meta:
        model=Post
        fields=['id','user','post_photos','video','get_like_count','get_count_comment','description','hashtag','created_at','post_likes','post_comments']

    def get_like_count(self, obj):
        return obj.get_like_count

    def get_count_comment(self, obj):
        return obj.get_count_people



class PostCreateSerializer(serializers.ModelSerializer):
    post_photos=PostPhotosSerializer(many=True, read_only=True)
    class Meta:
        model=Post
        fields=['video','description','hashtag','user','post_photos',]


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Story
        fields='__all__'


class UserProfileDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields='__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserProfile
        fields='__all__'


class SaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavePost
        fields = '__all__'


class SavePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaveItem
        fields = '__all__'
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserProfile(AbstractUser):
    bio = models.TextField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='user_image/', null=True, blank=True)
    website = models.CharField(max_length=300, null=True, blank=True)


class Follow(models.Model):
    follower = models.ForeignKey(UserProfile, related_name='follower', on_delete=models.CASCADE)
    following = models.ForeignKey(UserProfile, related_name='following', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following',)


class Post(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='post')
    video = models.FileField(upload_to='post_video/', null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    hashtag = models.CharField(max_length=200, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


    def get_like_count(self):
        post = self.post_likes.all()
        if post.exists():
            return post.count()
        return 0

    def get_count_comment(self):
        comment = self.post_comments.all()
        if comment.exists():
            return comment.count()
        return 0


class PostPhotos(models.Model):
     post = models.ForeignKey(Post, related_name='post_photos', on_delete=models.CASCADE)
     image = models.ImageField(upload_to='post_img/')


class PostLike(models.Model):
    user = models.ForeignKey(UserProfile, related_name='liked_posts', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='post_likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together=('user','post',)

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='post_comments', on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    parent_review = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)

    def get_count_people(self):
        comment = self.comment_likes.all()
        if comment.exists():
            return comment.count()
        return 0


class CommentLike(models.Model):
    user = models.ForeignKey(UserProfile, related_name='liked_comments', on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='comment_likes', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'comment',)


class Story(models.Model):
    user = models.ForeignKey(UserProfile, related_name='stories', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='story_image/')
    video = models.FileField(upload_to='story_video/')
    created_at = models.DateTimeField(auto_now_add=True)


class SavePost(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'{self.user}'


class SaveItem(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    save_post = models.ForeignKey(SavePost, related_name='items', on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)



class Chat(models.Model):
    person=models.ManyToManyField(UserProfile)
    created_date=models.DateField(auto_now_add=True)


class Message(models.Model):
    chat=models.ForeignKey(Chat, on_delete=models.CASCADE)
    author=models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text=models.TextField(null=True, blank=True)
    image=models.ImageField(upload_to='images', null=True, blank=True)
    video=models.FileField(upload_to='videos',null=True, blank=True)
    created_date=models.DateTimeField(auto_now_add=True)






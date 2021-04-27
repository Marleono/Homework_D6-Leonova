from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from django.db.models import Sum, F

# Create your models here.
class Author(models.Model):
    user_id = models.OneToOneField(User, on_delete = models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        post_rating = Post.objects.filter(author = self.id).aggregate(total=Sum(F('rating')*3))['total']
        comm_rating = post_rating + Comment.objects.filter(post__author = self.id).aggregate(total=Sum('rating_of_comment'))['total']
        comm_author = post_rating + Comment.objects.filter(user=self.id).aggregate(total=Sum('rating_of_comments'))['total']
        self.save()

class Category(models.Model):
    name = models.CharField(unique = True, max_length = 50)
    subscribers = models.ManyToManyField(User)

    def __str__(self):
        return f'{self.name()}'

class Post(models.Model):
    author = models.ForeignKey(Author, on_delete = models.CASCADE)
    news = 'N'
    article = 'A'
    types = (
        (news, 'новость'),
        (article, 'статья')
    )
    post_type = models.CharField(max_length=1, choices=types, default=news)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    category = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=150)
    text = models.TextField()
    rating = models.IntegerField(default=0)


    def __str__(self):
        return f'{self.title.title()}: {self.text[:300]}'



    def preview(self):
        return self.text[0:124] + "..."

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def get_absolute_url(self):  # добавим абсолютный путь чтобы после создания нас перебрасывало на страницу с товаром
        return f'/news/{self.id}'

class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_text = models.CharField(max_length=255)
    comment_datetime = models.DateTimeField(auto_now_add=True)
    rating_of_comment = models.IntegerField(default=0)

    def like(self):
        self.rating_of_comment += 1
        self.save()

    def dislike(self):
        self.rating_of_comment -= 1
        self.save()


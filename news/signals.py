from django.db.models.signals import post_save
from django.dispatch import receiver # импортируем нужный декоратор
from django.core.mail import mail_managers
from .models import Post, Category, User
from datetime import datetime, timedelta
from django.utils import timezone



def notify_subscribers_news(request, sender, instance, created, **kwargs):
    categories = Category.objects.all()
    subscribers = Category.objects.values_list('subscribers')
    new_posts = Post.objects.filter(created__range=[timezone.now() - timedelta(weeks=1), timezone.now()])
    week_categories = new_posts.values_list('category', flat=True).distinct()
    subscribed_users = User.objects.filter(category__in=week_categories)
    for user in subscribed_users:
            if created:
                subject = f'{instance.username} {instance.date.strftime("%d %m %Y")}'
            else:
                subject = f'Список новостей изменен для {instance.username} {instance.date.strftime("%d %m %Y")}'

            mail_managers(
                subject=subject,
                message=instance.message,
            )
post_save.connect(notify_subscribers_news(), sender=Post)
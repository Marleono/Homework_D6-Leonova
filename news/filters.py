from django_filters import FilterSet  # импортируем filterset, чем-то напоминающий знакомые дженерики
from .models import Post, User
import django_filters

class PostFilter(FilterSet):
    # Здесь в мета классе надо предоставить модель и указать поля по которым будет фильтроваться (т.е. подбираться) информация о товарах
    class Meta:
        model = Post
        fields = {
            'title': ['icontains'],
            'author': ['exact'],
            'created': ['gt'],
        }



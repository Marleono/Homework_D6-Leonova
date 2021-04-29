from django.urls import path
from .views import Posts, PostDetailView, PostCreateView, PostUpdateView, PostDeleteView, CategoryView
from .views import subscribe_me, unsubscribe_me




urlpatterns = [
    path('', Posts.as_view()),
    path('search/', Posts.as_view(), name='posts'),
    path('<int:pk>/', PostDetailView.as_view(), name='news_detail'), # Ссылка на детали товара
    path('add/', PostCreateView.as_view(), name='news_add'), # Ссылка на создание товара
    path('<int:pk>/edit/', PostUpdateView.as_view(), name='news_add'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='news_delete'),
    path('categories/', CategoryView.as_view(), name='subscribe'),
    path('categories/<int:cat_id>/subscribe/', subscribe_me, name='subscribe'),
    path('categories/<int:cat_id>/unsubscribe/', unsubscribe_me, name='subscribe'),
]

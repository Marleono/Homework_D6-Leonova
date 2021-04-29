from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.views import View
from django.core.paginator import Paginator
from datetime import datetime
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail



# Create your views here.


class Posts(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-created']
    paginate_by = 10



    def get_context_data(self, **kwargs): # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса (привет полиморфизм, мы скучали!!!)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) # вписываем наш фильтр в контекст
        return context



class PostDetailView(DetailView):
    template_name = 'news_detail.html'
    queryset = Post.objects.all()

class PostCreateView(CreateView):
    template_name = 'news_add.html'
    form_class = PostForm


class PostUpdateView(UpdateView):
    template_name = 'news_add.html'
    form_class = PostForm

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте который мы собираемся редактировать
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


# дженерик для удаления товара
class PostDeleteView(DeleteView):
    template_name = 'news_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'



class AddPost(PermissionRequiredMixin, CreateView):
    permission_required = ('news.news_add', 'news.news_delete')


class CategoryView(ListView):
    model = Category
    template_name = 'subscribe.html'
    context_object_name = 'category'
    queryset = Category.objects.all()
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['not_subscribed'] = not Category.objects.filter(name='category_id').exists()
        return context

@login_required
def subscribe_me(request,cat_id):
    user = request.user
    category = Category.objects.get(pk=cat_id)
    if request.user not in category.subscribers.all():
        category.subscribers.add(user)
    return redirect('/news/categories/')















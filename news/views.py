from django.shortcuts import render, reverse, redirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import CreateView
from .models import Post, Category
from .filters import PostFilter
from .forms import PostForm
from django.views import View
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



# Create your views here.


class Posts(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = ['-created']
    paginate_by = 10



    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset()) 
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

@login_required
def subscribe_me(request,cat_id):
    user = request.user
    category = Category.objects.get(pk=cat_id)
    if request.user not in category.subscribers.all():
        category.subscribers.add(user)
    return redirect('/news/categories/')

@login_required
def unsubscribe_me(request, cat_id):
   user = request.user
   category = Category.objects.get(pk=cat_id)
   if request.user in category.subscribers.all():
       category.subscribers.remove(user)
   return redirect('/news/categories/')

@login_required
def mail(request):
    category = Category.objects.all()
    subscribers = Category.objects.values_list('subscribers')
    new_posts = Post.objects.filter(created__range=[timezone.now() - timedelta(weeks=1), timezone.now()])
    week_categories = new_posts.values_list('category', flat=True).distinct()
    subscribed_users = User.objects.filter(category__in=week_categories)
    for user in subscribed_users:
        html_content = render_to_string(
            'news_detail.html',
            {
                'post': new_posts,
            }
        )
        msg = EmailMultiAlternatives(
            subject=f'{new_posts.title}',
            message=f'«Здравствуй, {subscribed_users.name}. 
            from_email='test_user_python@mail.ru'
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send()  
        return redirect('/')















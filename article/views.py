from django.http import HttpResponseForbidden, HttpResponseRedirect
from django.urls import reverse_lazy
from django.shortcuts import render, render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from article.models import Article
from .forms import ArticleForm
from .tools import get_article_background


def home(request):
    paginator = Paginator(Article.objects.all(), 10)
    page = request.GET.get('page')
    try:
        articles = paginator.page(page)
    except PageNotAnInteger:
        articles = paginator.page(1)
    except EmptyPage:
        articles = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'articles': articles})


def detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    tags = article.tags.all()
    return render(request, 'article_detail.html', {'article': article, 'tags': tags})


@login_required(login_url=reverse_lazy('author:login'))
def edit(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if article.author != request.user and not request.user.is_superuser:
        return HttpResponseForbidden(render_to_response('error.html', {'status_code': 403, 'message': 'Forbidden :('}))
    form = ArticleForm(request.POST or None, instance=article)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse_lazy('article:detail', kwargs={'article_id': form.instance.id}))
    context = {
        'form': form,
        'header_id': 'tag-heading',
        'title': 'Edit Article',
        'subtitle': form.instance.title,
        'background': form.instance.background or get_article_background(),
        'submit': 'update'
    }
    return render(request, 'generic_form.html', context)


@login_required(login_url=reverse_lazy('author:login'))
def new(request):
    form = ArticleForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.instance.author = request.user
        form.save()
        return HttpResponseRedirect(reverse_lazy('article:detail', kwargs={'article_id': form.instance.id}))
    context = {
        'form': form,
        'header_id': 'tag-heading',
        'title': 'New Article',
        'subtitle': 'That looks great!',
        'background': form.instance.background or get_article_background(),
        'submit': 'new'
    }
    return render(request, 'generic_form.html', context)

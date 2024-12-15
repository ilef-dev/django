from django.shortcuts import render, get_object_or_404
from .models import News, Category, Tag
from django.core.paginator import Paginator

def news_list(request):
    category_id = request.GET.get('category')
    tag_ids = request.GET.getlist('tags')
    category = None
    tags = []

    news = News.objects.all().order_by('-created_at')

    if category_id:
        category = get_object_or_404(Category, id=category_id)
        news = news.filter(category=category)

    if tag_ids:
        tags = Tag.objects.filter(id__in=tag_ids)
        news = news.filter(tags__in=tags).distinct()

    paginator = Paginator(news, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    categories = Category.objects.all()
    all_tags = Tag.objects.all()

    return render(request, 'news.html', {
        'page_obj': page_obj,
        'categories': categories,
        'category': category,
        'tags': all_tags,
        'selected_tags': tags,
    })

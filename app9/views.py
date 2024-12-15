from django.core.paginator import Paginator
from django.shortcuts import render
from .models import News

def news_list(request):
    news = News.objects.all().order_by('-created_at')
    paginator = Paginator(news, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news.html', {'page_obj': page_obj})


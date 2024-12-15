from django.contrib import admin
from .models import Category, News, Tag

admin.site.register(News)
admin.site.register(Category)
admin.site.register(Tag)
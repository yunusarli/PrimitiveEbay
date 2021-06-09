from django.contrib import admin
from .models import Listing, Bid, Comment, WatchLists
# Register your models here.

class CommentInline(admin.StackedInline):
    model = Comment

class ArticleInline(admin.ModelAdmin):
    inlines =  [
        CommentInline,
    ]

admin.site.register(Listing,ArticleInline)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(WatchLists)
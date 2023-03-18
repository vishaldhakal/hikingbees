from django.contrib import admin
from .models import Author,Category,Post,Tag,BlogContent

class BlogContentInline(admin.StackedInline):
    model = BlogContent

class PostAdmin(admin.ModelAdmin):
    inlines = [
        BlogContentInline,
    ]

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Post,PostAdmin)

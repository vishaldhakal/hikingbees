from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Author, Category, Post, Tag
from tinymce.widgets import TinyMCE
from django import forms

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
        widgets = {
            'about': TinyMCE(),
        }

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        widgets = {
            'blog_content': TinyMCE(),
        }

class AuthorAdmin(ModelAdmin):
    form = AuthorForm
    list_display = ('name', 'role', 'created_at')
    search_fields = ('name', 'role')

class CategoryAdmin(ModelAdmin):
    list_display = ('category_name',)
    search_fields = ('category_name',)

class TagAdmin(ModelAdmin):
    list_display = ('tag_name',)
    search_fields = ('tag_name',)

class PostAdmin(ModelAdmin):
    form = PostForm
    list_display = ('title', 'category', 'author', 'created_at')
    list_filter = ('category', 'author', 'tags')
    search_fields = ('title', 'meta_title')
    filter_horizontal = ('tags',)
    date_hierarchy = 'created_at'

admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post, PostAdmin)

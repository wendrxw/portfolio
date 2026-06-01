from django.contrib import admin
from django import forms

from .models import Article, Category

try:
    from ckeditor.widgets import CKEditorWidget
except Exception:
    CKEditorWidget = None


class ArticleAdminForm(forms.ModelForm):
    if CKEditorWidget is not None:
        content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Article
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    form = ArticleAdminForm
    list_display = ('title', 'published', 'published_at', 'views')
    list_filter = ('published', 'category')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ('category',)

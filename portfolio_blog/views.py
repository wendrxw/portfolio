from django.db.models import F
from django.views.generic import DetailView, ListView

from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'portfolio_blog/article_list.html'
    context_object_name = 'articles'
    paginate_by = 6

    def get_queryset(self):
        return Article.objects.filter(published=True)


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'portfolio_blog/article_detail.html'
    context_object_name = 'article'

    def get_object(self, queryset=None):
        article = super().get_object(queryset=queryset)
        Article.objects.filter(pk=article.pk).update(views=F('views') + 1)
        article.refresh_from_db()
        return article

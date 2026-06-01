from django.views.generic import TemplateView

from portfolio_blog.models import Article


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_projects'] = [
            {
                'title': 'crawler-verx-serasa',
                'subtitle': 'Python | Selenium | BS4 | Pandas',
                'description': 'Crawler para extração de informações usando Selenium, BeautifulSoup4 e Pandas. Automação completa de processos de web scraping.',
                'url': 'https://github.com/wendrxw/crawler-verx-serasa',
            },
            {
                'title': 'ehr',
                'subtitle': 'Python | HTTP Library',
                'description': 'A HTTP request library like the others. Biblioteca customizada para requisições HTTP em Python, focada em simplicidade e performance.',
                'url': 'https://github.com/wendrxw/ehr',
            },
            {
                'title': 'transfer-simulator',
                'subtitle': 'Haskell | Functional',
                'description': 'Demonstração técnica de lógica de negócios e segurança de tipos utilizando Haskell para simulação de transferências financeiras.',
                'url': 'https://github.com/wendrxw/transfer-simulator',
            },
            {
                'title': 'webssh',
                'subtitle': 'Python | Web SSH',
                'description': 'Cliente SSH baseado em web para acesso remoto a servidores diretamente pelo navegador.',
                'url': 'https://github.com/wendrxw/webssh',
            },
            {
                'title': 'learnyouahaskell_ptbr',
                'subtitle': 'Haskell | Tradução',
                'description': 'Tradução para português brasileiro do tutorial Learn You a Haskell for Great Good!, tornando o aprendizado de Haskell mais acessível.',
                'url': 'https://github.com/wendrxw/learnyouahaskell_ptbr',
            },
        ]
        context['recent_articles'] = Article.objects.filter(published=True).order_by('-published_at')[:3]
        return context

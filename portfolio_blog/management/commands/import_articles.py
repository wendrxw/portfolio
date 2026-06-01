from pathlib import Path
import re
from html import unescape

from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone

from portfolio_blog.models import Article


def strip_tags(html: str) -> str:
    return re.sub(r'<[^>]+>', '', html).strip()


class Command(BaseCommand):
    help = 'Import HTML files from the top-level articles/ directory into the Article model'

    def add_arguments(self, parser):
        parser.add_argument('--dir', help='Path to articles directory (defaults to BASE_DIR / "articles")')
        parser.add_argument('--dry-run', action='store_true', help='Do not write to the database')

    def handle(self, *args, **options):
        articles_dir = Path(options['dir']) if options.get('dir') else Path(settings.BASE_DIR) / 'articles'

        if not articles_dir.exists():
            self.stderr.write(f'Articles directory not found: {articles_dir}')
            return

        html_files = sorted(articles_dir.glob('*.html'))
        if not html_files:
            self.stdout.write('No HTML files found to import.')
            return

        for f in html_files:
            text = f.read_text(encoding='utf-8')

            title_m = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S | re.I)
            title = unescape(strip_tags(title_m.group(1))) if title_m else f.stem.replace('-', ' ').title()

            content_m = re.search(r'<div[^>]*class=["\']article-content["\'][^>]*>(.*?)</div>', text, re.S | re.I)
            if content_m:
                content_html = content_m.group(1).strip()
            else:
                article_m = re.search(r'<article[^>]*>(.*?)</article>', text, re.S | re.I)
                if article_m:
                    content_html = article_m.group(1).strip()
                else:
                    body_m = re.search(r'<body[^>]*>(.*?)</body>', text, re.S | re.I)
                    content_html = body_m.group(1).strip() if body_m else text

            excerpt_m = re.search(r'<p[^>]*>(.*?)</p>', content_html, re.S | re.I)
            excerpt = unescape(strip_tags(excerpt_m.group(0))) if excerpt_m else ''

            slug = slugify(f.stem)

            defaults = {
                'title': title,
                'excerpt': excerpt,
                'content': content_html,
                'published': True,
                'published_at': timezone.now(),
            }

            if options.get('dry_run'):
                self.stdout.write(f'[dry-run] would import {f.name} -> slug: {slug}')
                continue

            obj, created = Article.objects.update_or_create(slug=slug, defaults=defaults)
            self.stdout.write(f"{\"Created\" if created else \"Updated\"}: {obj.title} (slug={obj.slug})")

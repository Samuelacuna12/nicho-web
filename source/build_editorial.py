#!/usr/bin/env python3
"""Render approved editorial records without rebuilding unrelated site pages.

Run after source/build.py when doing a full rebuild. The committed template
retains the production editorial shell. Only articles, Recursos, sitemap and
the page index are written. This script does not research, approve or deploy.
"""
from pathlib import Path
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = 'https://nichoagenciadigital.com'
BRAND = 'Nicho Agencia Digital'
START = '<!-- NICHO_EDITORIAL_CARDS_START -->'
END = '<!-- NICHO_EDITORIAL_CARDS_END -->'


class SafeFragment(HTMLParser):
    tags = {'p', 'ul', 'ol', 'li', 'strong', 'em', 'a', 'code', 'br', 'h3'}

    def handle_starttag(self, tag, attrs):
        assert tag in self.tags, f'Unsupported editorial tag: {tag}'
        for key, value in attrs:
            assert tag == 'a' and key in {'href', 'title'}, f'Unsupported attribute: {key}'
            if key == 'href':
                parsed = urlparse(value)
                assert parsed.scheme in {'', 'https'}, f'Unsafe link: {value}'
                assert not value.startswith('//'), f'Protocol-relative link: {value}'

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)


def text(value):
    return escape(str(value), quote=True)


def render(article, template):
    path = 'recursos/' + article['slug'] + '.html'
    canonical = DOMAIN + '/' + path
    title = article['title'] + ' | ' + BRAND
    sections = []
    toc = []
    for i, section in enumerate(article['sections'], 1):
        SafeFragment().feed(section['html'])
        heading = text(section['heading'])
        toc.append(f'<a href="#apartado-{i}">{heading}</a>')
        sections.append(f'<section id="apartado-{i}"><h2>{heading}</h2>{section["html"]}</section>')
    published = article['datePublished']
    modified = article.get('dateModified', published)
    date_label = article['dateLabel']
    service = article['service']
    assert service in {'sistemas.html', 'agentes-ia.html', 'automatizaciones.html', 'crm-personalizado.html', 'desarrollo-web.html', 'whatsapp-api-empresas.html'}
    sources = ''.join(f'<li><a href="{text(s["url"])}">{text(s["title"])}</a></li>' for s in article['sources'])
    body = (
        '<section class="page-hero article-hero"><div class="wrap">'
        '<nav class="breadcrumbs" aria-label="Ruta de navegación"><a href="/">Inicio</a><span>/</span>'
        '<a href="../recursos.html">Ideas y recursos</a><span>/</span><span>Guía práctica</span></nav>'
        f'<span class="case-status">{text(article["category"])}</span><h1>{text(article["title"])}</h1>'
        f'<p class="lead">{text(article["intro"])}</p></div></section>'
        '<section class="section"><div class="wrap article-layout">'
        '<nav class="article-toc" aria-label="Contenido de la guía"><span class="eyebrow">EN ESTA GUÍA</span>'
        + ''.join(toc) + '<a href="#siguiente-paso">El siguiente paso</a><a href="#fuentes">Fuentes y alcance</a></nav>'
        f'<article class="article-body"><p class="small">Por {BRAND} · Publicado el <time datetime="{text(published)}">{text(date_label)}</time></p>'
        + ''.join(sections)
        + f'<section id="siguiente-paso"><h2>El siguiente paso</h2><p>{text(article["cta"])}</p>'
        f'<p><a href="../{service}">Explorar la solución de Nicho</a> · <a href="../contacto.html">Conversar sobre tu proyecto ↗</a></p></section>'
        f'<section id="fuentes"><h2>Fuentes y alcance</h2><ul>{sources}</ul>'
        f'<p class="small">Fuentes consultadas el {text(article["sourceDateLabel"])}. Las recomendaciones de proceso son propuestas editoriales de Nicho; los ejemplos identificados como hipotéticos no representan resultados de clientes.</p>'
        '<p class="small">Contenido preparado con asistencia de IA y comprobaciones automáticas. No sustituye una evaluación de tu implementación ni garantiza resultados. '
        '<a href="mailto:nicho.agenciadigital@gmail.com">Escríbenos si encuentras algo que debamos corregir</a>.</p></section></article></div></section>'
    )
    graph = [
        {'@type': 'WebPage', '@id': canonical + '#webpage', 'url': canonical, 'name': title,
         'description': article['description'], 'inLanguage': 'es-CO',
         'isPartOf': {'@id': DOMAIN + '/#website'}, 'breadcrumb': {'@id': canonical + '#breadcrumbs'}},
        {'@type': 'BreadcrumbList', '@id': canonical + '#breadcrumbs', 'itemListElement': [
            {'@type': 'ListItem', 'position': 1, 'name': 'Inicio', 'item': DOMAIN + '/'},
            {'@type': 'ListItem', 'position': 2, 'name': 'Ideas y recursos', 'item': DOMAIN + '/recursos.html'},
            {'@type': 'ListItem', 'position': 3, 'name': article['title'], 'item': canonical}]},
        {'@type': 'Article', 'headline': article['title'], 'description': article['description'],
         'image': DOMAIN + '/assets/media/og-nicho.jpg', 'mainEntityOfPage': {'@id': canonical + '#webpage'},
         'author': {'@type': 'Organization', 'name': BRAND, 'url': DOMAIN + '/nosotros.html'},
         'publisher': {'@type': 'Organization', 'name': BRAND, 'url': DOMAIN + '/'},
         'datePublished': published, 'dateModified': modified, 'inLanguage': 'es-CO',
         'articleSection': article['category']}
    ]
    replacements = {
        '__EDITORIAL_TITLE__': text(title), '__EDITORIAL_DESCRIPTION__': text(article['description']),
        '__EDITORIAL_CANONICAL__': canonical, '__EDITORIAL_BODY__': body,
        '__EDITORIAL_SCHEMA__': json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False, separators=(',', ':')).replace('<', '\\u003c')}
    output = template
    for key, value in replacements.items():
        output = output.replace(key, value)
    assert '__EDITORIAL_' not in output
    return path, title, output


def apply(site=ROOT):
    site = Path(site)
    articles = json.loads((ROOT / 'source/editorial-articles.json').read_text())
    template = (ROOT / 'source/editorial-template.html.tmpl').read_text()
    slugs = [a['slug'] for a in articles]
    assert len(slugs) == len(set(slugs)), 'Duplicate editorial slug'
    assert all(re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*', s) for s in slugs)
    cards = []
    page_index_path = ROOT / 'source/page-index.json'
    page_index = json.loads(page_index_path.read_text())
    sitemap_path = site / 'sitemap.xml'
    sitemap = sitemap_path.read_text()
    existing_urls = {e.text for e in ET.fromstring(sitemap).findall('{*}url/{*}loc')}
    for article in articles:
        path, title, output = render(article, template)
        target = site / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(output, encoding='utf-8')
        page_index[path] = {'title': title, 'description': article['description'], 'kind': 'Article'}
        canonical = DOMAIN + '/' + path
        if canonical not in existing_urls:
            entry = f'  <url><loc>{canonical}</loc><lastmod>{article.get("dateModified", article["datePublished"])}</lastmod></url>\n'
            sitemap = sitemap.replace('</urlset>', entry + '</urlset>')
        else:
            pattern = r'(<url>\s*<loc>' + re.escape(canonical) + r'</loc>\s*<lastmod>)[^<]+(</lastmod>)'
            sitemap = re.sub(pattern, lambda m: m[1] + article.get('dateModified', article['datePublished']) + m[2], sitemap)
        cards.append(f'<article class="article-card"><span class="eyebrow">{text(article["category"])}</span><h3><a href="{path}">{text(article["title"])}</a></h3><p>{text(article["description"])}</p><a class="text-link" href="{path}">Leer guía ↗</a></article>')
    index_path = site / 'recursos.html'
    index = index_path.read_text()
    index = re.sub(re.escape(START) + '.*?' + re.escape(END), '', index, flags=re.S)
    anchor = '<div class="wrap articles-grid">'
    assert index.count(anchor) == 1, 'Resources grid changed: review before rebuilding'
    index = index.replace(anchor, anchor + START + ''.join(cards) + END)
    index_path.write_text(index, encoding='utf-8')
    sitemap_path.write_text(sitemap, encoding='utf-8')
    page_index_path.write_text(json.dumps(page_index, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Rendered {len(articles)} editorial pages; retained existing resources and sitemap entries.')


if __name__ == '__main__':
    apply()

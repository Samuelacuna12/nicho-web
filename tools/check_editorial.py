#!/usr/bin/env python3
"""Validate approved editorial records and their generated public pages."""
from pathlib import Path
from html.parser import HTMLParser
from datetime import date, datetime
from zoneinfo import ZoneInfo
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
import collections
import json
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parents[1])
articles = json.loads((root/'source/editorial-articles.json').read_text())
errors = []


class Document(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]; self.headings=[]; self.text=[]
    def handle_starttag(self, tag, attrs):
        attrs=dict(attrs)
        if tag=='a': self.links.append(attrs.get('href',''))
        if tag in ['h1','h2','h3']: self.headings.append(tag)
    def handle_data(self, data):
        self.text.append(data)


for field in ['slug','title','description']:
    duplicates=[x for x,n in collections.Counter(a[field] for a in articles).items() if n>1]
    if duplicates: errors.append({'field':field,'duplicates':duplicates})
index=(root/'recursos.html').read_text()
sitemap={e.text for e in ET.parse(root/'sitemap.xml').getroot().findall('{*}url/{*}loc')}
wordcounts={}
for a in articles:
    path='recursos/'+a['slug']+'.html'; canonical='https://nichoagenciadigital.com/'+path
    html=(root/path).read_text(); doc=Document();doc.feed(html)
    if not 50<=len(a['description'])<=180: errors.append({'slug':a['slug'],'error':'description_length'})
    if doc.headings.count('h1')!=1: errors.append({'slug':a['slug'],'error':'h1_count'})
    if canonical not in sitemap or path not in index: errors.append({'slug':a['slug'],'error':'undiscoverable'})
    if '__EDITORIAL_' in html: errors.append({'slug':a['slug'],'error':'placeholder'})
    if 'asistencia de IA y comprobaciones automáticas' not in html: errors.append({'slug':a['slug'],'error':'missing_disclosure'})
    if 'intent' in a: errors.append({'slug':a['slug'],'error':'private_editorial_intent_in_public_record'})
    if not a['sources']: errors.append({'slug':a['slug'],'error':'missing_sources'})
    for s in a['sources']:
        if urlparse(s['url']).scheme!='https' or s['url'] not in doc.links:
            errors.append({'slug':a['slug'],'error':'source_link','url':s['url']})
    ld=re.search(r'<script type="application/ld\+json">(.*?)</script>',html,re.S)
    graph=json.loads(ld.group(1))['@graph']
    schema=next(x for x in graph if x['@type']=='Article')
    for k in ['headline','description','datePublished']:
        expected=a['title'] if k=='headline' else a[k]
        if schema[k]!=expected: errors.append({'slug':a['slug'],'error':'schema_mismatch','field':k})
    if date.fromisoformat(a['datePublished'][:10]) > datetime.now(ZoneInfo('America/Bogota')).date():
        errors.append({'slug':a['slug'],'error':'future_publication_date'})
    words=Document();words.feed(a['intro']+' '+''.join(s['html'] for s in a['sections']))
    wordcounts[a['slug']]=len(' '.join(words.text).split())
print(json.dumps({'articles':len(articles),'errors':errors,'words':wordcounts},ensure_ascii=False,indent=2))
sys.exit(bool(errors))

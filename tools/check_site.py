#!/usr/bin/env python3
"""Static site QA using only Python's standard library.
Checks local paths, HTML anchors, headings, JSON-LD, canonicals, sitemap and font leakage.
This does NOT measure Google rankings, Core Web Vitals, TLS or the rendered visual result.
"""
import argparse, collections, gzip, json, re, sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse, unquote
from xml.etree import ElementTree as ET

DOMAIN = 'https://nichoagenciadigital.com'
# Existing customer training URLs must survive website rebuilds and migrations.
PRIVATE_PAGES = {'curso-basico-de-como-integrar-tu-api/index.html'}
REQUIRED_LEGACY_FILES = PRIVATE_PAGES | {'wp-content/uploads/2026/09/GUIA-WHATSAPP-API-.pdf'}

def page_url(path):
    return DOMAIN + '/' + (path[:-10] if path.endswith('index.html') else path)

class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.h1=0; self.title=''; self.in_title=False; self.main=0; self.ids=[]
        self.meta={}; self.links=[]; self.refs=[]; self.images=[]; self.json=[]; self.in_ld=False; self.ld=''
    def handle_starttag(self, tag, attributes):
        a=dict(attributes)
        if a.get('id'): self.ids.append(a['id'])
        if tag=='h1': self.h1+=1
        if tag=='main': self.main+=1
        if tag=='title': self.in_title=True
        if tag=='meta': self.meta[a.get('name') or a.get('property')]=a.get('content','')
        if tag=='link': self.links.append(a)
        if tag=='img': self.images.append(a)
        if tag=='script' and a.get('type')=='application/ld+json': self.in_ld=True; self.ld=''
        for name in ('href','src','poster','data-src'):
            if a.get(name): self.refs.append((tag,name,a[name]))
    def handle_endtag(self, tag):
        if tag=='title': self.in_title=False
        if tag=='script' and self.in_ld:
            self.json.append(self.ld); self.in_ld=False
    def handle_data(self, data):
        if self.in_title: self.title+=data
        if self.in_ld: self.ld+=data


def audit(root):
    root=root.resolve(); errors=[]; warnings=[]; parsed={}; rows=[]
    for legacy_path in sorted(REQUIRED_LEGACY_FILES):
        if not (root / legacy_path).is_file():
            errors.append({'page':legacy_path, 'code':'missing_legacy_resource'})
    html_paths=sorted(p for p in root.rglob('*.html') if '.git' not in p.parts and 'qa' not in p.parts)
    for path in html_paths:
        parser=Page(); parser.feed(path.read_text(encoding='utf-8')); parsed[path]=parser
    def issue(path,code,detail): errors.append({'page':str(path.relative_to(root)), 'code':code, 'detail':detail})
    for path,p in parsed.items():
        rel=path.relative_to(root).as_posix(); is404=rel=='404.html'; is_private=rel in PRIVATE_PAGES
        if p.h1!=1: issue(path,'h1_count',p.h1)
        if p.main!=1: issue(path,'main_count',p.main)
        if not p.title.strip(): issue(path,'missing_title','')
        if not p.meta.get('description'): issue(path,'missing_description','')
        duplicate_ids=[k for k,n in collections.Counter(p.ids).items() if n>1]
        if duplicate_ids: issue(path,'duplicate_ids',duplicate_ids)
        canonical=[x.get('href') for x in p.links if x.get('rel')=='canonical']
        expected=page_url(rel)
        if not is404 and canonical!=[expected]: issue(path,'canonical',{'found':canonical,'expected':expected})
        if not is404 and not is_private and 'noindex' in p.meta.get('robots',''): issue(path,'production_noindex','')
        if is_private and 'noindex' not in p.meta.get('robots',''): issue(path,'private_page_indexable','')
        if is404 and 'noindex' not in p.meta.get('robots',''): issue(path,'404_indexable','')
        if not is404 and not is_private and not p.json: issue(path,'missing_schema','')
        for blob in p.json:
            try:
                schema=json.loads(blob)
                if schema.get('@context')!='https://schema.org': issue(path,'schema_context','')
                for n in schema.get('@graph',[]):
                    if n.get('@type') in ('Review','AggregateRating'): issue(path,'unverified_review_markup',n.get('@type'))
            except Exception as exc: issue(path,'invalid_jsonld',str(exc))
        for img in p.images:
            if 'alt' not in img: issue(path,'image_without_alt',img.get('src'))
            if 'width' not in img or 'height' not in img: warnings.append({'page':rel,'code':'image_dimensions','src':img.get('src')})
        for tag,attr,raw in p.refs:
            u=urlparse(raw)
            if u.scheme in ('mailto','tel','data','javascript','blob'): continue
            if u.scheme in ('http','https'):
                if u.scheme=='http': issue(path,'insecure_url',raw)
                if u.netloc!='nichoagenciadigital.com': continue
                target=root/unquote(u.path.lstrip('/'))
            elif u.netloc: continue
            elif u.path.startswith('/'): target=root/unquote(u.path.lstrip('/'))
            elif not u.path: target=path
            else: target=(path.parent/unquote(u.path)).resolve()
            if target.is_dir(): target=target/'index.html'
            if not target.is_relative_to(root): issue(path,'path_outside_site',raw); continue
            if not target.exists(): issue(path,'missing_asset_or_page',raw); continue
            if u.fragment and target in parsed and unquote(u.fragment) not in parsed[target].ids:
                issue(path,'missing_anchor',raw)
        rows.append({'page':rel,'title':p.title,'title_length':len(p.title),'description_length':len(p.meta.get('description','')),'canonical':canonical[0] if canonical else None,'stylesheets':len([l for l in p.links if l.get('rel')=='stylesheet']),'h1':p.h1,'jsonld_blocks':len(p.json),'html_bytes':path.stat().st_size})
    for field in ('title',):
        values=collections.defaultdict(list)
        for r in rows: values[r[field]].append(r['page'])
        for v,ps in values.items():
            if len(ps)>1: errors.append({'code':'duplicate_'+field,'pages':ps,'value':v})
    desc=collections.defaultdict(list)
    for path,p in parsed.items(): desc[p.meta.get('description')].append(str(path.relative_to(root)))
    for v,ps in desc.items():
        if len(ps)>1: errors.append({'code':'duplicate_description','pages':ps})
    try:
        urls=[e.text for e in ET.parse(root/'sitemap.xml').getroot().findall('{*}url/{*}loc')]
        expected={page_url(r['page']) for r in rows if r['page']!='404.html' and r['page'] not in PRIVATE_PAGES}
        if set(urls)!=expected: errors.append({'code':'sitemap_mismatch','missing':sorted(expected-set(urls)),'extra':sorted(set(urls)-expected)})
        if len(urls)!=len(set(urls)): errors.append({'code':'sitemap_duplicates'})
    except Exception as exc: errors.append({'code':'sitemap_invalid','detail':str(exc)});urls=[]
    for path in root.rglob('*'):
        if path.suffix.lower() in ('.ttf','.otf','.woff','.woff2'):
            errors.append({'code':'font_file_in_release','path':str(path.relative_to(root))})
    if (root/'CNAME').read_text().strip()!='nichoagenciadigital.com': errors.append({'code':'cname_changed'})
    if 'Sitemap: '+DOMAIN+'/sitemap.xml' not in (root/'robots.txt').read_text(): errors.append({'code':'robots_sitemap_missing'})
    files=[p for p in root.rglob('*') if p.is_file() and '.git' not in p.parts and 'qa' not in p.parts]
    media=[{'path':str(p.relative_to(root)),'bytes':p.stat().st_size} for p in files if p.suffix in ('.mp4','.webp','.jpg','.svg','.png')]
    return {'method':'Static source and file validation; not a Google rating or live network audit.','summary':{'html_pages':len(rows),'indexable_pages':len(urls),'errors':len(errors),'warnings':len(warnings),'files':len(files),'source_bytes':sum(p.stat().st_size for p in files)},'errors':errors,'warnings':warnings,'pages':rows,'media':media}

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('site',type=Path,nargs='?',default=Path(__file__).resolve().parents[1]);ap.add_argument('--json',type=Path)
    args=ap.parse_args();result=audit(args.site)
    if args.json: args.json.parent.mkdir(parents=True,exist_ok=True);args.json.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result['summary'],ensure_ascii=False,indent=2))
    if result['errors']: print(json.dumps(result['errors'],ensure_ascii=False,indent=2))
    sys.exit(1 if result['errors'] else 0)

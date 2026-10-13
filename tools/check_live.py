#!/usr/bin/env python3
"""Verify the actual HTTPS deployment against the checked-out release bytes.
Does not modify DNS, Pages settings or third-party accounts.
"""
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = 'https://nichoagenciadigital.com'
REVISION = os.environ.get('GITHUB_SHA', 'studio-04')


def check(path):
    public_path = '/' if path == 'index.html' else '/' + path
    url = DOMAIN + public_path + ''
    expected = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
    request = urllib.request.Request(url, headers={
        'User-Agent': 'NICHO-Deployment-Verification/1.0',
        'Accept-Encoding': 'identity',
        'Cache-Control': 'no-cache',
    })
    try:
        with urllib.request.urlopen(request, timeout=25) as response:
            data = response.read(6000000)
            final = urllib.parse.urlparse(response.url)
            if final.scheme != 'https' or final.hostname != 'nichoagenciadigital.com':
                raise RuntimeError('Redireccion inesperada: ' + response.url)
            actual = hashlib.sha256(data).hexdigest()
            if actual != expected:
                raise RuntimeError('Contenido publicado distinto de la entrega: ' + path)
            return {'path': public_path, 'status': response.status, 'bytes': len(data),
                    'sha256_match': True, 'https_verified': True}
    except Exception as exc:
        return {'path': public_path, 'error': str(exc), 'https_verified': False}


def main():
    # Wait for GitHub Pages/CDN to publish this revision, without disabling TLS checks.
    deadline = time.monotonic() + 240
    while True:
        # Editorial-only releases do not change the homepage. Wait for the
        # release manifest as well, otherwise new articles can be checked
        # before Pages has deployed them and incorrectly reported as 404.
        release_checks = [check('index.html'), check('sitemap.xml')]
        pending = [result for result in release_checks if 'error' in result]
        if not pending:
            break
        print('Esperando publicacion:', json.dumps(pending), flush=True)
        if time.monotonic() >= deadline:
            raise SystemExit('No se pudo confirmar portada y sitemap de la entrega por HTTPS')
        time.sleep(12)
    locs = [x.text for x in ET.parse(ROOT / 'sitemap.xml').getroot().findall('{*}url/{*}loc')]
    paths = [urllib.parse.urlparse(url).path.lstrip('/') or 'index.html' for url in locs]
    paths += ['assets/css/editorial-shell.css', 'assets/js/editorial-shell.js']
    paths += [str(p.relative_to(ROOT)) for p in (ROOT/'assets/media/projects').glob('*.webp')]
    paths += ['assets/css/main.css', 'assets/js/app.js', 'assets/js/wordmark.js',
              'assets/js/wordmark-data.js', 'assets/js/config.js',
              'assets/media/nicho-wordmark-motion.mp4', 'assets/media/nicho-wordmark-poster.webp',
              'assets/media/liquid-studio.mp4', 'assets/media/liquid-studio.webp',
              'assets/media/og-nicho.jpg', 'assets/media/architecture.webp',
              'assets/media/workspace.webp', 'assets/vendor/gsap.min.js',
              'assets/vendor/ScrollTrigger.min.js', 'favicon.ico', 'favicon.svg',
              'apple-touch-icon.png', 'icon-512.png', 'site.webmanifest', 'sitemap.xml', 'robots.txt']
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as executor:
        results = list(executor.map(check, sorted(set(paths))))
    errors = [result for result in results if 'error' in result]
    report = {'revision': REVISION, 'domain': DOMAIN, 'checks': len(results),
              'errors': len(errors), 'results': results}
    output = ROOT / 'qa' / 'live-report.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2), flush=True)
    if errors:
        raise SystemExit(1)
    print('PUBLICACION HTTPS VERIFICADA: archivos y paginas coinciden con la nueva entrega.')


if __name__ == '__main__':
    main()

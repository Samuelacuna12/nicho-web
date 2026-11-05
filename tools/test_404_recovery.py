"""Keep 404 recovery links useful even when served at nested missing URLs."""
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOMAIN = 'https://nichoagenciadigital.com'


class RecoveryLinks(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.links.append(dict(attrs)['href'])


class ErrorPageRecovery(unittest.TestCase):
    def setUp(self):
        self.html = (ROOT / '404.html').read_text()
        self.copy = re.search(r'<section class="page404">.*?<p>(.*?)</p>', self.html, re.S).group(1)

    def test_contextual_recovery_links_use_absolute_existing_destinations(self):
        links = RecoveryLinks(self.copy).links
        self.assertEqual(links, [DOMAIN + '/soluciones.html', DOMAIN + '/recursos.html'])
        for link in links:
            self.assertTrue((ROOT / link.removeprefix(DOMAIN + '/')).is_file())

    def test_remains_nonindexable_and_outside_sitemap(self):
        self.assertIn('<meta content="noindex,follow" name="robots"/>', self.html)
        self.assertNotIn('rel="canonical"', self.html)
        self.assertNotIn('/404.html', (ROOT / 'sitemap.xml').read_text())

    def test_generator_preserves_recovery_copy(self):
        self.assertIn(self.copy, (ROOT / 'source/build.py').read_text())


if __name__ == '__main__':
    unittest.main()

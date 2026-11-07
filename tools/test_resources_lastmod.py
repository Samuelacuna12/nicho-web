"""Regressions for truthful sitemap freshness on the resources hub."""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('editorial', ROOT / 'source/build_editorial.py')
editorial = importlib.util.module_from_spec(spec)
spec.loader.exec_module(editorial)


class ResourcesLastmod(unittest.TestCase):
    def sitemap(self, date):
        return ('<urlset><url><loc>https://nichoagenciadigital.com/recursos.html</loc>'
                f'<lastmod>{date}</lastmod></url><url><loc>https://nichoagenciadigital.com/</loc>'
                '<lastmod>2026-10-11</lastmod></url></urlset>')

    def test_uses_latest_publication_or_modification(self):
        articles = [{'datePublished': '2026-10-20', 'dateModified': '2026-11-04'},
                    {'datePublished': '2026-11-02'}]
        self.assertEqual(editorial.update_resources_lastmod(self.sitemap('2026-10-11'), articles),
                         self.sitemap('2026-11-04'))

    def test_preserves_newer_existing_hub_date(self):
        source = self.sitemap('2026-11-06')
        self.assertEqual(editorial.update_resources_lastmod(source, [{'datePublished': '2026-11-04'}]), source)

    def test_empty_editorial_collection_leaves_sitemap_unchanged(self):
        source = self.sitemap('2026-10-11')
        self.assertEqual(editorial.update_resources_lastmod(source, []), source)

    def test_missing_hub_entry_requires_review(self):
        with self.assertRaises(AssertionError):
            editorial.update_resources_lastmod('<urlset/>', [{'datePublished': '2026-11-04'}])

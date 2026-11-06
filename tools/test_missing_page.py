"""Offline checks for real HTTP 404 responses, never successful soft 404s."""
import io
from pathlib import Path
import tempfile
import unittest
import urllib.error
from unittest.mock import patch
from test_check_live import live


class Response(io.BytesIO):
    def __init__(self, data, status, url):
        super().__init__(data)
        self.status = status
        self.url = url

    def geturl(self):
        return self.url


class MissingPageTests(unittest.TestCase):
    path = '/recursos/__nicho_missing_page_probe__.html'
    body = b'<html><meta name="robots" content="noindex,follow">Not found</html>'

    def run_check(self, status=404, body=None, redirect=False, network_error=False):
        url = live.DOMAIN + self.path
        response = Response(self.body if body is None else body, status,
                            live.DOMAIN + '/404.html' if redirect else url)
        if network_error:
            effect = urllib.error.URLError('connection failed')
        elif status == 404:
            effect = urllib.error.HTTPError(response.url, 404, 'Not found', {}, response)
        else:
            effect = None
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / '404.html').write_bytes(self.body)
            with patch.object(live, 'ROOT', root), patch.object(
                live.urllib.request, 'urlopen', return_value=response, side_effect=effect
            ):
                return live.check_missing_page(self.path)

    def test_actual_404_with_expected_body_passes(self):
        result = self.run_check()
        self.assertEqual(result['status'], 404)
        self.assertTrue(result['missing_page_verified'])

    def test_soft_404_with_200_status_fails(self):
        self.assertIn('error', self.run_check(status=200))

    def test_server_error_fails(self):
        self.assertIn('error', self.run_check(status=503))

    def test_generic_or_stale_404_body_fails(self):
        self.assertIn('error', self.run_check(body=b'Generic error'))

    def test_redirected_404_fails(self):
        self.assertIn('error', self.run_check(redirect=True))

    def test_network_error_fails(self):
        self.assertIn('error', self.run_check(network_error=True))

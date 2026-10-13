#!/usr/bin/env python3
"""Offline regression tests for the deployment-readiness gate."""
import contextlib
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('check_live', Path(__file__).with_name('check_live.py'))
live = importlib.util.module_from_spec(spec)
spec.loader.exec_module(live)


class DeploymentGateTests(unittest.TestCase):
    def test_unchanged_home_does_not_skip_pending_sitemap(self):
        calls = []
        sitemap_reads = 0

        def fake_check(path):
            nonlocal sitemap_reads
            calls.append(path)
            if path == 'sitemap.xml':
                sitemap_reads += 1
                if sitemap_reads == 1:
                    return {'path': path, 'error': 'previous release'}
            return {'path': path, 'status': 200, 'sha256_match': True}

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'sitemap.xml').write_text(
                '<urlset><url><loc>https://nichoagenciadigital.com/recursos/new.html</loc></url></urlset>'
            )
            with patch.object(live, 'ROOT', root), patch.object(live, 'check', side_effect=fake_check), \
                 patch.object(live.time, 'sleep') as sleep, contextlib.redirect_stdout(io.StringIO()):
                live.main()
            self.assertEqual(calls[:4], ['index.html', 'sitemap.xml', 'index.html', 'sitemap.xml'])
            sleep.assert_called_once_with(12)
            self.assertIn('recursos/new.html', calls[4:])
            self.assertTrue((root / 'qa/live-report.json').exists())

    def test_pending_release_times_out_without_passing(self):
        def fake_check(path):
            return {'path': path, **({'error': 'stale'} if path == 'sitemap.xml' else {'status': 200})}

        with patch.object(live, 'check', side_effect=fake_check), \
             patch.object(live.time, 'monotonic', side_effect=[0, 241]), \
             patch.object(live.time, 'sleep') as sleep, contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(SystemExit):
                live.main()
            sleep.assert_not_called()


if __name__ == '__main__':
    unittest.main()

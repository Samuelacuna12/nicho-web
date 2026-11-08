"""Prevent accidental Google exclusions from bypassing static publication QA."""
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('check_site', Path(__file__).with_name('check_site.py'))
site = importlib.util.module_from_spec(spec)
spec.loader.exec_module(site)


class SearchRobotsTests(unittest.TestCase):
    def excluded(self, html):
        page = site.Page()
        page.feed(html)
        return site.has_noindex(page.search_robots)

    def test_regular_indexable_directives_pass(self):
        self.assertFalse(self.excluded('<meta name="robots" content="index,follow,max-image-preview:large">'))

    def test_case_insensitive_googlebot_noindex_is_detected(self):
        self.assertTrue(self.excluded('<meta name="Googlebot" content="NOINDEX, FOLLOW">'))

    def test_none_is_an_indexing_exclusion(self):
        self.assertTrue(self.excluded('<meta name="ROBOTS" content="none">'))

    def test_restrictive_duplicate_is_not_overwritten(self):
        self.assertTrue(self.excluded('<meta name="robots" content="noindex"><meta name="robots" content="index">'))

    def test_googlebot_restriction_is_not_overridden_by_generic_index(self):
        self.assertTrue(self.excluded('<meta name="googlebot" content="none"><meta name="robots" content="index,follow">'))

    def test_unrelated_metadata_and_nofollow_do_not_mark_noindex(self):
        self.assertFalse(self.excluded('<meta name="description" content="noindex"><meta name="robots" content="nofollow">'))

    def test_tokens_are_exact(self):
        self.assertFalse(site.has_noindex(['not-noindex, noindex-example']))

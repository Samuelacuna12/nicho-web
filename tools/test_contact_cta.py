"""Regression checks for the bounded home/contact consultation CTA change."""
from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
AGENDA = 'https://calendar.app.google/DAYcFPswU2gASF418'
LABEL = 'Agenda una asesoría gratuita de 30 minutos'


class Links(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = []
        self.current = None
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            self.current = dict(attrs)
            self.current['text'] = ''

    def handle_data(self, data):
        if self.current is not None:
            self.current['text'] += data

    def handle_endtag(self, tag):
        if tag == 'a' and self.current is not None:
            self.links.append(self.current)
            self.current = None


class ConsultationCTA(unittest.TestCase):
    def links(self, page):
        return Links((ROOT / page).read_text()).links

    def test_primary_home_action_precedes_existing_portfolio(self):
        links = self.links('index.html')
        primary = next(a for a in links if 'n-consultation' in a.get('class', '').split())
        secondary = next(a for a in links if 'n-projects-secondary' in a.get('class', '').split())
        self.assertEqual(primary['href'], AGENDA)
        self.assertIn(LABEL, primary['text'])
        self.assertEqual(secondary['href'], '/portafolio.html')
        self.assertIn('Explorar proyectos', secondary['text'])
        self.assertLess(links.index(primary), links.index(secondary))

    def test_agenda_copy_and_safe_external_links_on_both_pages(self):
        for page, expected in [('index.html', 2), ('contacto.html', 3)]:
            links = [a for a in self.links(page) if a.get('href') == AGENDA]
            self.assertEqual(len(links), expected, page)
            for a in links:
                self.assertIn(LABEL, a['text'])
                self.assertEqual(a.get('target'), '_blank')
                self.assertTrue({'noopener', 'noreferrer'} <= set(a.get('rel', '').split()))

    def test_contact_retains_direct_channels_and_honest_brief(self):
        html = (ROOT / 'contacto.html').read_text()
        self.assertIn('n-contact-consultation', html)
        self.assertIn('https://wa.me/573028289997', html)
        self.assertIn('mailto:nicho.agenciadigital@gmail.com', html)
        self.assertIn('No se envía ni se guarda esta información en un servidor', html)
        self.assertIn('Preparar mi mensaje', html)


if __name__ == '__main__':
    unittest.main()

from unittest import TestCase
from django.conf import settings
import ujson

settings.configure()

from drf_ujson.renderers import UJSONRenderer


class UJSONRendererTests(TestCase):
    def setUp(self):
        self.renderer = UJSONRenderer()
        self.data = {
            'a': [1, 2, 3],
            'b': True,
            'c': 1.23,
            'd': 'test',
            'e': {'foo': 'bar'},
        }

    def test_basic_data_structures_rendered_correctly(self):

        rendered = self.renderer.render(self.data)
        reloaded = ujson.loads(rendered)

        self.assertEqual(reloaded, self.data)

    def test_renderer_works_correctly_when_media_type_and_context_provided(self):

        rendered = self.renderer.render(
            data=self.data,
            media_type='application/json',
            renderer_context={},
        )
        reloaded = ujson.loads(rendered)

        self.assertEqual(reloaded, self.data)

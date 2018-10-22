from __future__ import unicode_literals

import codecs

from django.conf import settings
from rest_framework.compat import six
from rest_framework.parsers import BaseParser, ParseError
from rest_framework import renderers
from rest_framework.settings import api_settings
import ujson


class UJSONParser(BaseParser):
    """
    Parses JSON-serialized data.
    """
    media_type = 'application/json'
    renderer_class = renderers.JSONRenderer
    strict = api_settings.STRICT_JSON

    def parse(self, stream, media_type=None, parser_context=None):
        """
        Parses the incoming bytestream as JSON and returns the resulting data.
        """
        parser_context = parser_context or {}
        encoding = parser_context.get('encoding', settings.DEFAULT_CHARSET)

        try:
            decoded_stream = codecs.getreader(encoding)(stream)
            parse_constant = ujson.strict_constant if self.strict else None
            return ujson.load(decoded_stream, parse_constant=parse_constant)
        except ValueError as exc:
            raise ParseError('JSON parse error - %s' % six.text_type(exc))

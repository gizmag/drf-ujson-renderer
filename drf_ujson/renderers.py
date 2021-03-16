from __future__ import unicode_literals
from rest_framework.renderers import BaseRenderer
import ujson


class UJSONRenderer(BaseRenderer):
    """
    Renderer which serializes to JSON.
    Applies JSON's backslash-u character escaping for non-ascii characters.
    Uses the blazing-fast ujson library for serialization.
    """

    media_type = 'application/json'
    format = 'json'
    ensure_ascii = True
    charset = None

    def render(self, data, *args, **kwargs):

        if data is None:
            return bytes()

        ret = ujson.dumps(data, ensure_ascii=self.ensure_ascii)
        if isinstance(ret, str):
            return bytes(ret.encode('utf-8'))
        return ret

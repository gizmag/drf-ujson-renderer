from __future__ import unicode_literals
from rest_framework.compat import six
from rest_framework.renderers import JSONRenderer
import ujson


class UJSONRenderer(JSONRenderer):
    """
    Renderer which serializes to JSON.
    Applies JSON's backslash-u character escaping for non-ascii characters.
    Uses the blazing-fast ujson library for serialization.
    """

    # Controls how many decimals to encode for double or decimal values.
    double_precision = 9
    # Controls whether forward slashes (/) are escaped.
    escape_forward_slashes = False
    # Used to enable special encoding of "unsafe" HTML characters into safer
    # Unicode sequences.
    encode_html_chars = False

    def render(self, data, accepted_media_type=None, renderer_context=None):
        if data is None:
            return bytes()

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        ret = ujson.dumps(
            data,
            ensure_ascii=self.ensure_ascii,
            escape_forward_slashes=self.escape_forward_slashes,
            encode_html_chars=self.encode_html_chars,
            double_precision=self.double_precision,
            indent=indent or 0,
        )

        # force return value to unicode
        if isinstance(ret, six.text_type):
            # We always fully escape \u2028 and \u2029 to ensure we output JSON
            # that is a strict javascript subset. If bytes were returned
            # by json.dumps() then we don't have these characters in any case.
            # See: http://timelessrepo.com/json-isnt-a-javascript-subset
            ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
            return bytes(ret.encode('utf-8'))
        return ret

from __future__ import unicode_literals
from rest_framework.compat import six
from rest_framework.renderers import BaseRenderer
import ujson
from django.http.multipartparser import parse_header
from rest_framework.settings import api_settings


def zero_as_none(value):
    return None if value == 0 else value


# class UJSONRenderer(BaseRenderer):
#     """
#     Renderer which serializes to JSON.
#     Applies JSON's backslash-u character escaping for non-ascii characters.
#     Uses the blazing-fast ujson library for serialization.
#     """
#
#     media_type = 'application/json'
#     format = 'json'
#     ensure_ascii = True
#     charset = None
#
#     def get_indent(self, accepted_media_type, renderer_context):
#         if accepted_media_type:
#             # If the media type looks like 'application/json; indent=4',
#             # then pretty print the result.
#             # Note that we coerce `indent=0` into `indent=None`.
#             base_media_type, params = parse_header(accepted_media_type.encode('ascii'))
#             try:
#                 return zero_as_none(max(min(int(params['indent']), 8), 0))
#             except (KeyError, ValueError, TypeError):
#                 pass
#
#         # If 'indent' is provided in the context, then pretty print the result.
#         # E.g. If we're being called by the BrowsableAPIRenderer.
#         return renderer_context.get('indent', None)
#
#     def render(self, data, *args, **kwargs):
#
#         if data is None:
#             return bytes()
#
#         ret = ujson.dumps(data, ensure_ascii=self.ensure_ascii)
#
#         # force return value to unicode
#         if isinstance(ret, six.text_type):
#             return bytes(ret.encode('utf-8'))
#         return ret


class UJSONRenderer(BaseRenderer):
    """
    Renderer which serializes to JSON.
    """
    media_type = 'application/json'
    format = 'json'
    ensure_ascii = not api_settings.UNICODE_JSON
    compact = api_settings.COMPACT_JSON
    strict = api_settings.STRICT_JSON

    # We don't set a charset because JSON is a binary encoding,
    # that can be encoded as utf-8, utf-16 or utf-32.
    # See: https://www.ietf.org/rfc/rfc4627.txt
    # Also: http://lucumr.pocoo.org/2013/7/19/application-mimetypes-and-encodings/
    charset = None

    def get_indent(self, accepted_media_type, renderer_context):
        if accepted_media_type:
            # If the media type looks like 'application/json; indent=4',
            # then pretty print the result.
            # Note that we coerce `indent=0` into `indent=None`.
            base_media_type, params = parse_header(accepted_media_type.encode('ascii'))
            try:
                return zero_as_none(max(min(int(params['indent']), 8), 0))
            except (KeyError, ValueError, TypeError):
                pass

        # If 'indent' is provided in the context, then pretty print the result.
        # E.g. If we're being called by the BrowsableAPIRenderer.
        return renderer_context.get('indent', None)

    def render(self, data, accepted_media_type=None, renderer_context=None):
        """
        Render `data` into JSON, returning a bytestring.
        """
        if data is None:
            return bytes()

        renderer_context = renderer_context or {}
        indent = self.get_indent(accepted_media_type, renderer_context)

        ret = ujson.dumps(
            data,
            indent=indent, ensure_ascii=self.ensure_ascii,
        )

        # On python 2.x json.dumps() returns bytestrings if ensure_ascii=True,
        # but if ensure_ascii=False, the return type is underspecified,
        # and may (or may not) be unicode.
        # On python 3.x json.dumps() returns unicode strings.
        if isinstance(ret, six.text_type):
            # We always fully escape \u2028 and \u2029 to ensure we output JSON
            # that is a strict javascript subset. If bytes were returned
            # by json.dumps() then we don't have these characters in any case.
            # See: http://timelessrepo.com/json-isnt-a-javascript-subset
            ret = ret.replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
            return bytes(ret.encode('utf-8'))
        return ret

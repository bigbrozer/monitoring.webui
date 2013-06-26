# -*- coding: utf-8 -*-
# Copyright (C) Faurecia <http://www.faurecia.com/>
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
# DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE
# OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""Compatibility Middlewares"""

# From Gist: git://gist.github.com/113635.git
#
from django.conf import settings
from django.core.exceptions import MiddlewareNotUsed
from django.utils.decorators import decorator_from_middleware

CONTENT_TYPES = ('text/html', 'application/xhtml+xml', 'application/xml')
HEADER_VALUE = getattr(settings, 'X_UA_COMPATIBLE', 'IE=edge')


class XUACompatibleMiddleware(object):
    """
    Set X-UA-Compatible HTTP header for all request or specific view using
    a decorator.

    Settings:
        X_UA_COMPATIBLE: default to ``IE=edge``.
    """

    def __init__(self, value=None):

        self.value = value
        if value is None:
            self.value = HEADER_VALUE
        if not self.value:
            raise MiddlewareNotUsed

    def process_response(self, request, response):
        response_ct = response.get('Content-Type', '').split(';', 1)[0].lower()
        if response_ct in CONTENT_TYPES:
            if not 'X-UA-Compatible' in response:
                response['X-UA-Compatible'] = self.value
        return response

xuacompatible = decorator_from_middleware(XUACompatibleMiddleware)

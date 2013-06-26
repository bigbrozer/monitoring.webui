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

import urllib
import hashlib

from django import template
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.html import escape
from django.utils import simplejson

GRAVATAR_URL_PREFIX = getattr(settings,
                              "GRAVATAR_URL_PREFIX",
                              "http://www.gravatar.com/")
GRAVATAR_DEFAULT_IMAGE = getattr(settings, "GRAVATAR_DEFAULT_IMAGE",
                                 "identicon")
GRAVATAR_DEFAULT_RATING = getattr(settings, "GRAVATAR_DEFAULT_RATING", "g")
GRAVATAR_DEFAULT_SIZE = getattr(settings, "GRAVATAR_DEFAULT_SIZE", 80)
GRAVATAR_IMG_CLASS = getattr(settings, "GRAVATAR_IMG_CLASS", "gravatar")

register = template.Library()


def _imgclass_attr():
    if GRAVATAR_IMG_CLASS:
        return '%s' % (GRAVATAR_IMG_CLASS,)
    return ''


def _wrap_img_tag(url, info, extra_style):
    return '<img src="%s" class="%s %s" alt="Avatar for %s">' % (
        escape(url), _imgclass_attr(), extra_style, info)


def _get_user(user):
    if not isinstance(user, User):
        try:
            user = User.objects.get(username=user)
        except User.DoesNotExist:
            raise Exception("Bad user for gravatar.")
    return user


def _get_gravatar_id(email):
    return hashlib.md5(email).hexdigest()


@register.simple_tag
def gravatar_for_email(email, size=None, rating=None):
    """
    Generates a Gravatar URL for the given email address.

    Syntax::

        {% gravatar_for_email <email> [size] [rating] %}

    Example::

        {% gravatar_for_email someone@example.com 48 pg %}
    """
    gravatar_url = "%savatar/%s" % (GRAVATAR_URL_PREFIX,
                                    _get_gravatar_id(email))

    parameters = [p for p in (
        ('d', GRAVATAR_DEFAULT_IMAGE),
        ('s', size or GRAVATAR_DEFAULT_SIZE),
        ('r', rating or GRAVATAR_DEFAULT_RATING),
    ) if p[1]]

    if parameters:
        gravatar_url += '?' + urllib.urlencode(parameters, doseq=True)

    return gravatar_url


@register.simple_tag
def gravatar_for_user(user, size=None, rating=None):
    """
    Generates a Gravatar URL for the given user object or username.

    Syntax::

        {% gravatar_for_user <user> [size] [rating] %}

    Example::

        {% gravatar_for_user request.user 48 pg %}
        {% gravatar_for_user 'jtauber' 48 pg %}
    """
    user = _get_user(user)
    return gravatar_for_email(user.email, size, rating)


@register.simple_tag
def gravatar_img_for_email(email, size=None, rating=None, extra_style=""):
    """
    Generates a Gravatar img for the given email address.

    Syntax::

        {% gravatar_img_for_email <email> [size] [rating] [extra_style] %}

    Example::

        {% gravatar_img_for_email someone@example.com 48 pg %}
    """
    gravatar_url = gravatar_for_email(email, size, rating)
    return _wrap_img_tag(gravatar_url, email, extra_style)


@register.simple_tag
def gravatar_img_for_user(user, size=None, rating=None):
    """
    Generates a Gravatar img for the given user object or username.

    Syntax::

        {% gravatar_img_for_user <user> [size] [rating] %}

    Example::

        {% gravatar_img_for_user request.user 48 pg %}
        {% gravatar_img_for_user 'jtauber' 48 pg %}
    """
    gravatar_url = gravatar_for_user(user, size, rating)
    return _wrap_img_tag(gravatar_url, user.username)


@register.simple_tag
def gravatar_profile_for_email(email):
    """
    Generates the gravatar profile in json format for the given email address.

    Syntax::

        {% gravatar_profile_for_email <email> %}

    Example::

        {% gravatar_profile_for_email someone@example.com %}
    """
    gravatar_url = "%s%s.json" % (GRAVATAR_URL_PREFIX, _get_gravatar_id(email))
    return simplejson.load(urllib.urlopen(gravatar_url))


@register.simple_tag
def gravatar_profile_for_user(user):
    """
    Generates the gravatar profile in json format for the given user object or
    username.

    Syntax::

        {% gravatar_profile_for_user <user> %}

    Example::

        {% gravatar_profile_for_user request.user %}
        {% gravatar_profile_for_user 'jtauber' %}
    """
    user = _get_user(user)
    return gravatar_profile_for_email(user.email)

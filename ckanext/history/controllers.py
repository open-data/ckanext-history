#!/usr/bin/env python
# encoding: utf-8
import sys
from functools import partial

from docutils.core import publish_string, publish_parts
from ckan.lib import base
import ckan.logic as logic
import ckan.plugins as plugins


def trim(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxint
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxint:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)


class APIExtController(base.BaseController):
    def list(self):
        # Force the action cache to load. If we skip this step and an action
        # hasn't been called elsewhere yet, we may only get the built-in
        # actions.
        try:
            logic.get_action('~_~')
        except KeyError:
            pass

        action_filters = []

        # There appears to be no other way of getting all the action routes,
        # so we iterate over the (private) action cache.
        action_methods = sorted(
            (k, v) for k, v in logic._actions.iteritems()
            if all(action_filter(k, v) for action_filter in action_filters)
        )

        return plugins.toolkit.render(
            'api_list.html',
            extra_vars={
                'action_methods': action_methods,
                'publish_string': publish_string,
                'publish_parts': partial(
                    publish_parts,
                    writer_name='html',
                    settings_overrides={
                        'field_name_limit': 0,
                        'syntax_highlight': 'short'
                    }
                ),
                'trim': trim
            }
        )

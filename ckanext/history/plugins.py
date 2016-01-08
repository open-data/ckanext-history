#!/usr/bin/env python
# encoding: utf-8
import ckan.plugins as p
import pylons.config as config

import ckanext.history.helpers as h


class HistoryPlugin(p.SingletonPlugin):
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IConfigurer)
    p.implements(p.ITemplateHelpers)

    def update_config(self, config):
        p.toolkit.add_template_directory(config, 'templates')

    def get_helpers(self):
        return {
            'dataset_revisions': h.dataset_revisions
        }

    def before_map(self, map):
        return map

    def after_map(self, map):
        map.connect(
            'dataset_history',
            config.get('ckanext.history.url', '/dataset/history/{id}'),
            action='history',
            ckan_icon='time'
        )

        return map

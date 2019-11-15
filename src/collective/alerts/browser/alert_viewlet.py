# -*- coding: utf-8 -*-
from plone.app.caching.interfaces import IPloneCacheSettings
from plone.app.layout.viewlets.common import ViewletBase
from plone.registry.interfaces import IRegistry
from zope.component import queryUtility
import json


class AlertViewlet(ViewletBase):
    """Displays alert messages"""
    cache_view = False
    cache_global_view = False

    def update(self):
        super(AlertViewlet, self).update()
        alerts = getattr(self.context, 'enable_alerts', False)
        if alerts:
            self.show_in_context = True
        else:
            self.show_in_context = False
        self.get_message_view = "%s/get-alert-message" % self.context.portal_url.getPortalObject().absolute_url()
        self.get_global_message_view = (
                "%s/get-global-alert-message" %
                self.context.portal_url.getPortalObject().absolute_url()
        )
        self.should_cache()

    def should_cache(self):
        # We will check in the caching configuration, if the view is listed, then we'll allow it to cache
        # This is because jquery .ajax() call will automatically bust cache if this is a json resource
        registry = queryUtility(IRegistry)
        if registry:
            ploneCacheSettings = registry.forInterface(
                IPloneCacheSettings, check=False)
            if ploneCacheSettings.templateRulesetMapping is not None:
                ruleset = ploneCacheSettings.templateRulesetMapping.get("get-alert-message", None)
                if ruleset:
                    self.cache_view = True
                ruleset_global = ploneCacheSettings.templateRulesetMapping.get("get-global-alert-message", None)
                if ruleset_global:
                    self.cache_global_view = True

    def json_config(self, kind="local"):
        results = dict()
        results["show_in_context"] = self.show_in_context
        if kind == "local":
            results["get_message_view"] = self.get_message_view
            results["cache"] = self.cache_view
        else:
            results["get_message_view"] = self.get_global_message_view
            results["cache"] = self.cache_global_view
        return json.dumps(results)

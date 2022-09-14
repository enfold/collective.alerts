# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone.app.upgrade.utils import loadMigrationProfile
from Products.CMFCore.interfaces._content import IContentish
import logging


logger = logging.getLogger(__name__)


def walk(folder):
    for id in folder.objectIds():
        item = folder[id]
        base_item = aq_inner(item)
        if not IContentish.providedBy(base_item):
            continue

        isfolder = getattr(base_item, "objectIds", None) is not None

        yield item

        if isfolder:
            for subitem in walk(item):
                yield subitem


def reload_gs_profile(context):
    loadMigrationProfile(
        context, "profile-collective.alerts:default",
    )


def upgrade_to_1001(portal_setup):
    portal_setup.runAllImportStepsFromProfile(
        "profile-collective.alerts:upgrade1001"
    )

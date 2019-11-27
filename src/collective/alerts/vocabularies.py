# -*- coding: utf-8 -*-

from collective.alerts.interfaces import IAlertsSettings
from Products.CMFPlone.utils import safe_unicode
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.interface import implementer
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@implementer(IVocabularyFactory)
class AlertTypesVocabulary(object):
    """
    """

    def __call__(self, context):
        items = [SimpleTerm('disabled', 'disabled', u"Disabled")]
        registry = getUtility(IRegistry)
        alerts_settings = registry.forInterface(IAlertsSettings, check=False)
        if alerts_settings.alert_types:
            alert_types = alerts_settings.alert_types.split()
            for entry in alert_types:
                split_entry = entry.split('|')
                if len(split_entry) == 2:
                    items.append(
                        SimpleTerm(
                            split_entry[0],
                            split_entry[0],
                            safe_unicode(split_entry[1])
                        )
                    )

        return SimpleVocabulary(items)


AlertTypesVocabularyFactory = AlertTypesVocabulary()

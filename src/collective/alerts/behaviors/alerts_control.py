# -*- coding: utf-8 -*-
from plone.autoform import directives
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from z3c.form.interfaces import IAddForm
from z3c.form.interfaces import IEditForm
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IAlertsControl(model.Schema):
    """Behavior interface to exclude items from navigation.
    """

    model.fieldset(
        'settings',
        label=u"Settings",
        fields=['enable_alerts']
    )

    directives.write_permission(enable_alerts='collective.alerts.canChooseWhereToShowAlert')
    enable_alerts = schema.Bool(
        title=u'Enable alerts',
        description=u'Allow alerts to be shown here',
        required=False,
    )

    directives.omitted('enable_alerts')
    directives.no_omit(IEditForm, 'enable_alerts')
    directives.no_omit(IAddForm, 'enable_alerts')


class AlertsControl(object):

    def __init__(self, context):
        self.context = context

    def _get_enable_alerts(self):
        return self.context.enable_alerts

    def _set_enable_alerts(self, value):
        self.context.enable_alerts = value

    enable_alerts = property(_get_enable_alerts, _set_enable_alerts)

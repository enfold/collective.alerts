# -*- coding: utf-8 -*-
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

from collective.alerts.interfaces import IAlertsSettings
from plone.z3cform import layout
from z3c.form import form


class AlertsControlPanelForm(RegistryEditForm):
    form.extends(RegistryEditForm)
    schema = IAlertsSettings


AlertsControlPanelView = layout.wrap_form(AlertsControlPanelForm, ControlPanelFormWrapper)
AlertsControlPanelView.label = u"Alerts settings"

# -*- coding: utf-8 -*-
from collective.alerts.interfaces import IAlertsSettings
from Products.Five import BrowserView
from plone.api import portal as portal_api
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import IRichTextValue
from plone.app.textfield.value import RichTextValue
from plone.autoform import directives
from plone.autoform.form import AutoExtensibleForm
from plone.registry.interfaces import IRegistry
from plone.supermodel.directives import primary
from plone.supermodel import model
from Products.CMFPlone.interfaces import IPloneSiteRoot
from z3c.caching.interfaces import IPurgePaths
from z3c.caching.purge import Purge
from z3c.form import button
from z3c.form.form import EditForm
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.component import getUtility
from zope.event import notify
from zope.interface import implementer
from zope.schema import Bool
from zope.schema import Choice
from zope.schema import Float
from zope.schema import Int
from zope.schema import TextLine
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from datetime import datetime

import json
import urllib.parse


ANN_KEY = "collective.alerts"


location_items = [
    ("fixed_top", u"Fixed on top"),
    ("slide_left", u"Slide from the left"),
    ("slide_right", u"Slide from the right"),
]

location_terms = [SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in location_items]

location_vocab = SimpleVocabulary(location_terms)


class IAlertSchema(model.Schema):

    directives.widget(alert_type='plone.app.z3cform.widget.SelectFieldWidget')
    alert_type = Choice(
        title=u"Alert type",
        vocabulary="collective.alerts.AlertTypes",
        required=True,
    )

    title = TextLine(
        title=u"Title",
        required=False,
        default=u"",
    )

    primary('message')
    message = RichText(
        title=u"Message",
        required=False,
        default=u"",
    )

    show_feedback_button = Bool(
        title='Show Feedback Form Button',
        required=False,
        default=False,
    )

    directives.widget(alert_location='plone.app.z3cform.widget.SelectFieldWidget')
    alert_location = Choice(
        title=u"Alert location",
        description=u"Where to show the alert",
        vocabulary=location_vocab,
        required=True,
    )

    cookie_expire = Float(
        title=u"Close expire",
        description=(
            u"Provide the amount of hours it will take for an alert to "
            u"appear again if the user dismisses it. You can specify "
            u"fractions of an hout, example, 0.5 will be half hour. Use 0 so "
            u"it will show up on every page refresh."
        ),
        required=False,
        default=24.0,
    )

    retract_timeout = Int(
        title=u"Auto retract",
        description=(
            u"Number of seconds that should pass, before the alert closes "
            u"automatically. Set this value to 0 to not retract the alert "
            u"automatically."
        ),
        required=False,
        default=0,
    )

    display_on_every_page = Bool(
        title=u"Display on every page",
        description=(
            u"If not checked, the alert will be displayed only in locations "
            u"where they are specifically allowed."
        ),
        required=False,
        default=True,
    )


class setAlertMessage(AutoExtensibleForm, EditForm):

    schema = IAlertSchema
    status = ""
    ignoreContext = True

    def updateWidgets(self, *args, **kwargs):
        super(setAlertMessage, self).updateWidgets(*args, **kwargs)

        if not self.request.form:
            annotations = IAnnotations(self.context)
            alert_msg = annotations.get(ANN_KEY, {})

            message = alert_msg.get('message', u"")
            if not IRichTextValue.providedBy(message):
                message = RichTextValue(message)

            self.widgets['message'].value = message
            self.widgets['title'].value = alert_msg.get('title', u"")
            self.widgets['alert_type'].value = (alert_msg.get('klass', 'disabled'),)
            self.widgets['alert_location'].value = (alert_msg.get('alert_location', 'fixed_top'),)
            self.widgets['cookie_expire'].value = alert_msg.get('cookie_expire', 24.0)
            self.widgets['retract_timeout'].value = alert_msg.get('retract_timeout', 0)

            if 'display_on_every_page' in alert_msg and not alert_msg.get('display_on_every_page'):
                self.widgets['display_on_every_page'].value = []
            else:
                self.widgets['display_on_every_page'].value = ['selected']

            if 'show_feedback_button' in alert_msg and not alert_msg.get('show_feedback_button'):
                self.widgets['show_feedback_button'].value = []
            else:
                self.widgets['show_feedback_button'].value = ['selected']

    def update(self):
        self.request.set('disable_border', 1)
        return super(setAlertMessage, self).update()

    @button.buttonAndHandler(u'Apply')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        title = u""
        message = u""
        alert_type = 'disabled'
        alert_location = 'fixed_top'
        visible = False
        cookie_expire = 0
        retract_timeout = 0
        display_on_every_page = True
        show_feedback_button = False

        if data:
            if 'title' in data and data['title']:
                title = data['title']

            if 'message' in data and data['message']:
                message = data['message']

            if 'alert_type' in data:
                alert_type = data['alert_type']

            if 'alert_location' in data:
                alert_location = data['alert_location']

            if alert_type != 'disabled':
                visible = True

            if 'cookie_expire' in data:
                cookie_expire = data["cookie_expire"]

            if 'retract_timeout' in data:
                retract_timeout = data["retract_timeout"]

            if 'display_on_every_page' in data:
                display_on_every_page = data["display_on_every_page"]

            if 'show_feedback_button' in data:
                show_feedback_button = data['show_feedback_button']

        annotations = IAnnotations(self.context)
        annotations[ANN_KEY] = {
            'title': title,
            'message': message,
            'klass': alert_type,
            'alert_location': alert_location,
            'visible': visible,
            'cookie_expire': cookie_expire,
            'retract_timeout': retract_timeout,
            'display_on_every_page': display_on_every_page,
            'date': datetime.now().isoformat(),
            'show_feedback_button': show_feedback_button,
        }

        self.status = ""
        notify(Purge(self.context))
        self.request.response.redirect(self.context.absolute_url())

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
        self.request.response.redirect(self.context.absolute_url())


class BaseGetAlertMessageView(BrowserView):

    def _get_feedback_button(self, came_from):
        portal_url = portal_api.get_tool('portal_url')()
        return f'<p><a class="plone-btn-primary plone-btn btn-alerts-feedback" href="{portal_url}/alerts-feedback-form?came_from={came_from}">Feedback Form</a></p>'


class getAlertMessage(BaseGetAlertMessageView):

    def __call__(self):
        annotations = IAnnotations(self.context)
        results = dict()
        stored_message = annotations.get(ANN_KEY)
        context_url = self.context.absolute_url()
        came_from = urllib.parse.quote_plus(context_url)
        if stored_message:
            show_feedback_button = stored_message.get('show_feedback_button', False)
            for k,v in stored_message.items():
                if k == 'show_feedback_button':
                    continue
                if IRichTextValue.providedBy(v):
                    val = v.output
                else:
                    val = v
                results[k] = val
            if show_feedback_button:
                results['message'] = f'{results["message"]}{self._get_feedback_button(came_from)}'
        else:
            results = {'visible': False}

        self.request.response.setHeader('Content-type', 'application/json')
        return json.dumps(results)


class getGlobalAlertMessage(BaseGetAlertMessageView):

    def __call__(self):

        results = {'visible': False}
        context_url = self.context.absolute_url()
        came_from = urllib.parse.quote_plus(context_url)
        registry = getUtility(IRegistry)
        alerts_settings = registry.forInterface(IAlertsSettings, check=False)
        show_feedback_button = getattr(alerts_settings, 'show_feedback_button', False)
        if alerts_settings.show_alert_from_request:
            header = alerts_settings.alert_request_header
            if header:
                message = self.request.get(header)
                if message:
                    if show_feedback_button:
                        message = f'{message}{self._get_feedback_button(came_from)}'
                    results = {
                        'title': u"",
                        'message': message,
                        'klass': 'info',
                        'alert_location': 'fixed_top',
                        'visible': True,
                        'cookie_expire': 0,
                        'retract_timeout': 0,
                        'display_on_every_page': True,
                        'date': datetime.now().isoformat(),
                    }

        self.request.response.setHeader('Content-type', 'application/json')
        return json.dumps(results)


@adapter(IPloneSiteRoot)
@implementer(IPurgePaths)
class AlertViewPurgePaths(object):
    """
    """

    def __init__(self, context):
        self.context = context

    def getRelativePaths(self):
        return ['/get-alert-message', '/get-global-alert-message']

    def getAbsolutePaths(self):
        return []
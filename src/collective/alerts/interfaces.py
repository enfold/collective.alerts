# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from collective.alerts import _
from plone.app.textfield import RichText
from zope.interface import Interface
from zope import schema


class ICollectiveAlertsLayer(Interface):
    """Marker interface that defines a browser layer."""


class IAlertsSettings(Interface):

    show_alert_from_request = schema.Bool(
        title=_(u"Allow to show an alert from a request header"),
        description=_(
            u"If this is enabled, the system will look for a message in a "
            u"special request header, and show it in the site."
        ),
        required=False,
        default=True,
    )

    show_feedback_button = schema.Bool(
        title=_('Show Feedback Form Button'),
        required=False,
        default=False,
    )

    feedback_form_title = schema.TextLine(
        title=_('Feedback Form Title'),
        required=False,
        default='Feedback Form',
    )

    feedback_form_text = RichText(
        title=_('Feedback Form Text'),
        description=_('Text to be displayed between the form title and the form field(s).'),
        required=False,
    )

    feedback_form_message_max_length = schema.Int(
        title=_('Feedback Form Message Max Length'),
        description=_('The maximum number of characters allowed for the feedback form message.'),
        required=True,
        default=1024,
    )

    feedback_form_recipients = schema.Text(
        title=_('Feedback Form Recipients'),
        description=_('Specify the emails, user ids, or login names for the people that will receive the feedback form '
                      "submissions. If this is left blank or a list of emails can't be generated from the provided "
                      "information, the submission emails will be sent to the site 'From' email address specified on "
                      "the mail control panel."),
        required=False,
    )
    alert_request_header = schema.TextLine(
        title=_(u"Request header"),
        description=_(
            u"Specify here which request header to use to pull the alert "
            u"message from"
        ),
        required=False,
        default=u"HTTP_X_STATUS_MESSAGE",
    )

    alert_types = schema.Text(
        title=_(u"Alert types"),
        description=_(
            u"Add here the different alert types. Notice that the Javascript "
            u"will automatically prepend 'alert-' to the type id. Format: "
            u"id|title"
        ),
        required=False,
        default=u"",
    )

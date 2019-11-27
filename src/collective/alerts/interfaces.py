# -*- coding: utf-8 -*-
"""Module where all interfaces, events and exceptions live."""
from collective.alerts import _
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

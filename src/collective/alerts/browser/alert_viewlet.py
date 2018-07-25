# -*- coding: utf-8 -*-
from plone.app.layout.viewlets.common import ViewletBase


class AlertViewlet(ViewletBase):
    """Displays alert messages"""

    def update(self):
        super(AlertViewlet, self).update()
        alerts = getattr(self.context, 'enable_alerts', False)
        if alerts:
            self.show_in_context = "true"
        else:
            self.show_in_context = "false"
        self.get_message_view = "%s/get-alert-message" % self.context.portal_url.getPortalObject().absolute_url()
        self.get_global_message_view = (
                "%s/get-global-alert-message" %
                self.context.portal_url.getPortalObject().absolute_url()
        )

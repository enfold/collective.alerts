
import logging
import os
from collective.alerts.interfaces import IAlertsSettings
from plone.api import portal as portal_api
from plone.api import user as user_api
from plone.app.textfield.interfaces import IRichTextValue
from plone.registry.interfaces import IRegistry
from Products.CMFPlone.PloneTool import EMAIL_RE
from Products.CMFPlone.RegistrationTool import checkEmailAddress
from Products.CMFPlone.RegistrationTool import EmailAddressInvalid
from zope.component import getUtility
from zope.publisher.browser import BrowserView

logger = logging.getLogger(__name__)

DEFAULT_SETTINGS = (
    ('feedback_form_title', 'Feedback Form'),
    ('feedback_form_text', ''),
    ('feedback_form_message_max_length', 1024),
    ('feedback_form_recipients', ()),
)

EMAIL_TEXT_FORMAT = """Alert feedback from %s(%s).

%s
"""


class FeedbackFormView(BrowserView):

    _settings = None

    def maxlength(self):
        return self.settings['feedback_form_message_max_length']

    def title(self):
        return self.settings['feedback_form_title']

    def text(self):
        return self.settings['feedback_form_text']

    def __call__(self, *args, **kwargs):
        context = self.context
        request = self.request

        if request.get('cancel'):
            came_from = request.get('came_from')
            if came_from:
                url = came_from
            else:
                url = context.absolute_url()
            return request.response.redirect(url)
        if request.get('submit'):
            message = request.get('message')
            came_from = request.get('came_from', None)
            if message:
                if len(message) > self.maxlength():
                    msg = u'Message length must not exceed %s characters.'
                    msg = msg % self.maxlength

                    portal_api.show_message(message=msg,
                                            request=request,
                                            type='error')
                else:
                    emails = self._get_emails()
                    subject = 'Alert Feedback Form Submission'
                    email_to = ','.join(emails)
                    user = user_api.get_current()
                    username = user.getUserName()
                    fullname = user.getProperty('fullname')
                    if not fullname:
                        fullname = username
                    last_name = user.getProperty('last_name', default=None)
                    if last_name:
                        first_name = user.getProperty('first_name')
                        name = f'{last_name}, {first_name}'
                    else:
                        name = fullname

                    email_text = EMAIL_TEXT_FORMAT % (name, user.getProperty('email'), message)
                    portal_api.send_email(body=email_text, recipient=email_to, subject=subject)
                    msg = u'Your feedback has been submitted. Thank you.'
                    portal_api.show_message(message=msg,
                                            request=request,
                                            type='info')
                    if came_from:
                        return request.response.redirect(came_from)
                    else:
                        return request.response.redirect(
                            context.absolute_url()
                        )
            else:
                msg = u'You must provide a message.'
                portal_api.show_message(message=msg,
                                        request=request,
                                        type='error')
        return super(FeedbackFormView, self).__call__(*args, **kwargs)

    @property
    def settings(self):
        if self._settings is None:
            registry = getUtility(IRegistry)
            alerts_settings = registry.forInterface(IAlertsSettings, check=False)
            settings = self._settings = dict()
            for attr, default in DEFAULT_SETTINGS:
                v = getattr(alerts_settings, attr, default)
                if v is None:
                    v = default
                if IRichTextValue.providedBy(v):
                    val = v.output
                else:
                    val = v
                settings[attr] = val

        return self._settings

    def _get_emails(self):
        emails = dict()
        recipients = list()
        base_recipients = list(self.settings['feedback_form_recipients'])
        if base_recipients:
            recipients.extend(base_recipients)
        additional_recipients = os.getenv('ALERTS_FEEDBACK_RECIPIENTS')
        if additional_recipients:
            additional_recipients = additional_recipients.split()
        else:
            additional_recipients = list()
        recipients.extend(additional_recipients)
        for recipient in recipients:
            invalid_email = True
            user = user_api.get(userid=recipient)
            if user is None:
                user = user_api.get(username=recipient)
            if user is None:
                email = recipient
            else:
                email = user.getProperty('email')

            if EMAIL_RE.search(email) is not None:
                try:
                    checkEmailAddress(email)
                    emails[email] = 1
                    invalid_email = False
                except EmailAddressInvalid:
                    pass
            if invalid_email:
                logger.error(f'Could not find a valid email for recipient "{recipient}"')

        return [k for k in emails]

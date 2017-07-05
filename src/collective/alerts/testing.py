# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import collective.alerts


class CollectiveAlertsLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        self.loadZCML(package=collective.alerts)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.alerts:default')


COLLECTIVE_ALERTS_FIXTURE = CollectiveAlertsLayer()


COLLECTIVE_ALERTS_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_ALERTS_FIXTURE,),
    name='CollectiveAlertsLayer:IntegrationTesting'
)


COLLECTIVE_ALERTS_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_ALERTS_FIXTURE,),
    name='CollectiveAlertsLayer:FunctionalTesting'
)


COLLECTIVE_ALERTS_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        COLLECTIVE_ALERTS_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE
    ),
    name='CollectiveAlertsLayer:AcceptanceTesting'
)

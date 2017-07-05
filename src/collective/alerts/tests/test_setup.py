# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from idea.theme.testing import IDEA_THEME_INTEGRATION_TESTING  # noqa
from plone import api

import unittest


class TestSetup(unittest.TestCase):
    """Test that idea.static is properly installed."""

    layer = IDEA_THEME_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

    def test_product_installed(self):
        """Test if idea.static is installed."""
        self.assertTrue(self.installer.isProductInstalled(
            'idea.static'))

    def test_browserlayer(self):
        """Test that IIdeaThemeLayer is registered."""
        from idea.theme.interfaces import (
            IIdeaThemeLayer)
        from plone.browserlayer import utils
        self.assertIn(IIdeaThemeLayer, utils.registered_layers())


class TestUninstall(unittest.TestCase):

    layer = IDEA_THEME_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')
        self.installer.uninstallProducts(['idea.static'])

    def test_product_uninstalled(self):
        """Test if idea.static is cleanly uninstalled."""
        self.assertFalse(self.installer.isProductInstalled(
            'idea.static'))

    def test_browserlayer_removed(self):
        """Test that IIdeaThemeLayer is removed."""
        from idea.theme.interfaces import IIdeaThemeLayer
        from plone.browserlayer import utils
        self.assertNotIn(IIdeaThemeLayer, utils.registered_layers())

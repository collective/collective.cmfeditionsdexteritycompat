#coding=utf8
from plone.app.testing import (IntegrationTesting, FunctionalTesting, PLONE_FIXTURE, 
    PloneSandboxLayer)
from plone.testing import z2
from serpro.sitiorfbpolicy.config import PACKAGE_NAME

class PackageLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        pass

    def setUpPloneSite(self, portal):
        pass
    def tearDownZope(self, app):
        pass

FIXTURE = PackageLayer()
INTEGRATION_TESTING = IntegrationTesting(bases=(FIXTURE,), name='%s:Integration' % PACKAGE_NAME)
FUNCTIONAL_TESTING = FunctionalTesting(bases=(FIXTURE,), name='%s:Functional' % PACKAGE_NAME)


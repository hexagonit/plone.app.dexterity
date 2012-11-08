from Products.CMFCore.utils import getToolByName
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles
from plone.dexterity.utils import createContentInContainer
from zope.lifecycleevent import modified

import unittest


class PloneAppDexterity(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        """Set up Zope."""

        # Load ZCML
        import plone.app.dexterity
        self.loadZCML(package=plone.app.dexterity)
        import plone.app.dexterity.tests.types
        self.loadZCML(package=plone.app.dexterity.tests.types)

    def setUpPloneSite(self, portal):
        """Set up Plone."""
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'plone.app.dexterity:default')
        self.applyProfile(portal, 'plone.app.dexterity.tests.types:default')

    def tearDownZope(self, app):
        """Tear down Zope."""


FIXTURE = PloneAppDexterity()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,), name="PloneAppDexterity:Integration")
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,), name="PloneAppDexterity:Functional")


class IntegrationTestCase(unittest.TestCase):
    """Base class for integration tests."""

    layer = INTEGRATION_TESTING


class FunctionalTestCase(unittest.TestCase):
    """Base class for functional tests."""

    layer = FUNCTIONAL_TESTING


class TestCase(IntegrationTestCase):
    """TestCase for Plone setup."""

    def setUp(self):
        self.portal = self.layer['portal']
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.catalog = getToolByName(self.portal, 'portal_catalog')

    def amount_of_unique_values(self, values):
        res = []
        for val in values:
            if val not in res:
                res.append(val)
        return len(res)

    def test_copy_and_paste_archetypes_archetypes_archetypes_archetypes(self):
        """Copy and paste Archetypes Folder which is located at plone root and
        contains three Archetypes Folders hierarchically."""

        # Create structures.
        folder1 = self.portal[self.portal.invokeFactory('Folder', 'folder1')]
        folder1.reindexObject()
        folder11 = folder1[folder1.invokeFactory('Folder', 'folder11')]
        folder11.reindexObject()
        folder111 = folder11[folder11.invokeFactory('Folder', 'folder111')]
        folder111.reindexObject()
        folder1111 = folder111[folder111.invokeFactory('Folder', 'folder1111')]
        folder1111.reindexObject()

        self.assertIsNotNone(folder1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste folder1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(folder1.getId()))
        copy_of_folder1 = self.portal['copy_of_folder1']
        copy_of_folder11 = copy_of_folder1['folder11']
        copy_of_folder111 = copy_of_folder11['folder111']
        copy_of_folder1111 = copy_of_folder111['folder1111']

        self.assertIsNotNone(copy_of_folder1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

    def test_copy_and_paste_archetypes_archetypes_archetypes_dexterity(self):
        """Copy and paste Archetypes Folder which is located at plone root and
        contains Archetypes Folder / Archetypes Folder / Dexterity Container hierarchically."""

        # Create structures.
        folder1 = self.portal[self.portal.invokeFactory('Folder', 'folder1')]
        folder1.reindexObject()
        folder11 = folder1[folder1.invokeFactory('Folder', 'folder11')]
        folder11.reindexObject()
        folder111 = folder11[folder11.invokeFactory('Folder', 'folder111')]
        folder111.reindexObject()
        container1111 = createContentInContainer(folder111, 'TestContainer', id='container1111')
        modified(container1111)

        self.assertIsNotNone(container1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste folder1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(folder1.getId()))
        copy_of_folder1 = self.portal['copy_of_folder1']
        copy_of_folder11 = copy_of_folder1['folder11']
        copy_of_folder111 = copy_of_folder11['folder111']
        copy_of_container1111 = copy_of_folder111['container1111']

        self.assertIsNotNone(copy_of_container1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

    def test_copy_and_paste_archetypes_archetypes_dexterity_archetypes(self):
        """Copy and paste Archetypes Folder which is located at plone root and
        contains Archetypes Folder / Dexterity Container / Archetypes Folder hierarchically."""

        # Create structures.
        folder1 = self.portal[self.portal.invokeFactory('Folder', 'folder1')]
        folder1.reindexObject()
        folder11 = folder1[folder1.invokeFactory('Folder', 'folder11')]
        folder11.reindexObject()
        container111 = createContentInContainer(folder11, 'TestContainer', id='container111')
        modified(container111)
        folder1111 = container111[container111.invokeFactory('Folder', 'folder1111')]
        folder1111.reindexObject()

        self.assertIsNotNone(folder1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste folder1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(folder1.getId()))
        copy_of_folder1 = self.portal['copy_of_folder1']
        copy_of_folder11 = copy_of_folder1['folder11']
        copy_of_container111 = copy_of_folder11['container111']
        copy_of_folder1111 = copy_of_container111['folder1111']

        self.assertIsNotNone(copy_of_folder1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)


    def test_copy_and_paste_archetypes_archetypes_dexterity_dexterity(self):
        """Copy and paste Archetypes Folder which is located at plone root and
        contains Archetypes Folder / Dexterity Container / Dexterity Container hierarchically."""

        # Create structures.
        folder1 = self.portal[self.portal.invokeFactory('Folder', 'folder1')]
        folder1.reindexObject()
        folder11 = folder1[folder1.invokeFactory('Folder', 'folder11')]
        folder11.reindexObject()
        container111 = createContentInContainer(folder11, 'TestContainer', id='container111')
        modified(container111)
        container1111 = createContentInContainer(container111, 'TestContainer', id='container1111')
        modified(container1111)

        self.assertIsNotNone(container1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste folder1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(folder1.getId()))
        copy_of_folder1 = self.portal['copy_of_folder1']
        copy_of_folder11 = copy_of_folder1['folder11']
        copy_of_container111 = copy_of_folder11['container111']
        copy_of_container1111 = copy_of_container111['container1111']

        self.assertIsNotNone(copy_of_container1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

    def test_copy_and_paste_archetypes_dexterity_archetypes_archetypes(self):
        """Copy and paste Archetypes Folder which is located at plone root and
        contains Dexterity Container / Archetypes Folder / Archetypes Folder hierarchically."""

        # Create structures.
        folder1 = self.portal[self.portal.invokeFactory('Folder', 'folder1')]
        folder1.reindexObject()
        container11 = createContentInContainer(folder1, 'TestContainer', id='container11')
        modified(container11)
        folder111 = container11[container11.invokeFactory('Folder', 'folder111')]
        folder111.reindexObject()
        folder1111 = folder111[folder111.invokeFactory('Folder', 'folder1111')]
        folder1111.reindexObject()

        self.assertIsNotNone(folder1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste folder1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(folder1.getId()))
        copy_of_folder1 = self.portal['copy_of_folder1']
        copy_of_container11 = copy_of_folder1['container11']
        copy_of_folder111 = copy_of_container11['folder111']
        copy_of_folder1111 = copy_of_folder111['folder1111']

        self.assertIsNotNone(copy_of_folder1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

    def test_copy_and_paste_archetypes_dexterity_archetypes_dexterity(self):
        """Copy and paste Archetypes Folder which is located at plone root and
        contains Dexterity Container / Archetypes Folder / Dexterity Container hierarchically."""

        # Create structures.
        folder1 = self.portal[self.portal.invokeFactory('Folder', 'folder1')]
        folder1.reindexObject()
        container11 = createContentInContainer(folder1, 'TestContainer', id='container11')
        modified(container11)
        folder111 = container11[container11.invokeFactory('Folder', 'folder111')]
        folder111.reindexObject()
        container1111 = createContentInContainer(folder111, 'TestContainer', id='container1111')
        modified(container1111)

        self.assertIsNotNone(container1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste folder1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(folder1.getId()))
        copy_of_folder1 = self.portal['copy_of_folder1']
        copy_of_container11 = copy_of_folder1['container11']
        copy_of_folder111 = copy_of_container11['folder111']
        copy_of_container1111 = copy_of_folder111['container1111']

        self.assertIsNotNone(copy_of_container1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

    def test_copy_and_paste_archetypes_dexterity_dexterity_archetypes(self):
        """Copy and paste Archetypes Folder which is located at plone root and
        contains Dexterity Container / Dexterity Container / Archetypes Folder hierarchically."""

        # Create structures.
        folder1 = self.portal[self.portal.invokeFactory('Folder', 'folder1')]
        folder1.reindexObject()
        container11 = createContentInContainer(folder1, 'TestContainer', id='container11')
        modified(container11)
        container111 = createContentInContainer(container11, 'TestContainer', id='container111')
        modified(container111)
        folder1111 = container111[container111.invokeFactory('Folder', 'folder1111')]
        folder1111.reindexObject()

        self.assertIsNotNone(folder1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste folder1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(folder1.getId()))
        copy_of_folder1 = self.portal['copy_of_folder1']
        copy_of_container11 = copy_of_folder1['container11']
        copy_of_container111 = copy_of_container11['container111']
        copy_of_folder1111 = copy_of_container111['folder1111']

        self.assertIsNotNone(copy_of_folder1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

    def test_copy_and_paste_archetypes_dexterity_dexterity_dexterity(self):
        """Copy and paste Archetypes Folder which is located at plone root and
        contains Dexterity Container / Dexterity Container / Dexterity Container hierarchically."""

        # Create structures.
        folder1 = self.portal[self.portal.invokeFactory('Folder', 'folder1')]
        folder1.reindexObject()
        container11 = createContentInContainer(folder1, 'TestContainer', id='container11')
        modified(container11)
        container111 = createContentInContainer(container11, 'TestContainer', id='container111')
        modified(container111)
        container1111 = createContentInContainer(container111, 'TestContainer', id='container1111')
        modified(container1111)

        self.assertIsNotNone(container1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste folder1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(folder1.getId()))
        copy_of_folder1 = self.portal['copy_of_folder1']
        copy_of_container11 = copy_of_folder1['container11']
        copy_of_container111 = copy_of_container11['container111']
        copy_of_container1111 = copy_of_container111['container1111']

        self.assertIsNotNone(copy_of_container1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

    def test_copy_and_paste_dexterity_archtypes_archetypes_archetypes(self):
        """Copy and paste Dexterity Container which is located at plone root and
        contains Archetypes Folder / Archetypes Folder / Archetypes Folder hierarchically."""

        # Create structures.
        container1 = createContentInContainer(self.portal, 'TestContainer', id='container1')
        modified(container1)
        folder11 = container1[container1.invokeFactory('Folder', 'folder11')]
        folder11.reindexObject()
        folder111 = folder11[folder11.invokeFactory('Folder', 'folder111')]
        folder111.reindexObject()
        folder1111 = folder111[folder111.invokeFactory('Folder', 'folder1111')]
        folder1111.reindexObject()

        self.assertIsNotNone(folder1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste container1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(container1.getId()))
        copy_of_container1 = self.portal['copy_of_container1']
        copy_of_folder11 = copy_of_container1['folder11']
        copy_of_folder111 = copy_of_folder11['folder111']
        copy_of_folder1111 = copy_of_folder111['folder1111']

        self.assertIsNotNone(copy_of_folder1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

    def test_copy_and_paste_dexterity_archtypes_archetypes_dexterity(self):
        """Copy and paste Dexterity Container which is located at plone root and
        contains Archetypes Folder / Archetypes Folder / Dexterity Container hierarchically."""

        # Create structures.
        container1 = createContentInContainer(self.portal, 'TestContainer', id='container1')
        modified(container1)
        folder11 = container1[container1.invokeFactory('Folder', 'folder11')]
        folder11.reindexObject()
        folder111 = folder11[folder11.invokeFactory('Folder', 'folder111')]
        folder111.reindexObject()
        container1111 = createContentInContainer(folder111, 'TestContainer', id='container1111')
        modified(container1111)

        self.assertIsNotNone(container1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste container1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(container1.getId()))
        copy_of_container1 = self.portal['copy_of_container1']
        copy_of_folder11 = copy_of_container1['folder11']
        copy_of_folder111 = copy_of_folder11['folder111']
        copy_of_container1111 = copy_of_folder111['container1111']

        self.assertIsNotNone(copy_of_container1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

    def test_copy_and_paste_dexterity_archtypes_dexterity_archetypes(self):
        """Copy and paste Dexterity Container which is located at plone root and
        contains Archetypes Folder / Dexterity Container / Archetypes Folder hierarchically."""

        # Create structures.
        container1 = createContentInContainer(self.portal, 'TestContainer', id='container1')
        modified(container1)
        folder11 = container1[container1.invokeFactory('Folder', 'folder11')]
        folder11.reindexObject()
        container111 = createContentInContainer(folder11, 'TestContainer', id='container111')
        modified(container111)
        folder1111 = container111[container111.invokeFactory('Folder', 'folder1111')]
        folder1111.reindexObject()

        self.assertIsNotNone(folder1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste container1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(container1.getId()))
        copy_of_container1 = self.portal['copy_of_container1']
        copy_of_folder11 = copy_of_container1['folder11']
        copy_of_container111 = copy_of_folder11['container111']
        copy_of_folder1111 = copy_of_container111['folder1111']

        self.assertIsNotNone(copy_of_folder1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

    def test_copy_and_paste_dexterity_archtypes_dexterity_dexterity(self):
        """Copy and paste Dexterity Container which is located at plone root and
        contains Archetypes Folder / Dexterity Container / Dexterity Container hierarchically."""

        # Create structures.
        container1 = createContentInContainer(self.portal, 'TestContainer', id='container1')
        modified(container1)
        folder11 = container1[container1.invokeFactory('Folder', 'folder11')]
        folder11.reindexObject()
        container111 = createContentInContainer(folder11, 'TestContainer', id='container111')
        modified(container111)
        container1111 = createContentInContainer(container111, 'TestContainer', id='container1111')
        modified(container1111)

        self.assertIsNotNone(container1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste container1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(container1.getId()))
        copy_of_container1 = self.portal['copy_of_container1']
        copy_of_folder11 = copy_of_container1['folder11']
        copy_of_container111 = copy_of_folder11['container111']
        copy_of_container1111 = copy_of_container111['container1111']

        self.assertIsNotNone(copy_of_container1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

    def test_copy_and_paste_dexterity_dexterity_archetypes_archetypes(self):
        """Copy and paste Dexterity Container which is located at plone root and
        contains Dexterity Container / Archetypes Folder / Archetypes Folder hierarchically."""

        # Create structures.
        container1 = createContentInContainer(self.portal, 'TestContainer', id='container1')
        modified(container1)
        container11 = createContentInContainer(container1, 'TestContainer', id='container11')
        modified(container11)
        folder111 = container11[container11.invokeFactory('Folder', 'folder111')]
        folder111.reindexObject()
        folder1111 = folder111[folder111.invokeFactory('Folder', 'folder1111')]
        folder1111.reindexObject()

        self.assertIsNotNone(folder1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste container1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(container1.getId()))
        copy_of_container1 = self.portal['copy_of_container1']
        copy_of_container11 = copy_of_container1['container11']
        copy_of_folder111 = copy_of_container11['folder111']
        copy_of_folder1111 = copy_of_folder111['folder1111']

        self.assertIsNotNone(copy_of_folder1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

    def test_copy_and_paste_dexterity_dexterity_archetypes_dexterity(self):
        """Copy and paste Dexterity Container which is located at plone root and
        contains Dexterity Container / Archetypes Folder / Dexterity Container hierarchically."""

        # Create structures.
        container1 = createContentInContainer(self.portal, 'TestContainer', id='container1')
        modified(container1)
        container11 = createContentInContainer(container1, 'TestContainer', id='container11')
        modified(container11)
        folder111 = container11[container11.invokeFactory('Folder', 'folder111')]
        folder111.reindexObject()
        container1111 = createContentInContainer(folder111, 'TestContainer', id='container1111')
        modified(container1111)

        self.assertIsNotNone(container1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste container1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(container1.getId()))
        copy_of_container1 = self.portal['copy_of_container1']
        copy_of_container11 = copy_of_container1['container11']
        copy_of_folder111 = copy_of_container11['folder111']
        copy_of_container1111 = copy_of_folder111['container1111']

        self.assertIsNotNone(copy_of_container1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

    def test_copy_and_paste_dexterity_dexterity_dexterity_archetypes(self):
        """Copy and paste Dexterity Container which is located at plone root and
        contains Dexterity Container / Dexterity Container / Archetypes Folder hierarchically."""

        # Create structures.
        container1 = createContentInContainer(self.portal, 'TestContainer', id='container1')
        modified(container1)
        container11 = createContentInContainer(container1, 'TestContainer', id='container11')
        modified(container11)
        container111 = createContentInContainer(container11, 'TestContainer', id='container111')
        modified(container111)
        folder1111 = container111[container111.invokeFactory('Folder', 'folder1111')]
        folder1111.reindexObject()

        self.assertIsNotNone(folder1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste container1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(container1.getId()))
        copy_of_container1 = self.portal['copy_of_container1']
        copy_of_container11 = copy_of_container1['container11']
        copy_of_container111 = copy_of_container11['container111']
        copy_of_folder1111 = copy_of_container111['folder1111']

        self.assertIsNotNone(copy_of_folder1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

    def test_copy_and_paste_dexterity_dexterity_dexterity_dexterity(self):
        """Copy and paste Dexterity Container which is located at plone root and
        contains three Dexterity Container hierarchically."""

        # Create structures.
        container1 = createContentInContainer(self.portal, 'TestContainer', id='container1')
        modified(container1)
        container11 = createContentInContainer(container1, 'TestContainer', id='container11')
        modified(container11)
        container111 = createContentInContainer(container11, 'TestContainer', id='container111')
        modified(container111)
        container1111 = createContentInContainer(container111, 'TestContainer', id='container1111')
        modified(container1111)

        self.assertIsNotNone(container1111)

        # There should be 4 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 4)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 4)

        # Copy and paste container1.
        self.portal.manage_pasteObjects(self.portal.manage_copyObjects(container1.getId()))
        copy_of_container1 = self.portal['copy_of_container1']
        copy_of_container11 = copy_of_container1['container11']
        copy_of_container111 = copy_of_container11['container111']
        copy_of_container1111 = copy_of_container111['container1111']

        self.assertIsNotNone(copy_of_container1111)

        # There should be 8 indexed uuids.
        self.assertEqual(self.catalog.Indexes['UID'].numObjects(), 8)
        # Those uuid values should be unique.
        self.assertEqual(self.amount_of_unique_values(self.catalog.Indexes['UID'].uniqueValues()), 8)

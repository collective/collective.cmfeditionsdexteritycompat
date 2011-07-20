#coding=utf8
from Products.CMFCore.utils import getToolByName
from plone.app.testing import setRoles
from plone.app.testing.interfaces import (TEST_USER_ID, TEST_USER_PASSWORD, TEST_USER_ROLES, 
    TEST_USER_NAME)
from plone.testing.z2 import Browser
from collective.cmfeditionsdexteritycompat.testing import FUNCTIONAL_TESTING, TEST_CONTENT_TYPE_ID
import transaction
import unittest2 as unittest
from mechanize import LinkNotFoundError

class FunctionalTestCase(unittest.TestCase):

    layer = FUNCTIONAL_TESTING    
    
    def setUp(self):
        self.portal = self.layer['portal']
        self.portal_url = self.portal.absolute_url()
        self.browser = Browser(self.layer['app'])     
        self.browser.handleErrors = False
        setRoles(self.portal, TEST_USER_ID, ['Manager', 'Member'])
        self.portal.invokeFactory(
            type_name=TEST_CONTENT_TYPE_ID, 
            id='obj1', 
            title=u'Object 1 Title', 
            description=u'Description of obect number 1',
            text=u'Object 1 some footext.',            
        )
        self.obj1 = self.portal['obj1']
    
    def _dump_to_file(self):
        f = open('/tmp/a.html', 'w')
        f.write(self.browser.contents)
        f.close()
    
    def _login_browser(self, userid, password):        
        self.browser.open(self.portal_url + '/login_form')
        self.browser.getControl(name='__ac_name').value = userid
        self.browser.getControl(name='__ac_password').value = password
        self.browser.getControl(name='submit').click()
    
    def assertLinkNotExists(self, *args, **kwargs):
        self.assertRaises(LinkNotFoundError, self.browser.getLink, *args, **kwargs)
    
    def assertControlNotExists(self, *args, **kwargs):
        self.assertRaises(LookupError, self.browser.getControl, *args, **kwargs)
    
    def test_content_core_view(self):
        transaction.commit()
        self._login_browser(TEST_USER_NAME, TEST_USER_PASSWORD)
   
        self.browser.open(self.obj1.absolute_url() + '/@@content-core')

        # Title and description are metadata, not in content-core.
        self.assertFalse(self.obj1.title in self.browser.contents)
        self.assertFalse(self.obj1.description in self.browser.contents)                
        self.assertTrue(self.obj1.text in self.browser.contents)   
   
    def test_version_view(self):
        transaction.commit()
        self._login_browser(TEST_USER_NAME, TEST_USER_PASSWORD)
        
        self.browser.open(self.obj1.absolute_url() + '/@@version-view?version_id=0')
        
        # Title and description are metadata, not in content-core.
        self.assertFalse(self.obj1.title in self.browser.contents)
        self.assertFalse(self.obj1.description in self.browser.contents)                
        self.assertTrue(self.obj1.text in self.browser.contents)    
        
    def test_versions_history_form_should_work_with_dexterity_content(self):        
        old_text = self.obj1.text        
        old_title = self.obj1.title
        
        new_text = 'Some other text for object 1.'        
        new_title = 'My special new title for object 1'

        transaction.commit()
        self._login_browser(TEST_USER_NAME, TEST_USER_PASSWORD)
        self.browser.open(self.obj1.absolute_url() + '/edit')        
        self.browser.getControl(label='Title').value = new_title
        self.browser.getControl(label='Text').value = new_text                
        self.browser.getControl(name='form.buttons.save').click()       
        
        self._assert_versions_history_form(0, self.obj1.getId(), old_title, old_text)
        self._assert_versions_history_form(1, self.obj1.getId(), new_title, new_text)

    def _assert_versions_history_form(self, version_id, obj_id, title, text):
        self.browser.open(
            '%s/%s/versions_history_form?version_id=%s' % (self.portal_url, obj_id, version_id)
        )
        self.assertTrue('Working Copy' in self.browser.contents) 
        self.assertTrue(
            ('/%s/versions_history_form?version_id=%s' % (obj_id, version_id)) in self.browser.contents
        )
        self.assertTrue('Working Copy' in self.browser.contents) 
        self.assertTrue('Revert to this revision' in self.browser.contents)
        self.assertTrue(('/%s/version_diff?version_id1' % obj_id) in self.browser.contents)
        self.assertTrue(('Preview of Revision %s' % version_id) in self.browser.contents)
        self.assertTrue(
            ('<h1 class="documentFirstHeading">%s</h1>' % str(title)) in self.browser.contents
        )
        self.assertTrue(str(text) in self.browser.contents)
    
    def test_versions_history_form_should_work_with_archetypes_content(self):
        old_text = self.obj1.text        
        old_title = self.obj1.title
        
        new_text = 'Some other text for page 1.'        
        new_title = 'My special new title for page 1'        
        
        self.portal.invokeFactory(
            type_name='Document', 
            id='page1', 
            title=old_title, 
            text=old_text,            
        )
        page = self.portal['page1']
        transaction.commit()
        
        self._login_browser(TEST_USER_NAME, TEST_USER_PASSWORD)
        
        self.browser.open(page.absolute_url() + '/edit')        
        self.browser.getControl(label='Title').value = new_title
        self.browser.getControl(label='Body Text').value = new_text                
        self.browser.getControl(name='form.button.save').click()       
                
        self._assert_versions_history_form(0, page.getId(), old_title, old_text)
        self._assert_versions_history_form(1, page.getId(), new_title, new_text)
        

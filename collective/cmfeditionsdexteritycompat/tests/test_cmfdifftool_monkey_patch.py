from Products.CMFDiffTool.interfaces import IDifference
from collective.dexteritydiff.binarydiff import DexterityBinaryDiff
from plone.app.testing import setRoles, TEST_USER_ID
from plone.namedfile.file import NamedFile
from serpro.sitiorfbpolicy.testing import (INTEGRATION_TESTING_WITH_DEXTERITY_DIFF, 
    TEST_CONTENT_TYPE_ID)
import unittest2 as unittest

class CMFDiffToolMonkeyPatchTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING_WITH_DEXTERITY_DIFF    
    
    def setUp(self):
        self.portal = self.layer['portal']
    
    def test_deve_fornecer_inline_diff_se_apenas_conteudo_dos_arquivos_diferir(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj1',
            file=NamedFile(data='contents', filename=u'f.txt')
        )
        obj1 = self.portal['obj1']
        
        self.portal.invokeFactory(
            TEST_CONTENT_TYPE_ID, 
            'obj2',
            file=NamedFile(data='different contents', filename=u'f.txt') 
        )
        obj2 = self.portal['obj2']
                
        diff = DexterityBinaryDiff(obj1, obj2, 'file')
        self.assertTrue(IDifference.providedBy(diff))
        self.assertFalse(diff.same)
        self.assertTrue(diff.inline_diff())
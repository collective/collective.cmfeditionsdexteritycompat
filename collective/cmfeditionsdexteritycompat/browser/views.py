from zope.publisher.interfaces import NotFound
from plone.namedfile.utils import set_headers, stream_data
from Products.CMFCore.utils import getToolByName
import re
from zope.component import getMultiAdapter
from zope.interface import Interface
from five import grok
from plone.dexterity.interfaces import IDexterityContent
     
class VersionView(grok.View):
    grok.context(IDexterityContent)
    grok.require('zope2.View')
    grok.name('version-view')

    def render(self, version_id):
        content_core_view = getMultiAdapter((self.context, self.request), name='content-core')
        html = content_core_view()
        return re.sub(
            r'''/@@download/(?P<field_id>.*?)/(?P<filename>.*?)"''',
            r'''/@@download-version?field_id=\g<field_id>&filename=\g<filename>&version_id=''' + version_id + '"',
            html
        )

class DownloadVersion(grok.View):
    grok.context(IDexterityContent)
    grok.require('zope2.View')
    grok.name('download-version')
    
    def render(self, version_id, field_id, filename):
        repository = getToolByName(self.context, 'portal_repository')
        old_obj = repository.retrieve(self.context, version_id).object
        file_ = getattr(old_obj, field_id)

        if file_ is None:
            raise NotFound(self, filename, self.request)
        
        set_headers(file_, self.request.response, filename=filename)

        return stream_data(file_)


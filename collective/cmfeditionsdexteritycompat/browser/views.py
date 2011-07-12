from zope.publisher.interfaces import NotFound
from plone.namedfile.utils import set_headers, stream_data
from kss.core.BeautifulSoup import BeautifulSoup
from Products.CMFCore.utils import getToolByName
import re
from zope.component import getMultiAdapter
from zope.interface import Interface
from five import grok

class ContentCore(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('content-core')    

    def render(self, *args, **kwargs):
        view = getMultiAdapter((self.context, self.request), name='view')
        content = view()        
        soup = BeautifulSoup(content)
        element_id = 'content-core'
        tag = soup.find('div', id=element_id)
        if tag is None:
            raise RuntimeError, 'Result content did not contain <div id="%s">' % element_id
        # now we send it back to the client
        return unicode(tag)    
    
class VersionView(grok.View):
    grok.context(Interface)
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
    grok.context(Interface)
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


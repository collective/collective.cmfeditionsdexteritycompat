# coding=utf8
from .config import PACKAGE_NAME

    
def import_various(context):
    if context.readDataFile('%s_various.txt' % PACKAGE_NAME) is None:
        return
    
    portal = context.getSite()


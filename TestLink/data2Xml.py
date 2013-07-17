'''
Created on Jul 16, 2013

@author: Eric
'''
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom
import sys

class Data2Xml(object):
    '''
    Data to Xml mapping
    '''
    def __init__(self):
        self.testsuite = Element('testsuite')
    
    def cdataPrefix(self, str):
        '''
        :param str:
        '''
        if (type(str) == int):
            new_str = '![CDATA[%d]]' % (str,) 
        else:
            new_str = '![CDATA[' + str + ']]' 
    
        return new_str

    def prettify(self, elem):
        '''
        :param elem:
        '''
        """Return a pretty-printed XML string for the Element.
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding = 'utf-8')
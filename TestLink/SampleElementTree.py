'''
Created on Jul 2, 2013

@author: Eric
'''

from xml.etree import ElementTree
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom
import sys

def cdataPrefix(str):
    new_str = '![CDATA[' + str + ']]'
    return new_str

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding = 'utf-8')

def SampleElement():
    top = Element('top')
    # ?#@$ What's the difference ?
    tree = ElementTree.ElementTree(top)
    
    comment = Comment('Generated for PyMOTW')
    top.append(comment)
    
    child = SubElement(top, 'child')
    child.text = 'This child contains text.'
    
    child_with_tail = SubElement(top, 'child_with_tail')
    child_with_tail.text = '![CDATA[' + 'This child has regular text.' + ']]'
    child_with_tail.tail = 'And "tail" text.'
    
    child_with_entity_ref = SubElement(top, 'child_with_entity_ref')
    child_with_entity_ref.text = 'This & that'
    
    print prettify(top)
    prettyForm = prettify(top)
    #tree.write(sys.stdout)
    
    with open('somefile.txt', 'w') as the_file:
        the_file.write(prettyForm)
    return prettyForm

if __name__ == '__main__':
    pass
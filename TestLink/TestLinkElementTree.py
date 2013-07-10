'''
Created on Jul 2, 2013

@author: Eric
'''

from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom
import sys

def cdataPrefix(str):
    if (type(str) == int):
        new_str = '![CDATA[%d]]' % (str,) 
    else:
        new_str = '![CDATA[' + str + ']]' 

    return new_str

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ", encoding = 'utf-8')

def TSElement():
    testsuite = Element('testsuite')
    #tree = ET.ElementTree(top)
    
    comment = Comment('Generated for TestLink')
    testsuite.append(comment)
    testsuite.set('name','Home')
    
    detail = SubElement(testsuite, 'detail')
    testcase = SubElement(testsuite, 'testcase')
    testcase.set('name','Verify installation')
    testcase.set('internalid','')
    
    externalid = SubElement(testcase,'externalid')
    externalid.text = cdataPrefix('')
    version = SubElement(testcase,'version')
    version.text = cdataPrefix('')
    summary = SubElement(testcase,'summary')
    summary.text = cdataPrefix('')
    preconditions = SubElement(testcase,'preconditions')
    preconditions.text = cdataPrefix('')
    execution_type = SubElement(testcase,'execution_type')
    execution_type.text = cdataPrefix('1')
    importance = SubElement(testcase,'importance')
    steps = SubElement(testcase,'steps')
    for i in range(3):
        step = SubElement(steps, 'step')
        for j in range(3):
            step_number = SubElement(step, 'step_number')
            idx = j + 1
            step_number.text = cdataPrefix(idx)
            actions = SubElement(step, 'actions')
            actions.text = cdataPrefix('')
            expectedresults = SubElement(step, 'expectedresults')
            expectedresults.text = cdataPrefix('')
            execution_type = SubElement(step, 'execution_type')
            execution_type.text = cdataPrefix(1)
    
    print prettify(testsuite)
    prettyForm = prettify(testsuite)
    
    with open('sampeTestSuite.xml', 'w') as the_file:
        the_file.write(prettyForm)
    return prettyForm

if __name__ == '__main__':
    TSElement()
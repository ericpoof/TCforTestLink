'''
Created on Jul 16, 2013

@author: Eric
'''
from xml.etree import ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom
import sys

class Data2Xml(object):
    """
    Data to Xml mapping
    """
    def __init__(self, ts):
        self.testsuite = ts
        self.testsuiteTag = Element('testsuite')

    def cdataPrefix(self, str):
        """
        Return cdata wrapped string 
        """
        if (type(str) == int):
            new_str = '![CDATA[%d]]' % (str,) 
        else:
            new_str = '![CDATA[' + str + ']]' 
    
        return new_str

    def prettify(self, elem):
        """
        Return a pretty-printed XML string for the Element. 
        """
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding = 'utf-8')

    def getPrettyForm(self):
        return self.prettify(self.testsuiteTag)

    def printPrettyForm(self):
        print self.prettify(self.testsuiteTag)

    def saveTestsuiteTag(self, filename):
        prettyForm = self.getPrettyForm(self.testsuite.Tag)
        with open(filename, 'w') as the_file:
            the_file.write(prettyForm)

    def createTSElement(self):
        ts = self.testsuite
        
        #0 testsuiteTag
        #self.testsuiteTag = Element('testsuite')
        #tree = ET.ElementTree(top)
        
        comment = Comment('Generated for TestLink')
        self.testsuiteTag.append(comment)
        self.testsuiteTag.set('name', ts.name)

        ## additional tags
        detailTag = SubElement(self.testsuiteTag, 'detail')

        #1 testcaseTag
        testcaseTag = SubElement(self.testsuiteTag, 'testcase')
        testcaseTag.set('name','Verify installation')
        testcaseTag.set('internalid','')
        preconditionsTag = SubElement(testcaseTag,'preconditions')
        preconditionsTag.text = self.cdataPrefix('')
        
        ## additional tags
        externalidTag = SubElement(testcaseTag,'externalid')
        externalidTag.text = self.cdataPrefix('')
        versionTag = SubElement(testcaseTag,'version')
        versionTag.text = self.cdataPrefix('')
        summaryTag = SubElement(testcaseTag,'summary')
        summaryTag.text = self.cdataPrefix('')
        execution_typeTag = SubElement(testcaseTag,'execution_type')
        execution_typeTag.text = self.cdataPrefix('1')
        importanceTag = SubElement(testcaseTag,'importance')
        
        #2 steps
        steps = SubElement(testcaseTag,'steps')
        for i in range(3):
            step = SubElement(steps, 'step')
            for j in range(3):
                step_numberTag = SubElement(step, 'step_number')
                idx = j + 1
                step_numberTag.text = self.cdataPrefix(idx)
                actionsTag = SubElement(step, 'actions')
                actionsTag.text = self.cdataPrefix('')
                expectedresultsTag = SubElement(step, 'expectedresults')
                expectedresultsTag.text = self.cdataPrefix('')
                execution_typeTag = SubElement(step, 'execution_type')
                execution_typeTag.text = self.cdataPrefix(1)
        
    
    
    
    
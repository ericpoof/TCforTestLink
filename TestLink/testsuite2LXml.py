'''
Created on Jul 16, 2013

@author: Eric
'''
# from xml.etree import ElementTree as ET
# from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom
from lxml import etree as ET
import sys

class Testsuite2LXml(object):
    """
    Data to Xml mapping
    """
    def __init__(self, ts):
        self.testsuite = ts
        self.testsuiteTag = ET.Element('testsuite')


    """ @deprecated: not used here
    """
    def cdataPrefix(self, str):
        """
        Return cdata wrapped string 
        """
        if (type(str) == int):
            new_str = '<![CDATA[%d]]>' % (str,) 
        else:
            new_str = "<![CDATA[" + str + "]]>" 
    
        return new_str

    """ @deprecated: not used here
    """
    def prettify(self, elem):
        """
        Return a pretty-printed XML string for the Element. 
        """
        rough_string = ET.tostring(elem)
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ", encoding = 'utf-8')

    """ print testsuite in serialization using tostring 
    """
    def getPrettyForm(self):
#         return self.prettify(self.testsuiteTag)
        return ET.tostring(self.testsuiteTag, xml_declaration=True, pretty_print=True)

    def printPrettyForm(self):
        print self.getPrettyForm()

    def saveTestsuiteTag(self, filename):
        prettyForm = self.getPrettyForm()
        with open(filename, 'w') as the_file:
            the_file.write(prettyForm)

    def createTSElement(self):
        ts = self.testsuite
        
        #0 testsuiteTag
        #self.testsuiteTag = Element('testsuite')
        #tree = ET.ElementTree(top)
        
#         comment = Comment('Generated for TestLink')
#         self.testsuiteTag.append(comment)
        """ @var testsuite.name: 
        """
        tsname = ' ' + ts.name
        self.testsuiteTag.set('name', tsname)

        ## additional tags
        detailTag = ET.SubElement(self.testsuiteTag, 'detail')

        #1 testcaseTag
        for idx0, tc in enumerate(ts.testcases): 
            testcaseTag = ET.SubElement(self.testsuiteTag, 'testcase')
    
            """ ...@var testcase.name: 
            """
            tcname = '  ' + tc.name
            testcaseTag.set('name',tcname)
            testcaseTag.set('internalid','')
    
            """ ...@var testcase.preconditions:
            """
            preconditionsTag = ET.SubElement(testcaseTag,'preconditions')
#             preconditionsTag.text = ET.CDATA(tc.preconditions)
            preconditionsTag.text = ET.CDATA(tc.preconditions)
            
            ## additional tags
            externalidTag = ET.SubElement(testcaseTag,'externalid')
            externalidTag.text = ET.CDATA(str(idx0+1000))
            versionTag = ET.SubElement(testcaseTag,'version')
            versionTag.text = ET.CDATA('')
            summaryTag = ET.SubElement(testcaseTag,'summary')
            summaryTag.text = ET.CDATA('')
            execution_typeTag = ET.SubElement(testcaseTag,'execution_type')
            execution_typeTag.text = ET.CDATA(str(1))
            importanceTag = ET.SubElement(testcaseTag,'importance')
        
            #2 steps
            print '-------testcase ', idx0
            print '-----------------'
            stepsTag = ET.SubElement(testcaseTag,'steps')
            stepsLen = len(tc.steps)
            for idx, st in enumerate(tc.steps):
                stepTag = ET.SubElement(stepsTag, 'step')
                """ ......@var step.step_number: 
                """
                step_numberTag = ET.SubElement(stepTag, 'step_number')
                step_numberTag.text = ET.CDATA(str(idx+1))
                """ ......@var step.action: 
                """
                actionsTag = ET.SubElement(stepTag, 'actions')
                print 'st.actions = ', st.actions
                actionsTag.text = ET.CDATA(st.actions)
                """ ......@var step.expectedresults: 
                """
                if stepsLen == (idx+1):
                    expectedresultsTag = ET.SubElement(stepTag, 'expectedresults')
                    expectedresultsTag.text = ET.CDATA(st.expectedresults)
                execution_typeTag = ET.SubElement(stepTag, 'execution_type')
                execution_typeTag.text = ET.CDATA(str(1))
                
        
        """ @return: return testsuite in pretty form 
        """
#         return ET.tostring(self.testsuiteTag, xml_declaration=True, pretty_print=True)
            
        
    
    
    
    
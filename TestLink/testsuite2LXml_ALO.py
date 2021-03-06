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
        return ET.tostring(self.testsuiteTag, encoding='UTF-8', xml_declaration=True, pretty_print=True)

    def printPrettyForm(self):
        print self.getPrettyForm()

    def saveTestsuiteTag(self, filename):
        prettyForm = self.getPrettyForm()
        with open(filename, 'w') as the_file:
            the_file.write(prettyForm)

    def valid_XML_char_ordinal(self, i):
        return ( # conditions ordered by presumed frequency
            0x20 <= i <= 0xD7FF 
            or i in (0x9, 0xA, 0xD)
            or 0xE000 <= i <= 0xFFFD
            or 0x10000 <= i <= 0x10FFFF
            )

    def getUnicode(self, text):
        """
        return unicode if text is str, else return text as is
        @param text: 
        @type text: str or unicode
        """
        try:
            text = unicode(text, 'utf-8')
            return text
        except TypeError:
            return text
        
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
            print ' tc.name type = ', type(tc.name)
            print ' tcname type = ', type(tcname)
            utcname = self.getUnicode(tcname)
            print ' utcname type = ', type(utcname)
            testcaseTag.set('name', utcname)
#             testcaseTag.set('name', tcname)
            testcaseTag.set('internalid','')
    
            """ ...@var testcase.preconditions:
            """
            preconditionsTag = ET.SubElement(testcaseTag,'preconditions')
            preconditionsTag.text = ET.CDATA(tc.preconditions)
            
            ## additional tags
            externalidTag = ET.SubElement(testcaseTag,'externalid')
            externalidTag.text = ET.CDATA(tc.externalId)
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
                actionsTag.text = ET.CDATA(self.getUnicode(st.actions))
                """ ......@var step.expectedresults: 
                """
                expectedresultsTag = ET.SubElement(stepTag, 'expectedresults')
                expectedresultsTag.text = ET.CDATA(self.getUnicode(st.expectedresults))
                # kinky part on Mac not able to encode with mac-roman
#                     print '-----------Expected ', expectedresultsTag.text

                execution_typeTag = ET.SubElement(stepTag, 'execution_type')
                execution_typeTag.text = ET.CDATA(str(1))
                
        
        """ @return: return testsuite in pretty form 
        """
#         return ET.tostring(self.testsuiteTag, xml_declaration=True, pretty_print=True)
            
        
    
    
    
    
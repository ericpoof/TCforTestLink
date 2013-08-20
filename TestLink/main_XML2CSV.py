'''
Created on Jul 1, 2013

@author: me.jung
'''

import xlrd
import re
from testsuite2LXml_ALO import Testsuite2LXml
from xlsData import XlsData
from cellParser_ALO import CellParser
from testSuite import TestSuite, TestCase, Step
from lxml import etree
from _pyio import BytesIO
from schema import ATTLookout_Schema as AL


# Conversion Flow
## 1 XlsData()
### xlrd
### CellExl()

## 2 CellParser()
### re
### TestSuite()/TestCase()/Steps()        

## 3 Testsuite2LXml(testsuite)
### lxml
### testsuiteTag = ET.Element('testsuite')

def parseOneLevel():
    file = 'Testcases/Attfamilymapsample2.xml'
    with open(file, 'r') as f:
        print f
        tree = etree.parse(f)
#     TString = etree.tostring(tree)
#     print TString

#     some_xml_data = "<root>data</root>"
#     root = etree.fromstring(some_xml_data)
#     print(root.tag)
#     TString = etree.tostring(root)
#     print TString
#     etree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=False)    

#     some_file_like_object = BytesIO("<root>data</root>")
#     tree = etree.parse(some_file_like_object)
#     etree.tostring(tree)

    r = tree.xpath('//testcase')
    print type(r)
    for tc in r:
#         print 'tc type = ', type(tc)
        print ""
        print " === testcase ==="
        print tc.get('name')
        for tc_el in tc:
            print ' %s : %s' % (tc_el.tag, tc_el.text)
            if tc_el.tag == 'steps':
                print 'steps type? = ', tc_el.tag
                for st in tc_el:
                    print 'type_tc_el = ', type(st)
                    st_tree = etree.ElementTree(st)
                    print 'step in etree : ', etree.tostring(st_tree)
                    for st_el in st:
                        print ' %s : %s' % (st_el.tag, st_el.text)
def main():


    ## 1st stage to create cell data from a xls spreadsheet
    ## Skipped 1st stage for custom markdown testcases

#     parseOneLevel()
    file = 'Testcases/Home.testsuite-deep.xml'
    with open(file, 'r') as f:
#         print f
        tree = etree.parse(f)
#     print etree.tostring(tree)
    root = tree.getroot()
    print 'root = ', root.tag, root.get('name'), type(root)
    
    ts_root = TestSuite()
    ts_root.name = root.get('name')
    
    def Element_recursive(root, ts_root):
        for elm in root:
            if elm.tag == 'testsuite':
                new_ts = TestSuite()
                new_ts.name = elm.get('name')
                new_ts = Element_recursive(elm, new_ts )
                ts_root.testsuites.append(new_ts)
            elif elm.tag == 'testcase':
                new_tc = TestCase()
                new_tc.name = elm.get('name')
                ts_root.testcases.append(new_tc)
        return ts_root
    
    ts_root = Element_recursive(root, ts_root)
    print 'recursive done'
    x = 1 + 1
    print x

     
#     ## 2nd stage to parse xlsData and create testsuites
#     print '-------------------------------------'
#     print '2nd stage'
#     print '-------------------------------------'
#     cellParser = CellParser()
# 
#     """  @var no_rows: no of rows to parse
#     """ 
#     no_rows = xlsData.getRowLength() 
#     print 'number of rows is ', no_rows
#     cellParser.readTextMD(AL.File)
#     ts = cellParser.parseRows()
#     testsuites = cellParser.parseRows(no_rows)
#     print '-------------------------------------'
#     print 'printing testsuites'
#     print '-------------------------------------'
#     testsuites = [ts] 
#     cellParser.printTestSuites(testsuites)
    print 'done'
# 
#     ## 3rd stage to create xml compatible with TestLink
#     print '-------------------------------------'
#     print ' ### 3rd stage '
#     print '-------------------------------------'
#     
#     ts2xml = Testsuite2LXml(testsuites[0])
#     ts2xml.createTSElement()
#     ts2xml.printPrettyForm()
#     ts2xml.saveTestsuiteTag(AL.OutFile)


if __name__ == '__main__':
    main()

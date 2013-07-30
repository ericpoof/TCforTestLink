'''
Created on Jul 1, 2013

@author: me.jung
'''

import xlrd
import re
from testsuite2LXml import Testsuite2LXml
from xlsData import XlsData
from cellParser import CellParser
from testSuite import TestSuite, TestCase, Step


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


def main():

    from schema import ATTLookout_Schema as AL

    ## 1st stage to create cell data from a xls spreadsheet
    xlsData = XlsData()
    xlsData.readTextMD(AL.File)
     
#     ## 2nd stage to parse xlsData and create testsuites
#     print '-------------------------------------'
#     print '2nd stage'
#     print '-------------------------------------'
#     cellParser = CellParser(xlsData)
# 
#     """  @var no_rows: no of rows to parse
#     """ 
#     no_rows = xlsData.getRowLength() 
#     print 'number of rows is ', no_rows
#     testsuites = cellParser.parseRows(no_rows)
#     print '-------------------------------------'
#     print 'printing testsuites'
#     print '-------------------------------------'
#     cellParser.printTestSuites(testsuites)
# 
#     ## 3rd stage to create xml compatible with TestLink
#     print '-------------------------------------'
#     print ' ### 3rd stage '
#     print '-------------------------------------'
#     
#     ts2xml = Testsuite2LXml(testsuites[0])
#     ts2xml.createTSElement()
#     ts2xml.printPrettyForm()
#     ts2xml.saveTestsuiteTag(TT.OutFile)


if __name__ == '__main__':
    main()

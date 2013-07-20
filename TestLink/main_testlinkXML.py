'''
Created on Jul 1, 2013

@author: me.jung
'''

import xlrd
import re
from tcPattern import TMO_TV
from schema import TMOTV_Schema as S 
from test.test_iterlen import len
# from data2Xml import Data2Xml
from data2LXml import Data2LXml
from xlsData import XlsData
from cellParser import CellParser
from testSuite import TestSuite, TestCase, Step


# Conversion Flow
## 1
## 
## XlsData()

## CellExl()

## 1-2
## CellParser()

## 2
## TestSuite()/TestCase()/Steps()        

## 3
## Data2Xml(testsuite)



def main():
    xlsData = XlsData()
    xlsData.readXls()
    
     
    ## 2nd stage after getting xlsData

    cellParser = CellParser(xlsData)

    ## pass no of rows to parse

    no_rows = xlsData.getColLength()
    testsuites = cellParser.parseRows(no_rows)
    print '-------------------------------------'
    print 'printing testsuites'
    print '-------------------------------------'
    cellParser.printTestSuites(testsuites)

    ## 3rd stage after getting testsuites
    print '-------------------------------------'
    print ' ### 3rd stage '
    print '-------------------------------------'
    
#     data2xml = Data2Xml(testsuites[0])
    """  @ test lxml
    """ 
    data2xml = Data2LXml(testsuites[0])
    data2xml.createTSElement()
    data2xml.printPrettyForm()
    filename = '9testcases1.xml'
    data2xml.saveTestsuiteTag(filename)



if __name__ == '__main__':
    main()

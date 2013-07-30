'''
Created on Jul 9, 2013

@author: Eric
'''

## Schema mapping to testlink xml

class TMOTV_Schema(object):
    """
    Constants for TMO TV in Excel Spreadsheet 
    # col 0: Test Suit: Top, P[1..9] : testcase, XXX : Testsuite name 
    # col 1: id: can be skipped at the moment
    # col 2: Title: testacase name
    # col 3: Description: Preconditions, Steps
    # col 4: Expected result
    """
    Path = 'Testcases/'
    FileName = 'TmbieTV_tcs_short.xlsx'
    File = Path + FileName
    Sheet = 'Test Cases'
    OutFile = '9testcases1.xml'

    Row_Top = 0
    Row_Title = 1
    Row_Suite_start = 2
    Row_Testcase = '^P\d$'

    Row_Type_TC = 'TC' 
    Row_Type_TS = 'TS' 
    
    Col_TestPlan = 0
    Col_TestSuite = 0
    Col_TC_ID = 1
    Col_TC_title = 2
    Col_TC_Desc = 3
    Col_TC_Expt = 4

class ATTFamilyMap_Schema(object):
    """
    Constants for ATT Family Map in CSV file 
    # col 0: ID
    # col 1: Title
    # col 2: Preconditions
    # col 3: Steps
    # col 4: Expected Result
    """
    Path = 'Testcases/'
    FileName = 'ATTFamilyMap.csv'
    File = Path + FileName
    OutFile = 'Attfamilymapsample2.xml'

    Row_Top = 0
    Row_Suite_start = 1

    Col_TestSuite = 'ATT Family Map'

    Col_TC_ID = 0
    Col_TC_Title = 1
    Col_TC_Precon = 2
    Col_TC_Steps = 3
    Col_TC_Expt = 4
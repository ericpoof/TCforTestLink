'''
Created on Jul 9, 2013

@author: Eric
'''

## Schema mapping xls to testlink xml

# SCHEMA
# col 0: Test Suit: Top, P[1..9] : testcase, XXX : Testsuite name 
# col 1: id: can be skipped at the moment
# col 2: Title: testacase name
# col 3: Description: Preconditions, Steps
# col 4: Expected result
# col 5: 

class TMOTV_Schema(object):
    Row_Top = 0
    Row_Title = 1
    Row_Suite_start = 2
    Row_Suite = '^P\d$'

    Row_Type_TC = 10
    Row_Type_TS = 11
    
    Col_TestPlan = 0
    Col_TestSuite = 0
    Col_TC_ID = 1
    Col_TC_title = 2
    Col_TC_Desc = 3
    Col_TC_Expt = 4
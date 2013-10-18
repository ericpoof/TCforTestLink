'''
Created on Jul 9, 2013

@author: Eric
'''

## Schema mapping to testlink xml

class PLM_Schema(object):
    """
    Constants for PLM in Excel Spreadsheet 
    # col 0: Project Name 
    # col 1: Model Name
    # col 2: Product code
    # col 3: Case Code
    # col 4: Title
    # col 5: Status
    # col 6: Problem Type
    # col 7: Problem
    # col 8: Reproduction steps
    # col 9: Comment
    # col 10: Cause
    # col 11: Countermeasure
    """
    Path = 'Testcases/'

    Row_Top = 0
    Row_Title = 1
    Row_Suite_start = 2
    Row_Testcase = '^P\d$'

    Row_Type_TC = 'TC' 
    Row_Type_TS = 'TS' 
    
    Col_ProjectName = 0
    Col_ModelName = 1
    Col_ProductCode = 2
    Col_Casecode = 3
    Col_Title = 4
    Col_Status = 5
    Col_ProblemType = 6
    Col_Problem = 7
    Col_Reproduction = 8
    Col_Comment = 9
    Col_Cause = 10
    Col_Countermeasure = 11


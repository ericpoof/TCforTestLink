'''
Created on Jul 9, 2013

@author: Eric
'''

## Schema mapping xls to testlink xml
## Another one?
class TMOTV_Schema():
    Row_Top = 0
    Row_Title = 1
    Row_Suite = '^P\d$'
    
    Col_TestPlan = 0
    Col_TC_ID = 1
    Col_TC_title = 2
    Col_TC_Desc = 3
    Col_TC_Expt = 4
'''
Created on Jul 12, 2013

@author: Eric
'''

# 
# Quick way to test Python regex 
# http://pythex.org/

class TMO_TV(object):
    steps = '(\d\.)(.*)'
    precondition = '(Preconditions:)([a-zA-Z\s\'-\.]*)(?=step)'
    ### group(0): whole match, group(1): first group, group(2): 2nd group  
    sel_subgroup = 2
    

class ATT_FamilyMap(object):
    steps = '(\d\.)(.*)'
    sel_subgroup = 2


class ATT_Lookout(object):
    Title = '^QE'
    Test_Step = '^\d'
    Continue = '^\*'
    NoData = '^\@'
    Newline = '<\b>'
    
    TS = '^Test Step'
    TD = '^Test Data'
    EX = '^Expected'
    CR = '^\n'
    
    

    




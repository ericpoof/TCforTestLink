'''
Created on Jul 17, 2013

@author: Eric
'''


class TestSuite(object):
    def __init__(self):
        self.name = ''
        self.details = ''
        self.testcases = []
        
class TestCase(object): 
    def __init__(self):
        ## S.Col_TC_title
        self.name = ''
        ## external id
        self.externalId = ''
        ## S.Col_TC_Desc
        self.preconditions = ''
        self.steps = []


class Step(object):
    def __init__(self):
        ## retrieved from S.Col_TC_Desc
        self.step_number = 1
        self.actions = ''
        ## S.Col_TC_Expt
        self.expectedresults = ''
        ## Fixed to manual
        self.execution_type = 1

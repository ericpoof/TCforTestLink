'''
Created on Jul 17, 2013

@author: Eric
'''

import re
# from tcPattern import TMO_TV
from tcPattern import ATT_FamilyMap
# from schema import TMOTV_Schema as S 
from schema import ATTFamilyMap_Schema as AF
from testSuite import TestSuite, TestCase, Step


class CellParser(object):
    def __init__(self, xlsData):
        self.xlsData = xlsData
    
    def parseRows(self, no_parsing_rows):

        # Top-level testsuite aggregator
        testsuites = []
        # dummy object assignment to rule out adding testsuite at first time
        ts = TestSuite()
        ts.name = AF.Col_TestSuite
        ### details
        ts.details = ''

        ### testcases
        ts.testcases = []

        ## Looping in rows
        for i in range(AF.Row_Suite_start, no_parsing_rows):
            row = self.xlsData.getRow(i)
            tc = self.mapRow2TC(row)
            ts.testcases.append(tc)
        testsuites = [ts]

        ## The end result before passing to #3 XmlTree converter
        return testsuites

    def printTestSuites(self, testsuites):
        for ts in testsuites:
            print 'testsuite name is ', ts.name
            print ' beginning of testcases'
            for idx, tc in enumerate(ts.testcases):
                print 'testcase name is' , idx+1, tc.name
                print 'testsuite ID is ', tc.externalId
                print 'testcase precon is' , tc.preconditions
                for step in tc.steps:
                    print 'step=', step.step_number, ' :' , step.actions
                    if step.step_number == len(tc.steps):
                        print 'expected =', step.expectedresults


    def mapRow2TC(self, row):
            tc = TestCase()
            tc_title =  row[AF.Col_TC_Title].cell_value
            tc_desc =  row[AF.Col_TC_Steps].cell_value
            tc_expt =  row[AF.Col_TC_Expt].cell_value
            tc_extId = row[AF.Col_TC_ID].cell_value

            patClass = ATT_FamilyMap()
            parsedSteps = self.parseSteps(patClass, tc_desc)

            ## b. Filling out TestCase()
            ### name & Id
            tc.name = tc_title
            tc.externalId = tc_extId

            ### preconditions
#             tc.preconditions = parsedSteps['precon']
            tc.preconditions = row[AF.Col_TC_Precon].cell_value 
            print ' preconditions' , tc.preconditions

            ### steps
            steps = parsedSteps['steps']
            print ' steps' , steps


            ## c. Filling out Step()
            for idx,st in enumerate(steps):
                ### new Step object on each element of a list
                step = Step()
                ### step_number 
                step.step_number = idx + 1
                ### actions 
                step.actions = st
                ### expectedresults 
                if (idx + 1) == len(steps):
                    step.expectedresults = tc_expt
                ### append Step object to TestCase steps list
                tc.steps.append(step)
            
            ## return TestCase() object
            return tc
                

    def parseSteps(self, patClass, str):
            # regex compile
            steps_pat = re.compile(patClass.steps, re.I)
            
            m = steps_pat.match(str)

            steps = []
            # regex finditer and Match object group(#)
            if m:
                for step in steps_pat.finditer(str):
                    print 'step = ', step.group(patClass.sel_subgroup)
                    step = step.group(patClass.sel_subgroup)
                    steps.append(step)
            else:
                step = str
                steps.append(step)


            return {'steps':steps}


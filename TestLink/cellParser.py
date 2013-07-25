'''
Created on Jul 17, 2013

@author: Eric
'''

import re
from tcPattern import TMO_TV
from schema import TMOTV_Schema as S 
from testSuite import TestSuite, TestCase, Step


class CellParser(object):
    def __init__(self, xlsData):
        self.xlsData = xlsData
    
    def parseRows(self, no_parsing_rows):

        # Top-level testsuite aggregator
        testsuites = []
        # dummy object assignment to rule out adding testsuite at first time
        ts = object() 

        ## Looping in rows
        for i in range(S.Row_Suite_start, no_parsing_rows):
            row = self.xlsData.getRow(i)
            row_type = self.xlsData.getRowType(row)
            print 'row type = ', self.xlsData.getRowType(row)

            ## To decide if testsuite or individual testcase
            if row_type is S.Row_Type_TS:  
                if i != S.Row_Suite_start:
                    testsuites.append(ts)
                ts = TestSuite()
                ## a. Filling out TestSuite()
                ### name
                ts.name = row[S.Col_TestSuite].cell_value 
    
                ### details
                ts.details = ''
    
                ### testcases
                ts.testcases = []
            else:
                tc = self.mapRow2TC(row)
                ts.testcases.append(tc)
                if i == no_parsing_rows - 1:
                    testsuites.append(ts)

        ## The end result before passing to #3 XmlTree converter
        return testsuites

    def printTestSuites(self, testsuites):
        for ts in testsuites:
            print 'testsuite name is ', ts.name
            print ' beginning of testcases'
            for tc in ts.testcases:
                print 'testcase name is' , tc.name
                print 'testcase precon is' , tc.preconditions
                for step in tc.steps:
                    print 'step=', step.step_number, ' :' , step.actions
                    if step.step_number == len(tc.steps):
                        print 'expected =', step.expectedresults


    def mapRow2TC(self, row):
            tc = TestCase()
            tc_title =  row[S.Col_TC_title].cell_value
            tc_desc =  row[S.Col_TC_Desc].cell_value
            st_expt =  row[S.Col_TC_Expt].cell_value

            patClass = TMO_TV()
            parsedDesc = self.parseSteps(patClass, tc_desc)

            ## b. Filling out TestCase()
            ### name
            tc.name = tc_title
            ### preconditions
            tc.preconditions = parsedDesc['precon']
            print ' parsedDesc preconditions' , tc.preconditions

            ### steps
            steps = parsedDesc['steps']
            print ' parsedDesc steps' , steps


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
                    step.expectedresults = st_expt
                ### append Step object to TestCase steps list
                tc.steps.append(step)
            
            ## return TestCase() object
            return tc
                

    def parseSteps(self, patClass, str):
            # regex compile
            precondition_pat = re.compile(patClass.precondition, re.I)
            steps_pat = re.compile(patClass.steps, re.I)

            print 'description=', str
            print '----------------------------------------------------'

            # regex search
            precondition_match = precondition_pat.search(str)
            if precondition_match:
                precondition = precondition_match.group(patClass.sel_subgroup)
                print 'precondition_match =', precondition_match.group(patClass.sel_subgroup)
            else:
                precondition = ''
                print 'precondition_match is None'

            steps = []
            # regex finditer and Match object group(#)
            for step in steps_pat.finditer(str):
                print 'step = ', step.group(patClass.sel_subgroup)
                step = step.group(patClass.sel_subgroup)
                steps.append(step)
            print '----------end---------------------------------------'
            return {'precon':precondition, 'steps':steps}


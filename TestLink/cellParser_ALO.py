'''
Created on Jul 17, 2013

@author: Eric
'''

import re
# from tcPattern import TMO_TV
from tcPattern import ATT_FamilyMap
# from schema import TMOTV_Schema as S 
from schema import ATTLookout_Schema as AL
from tcPattern import ATT_Lookout as reAL
from testSuite import TestSuite, TestCase, Step
from collections import deque
from _pydev_xmlrpclib import escape


class CellParser(object):
    def __init__(self):
        self.content = []
        self.noTC = 0
        self.steps_queue = deque('',maxlen=15)
        self.data_queue = deque('',maxlen=15)
        self.expt_queue = deque('',maxlen=15)

    def readTextMD(self, file):
        """
        ATT Lookout
        create self.cellArr list of CellExl(s)
        @param file: custom markdown textfile
        @type file: str
        """
        with open(file) as f:
            self.content = f.readlines()


    def createTestCase(self, tc):
        if len(self.steps_queue) != 0 and (len(self.data_queue) == len(self.expt_queue)):
            print '============= testcase ended====================='
            # sanity check
            if len(self.steps_queue) != len(self.data_queue):
                print 'Mismatch in steps and data'
                print 'len self.steps_queue', len(self.steps_queue)
                print 'len self.data_queue', len(self.data_queue) # Need to combine self.steps_queue and self.data_queue
            for i in range(len(self.steps_queue)):
                st = Step()
                st.step_number = i+1
                data_tmp = self.data_queue.popleft()
                if data_tmp == '':
                    st.actions = self.steps_queue.popleft() 
                else:
                    st.actions = self.steps_queue.popleft() + '</br>' + ' precondition: ' + data_tmp
                print '--- actions = ', st.actions
                st.expectedresults = self.expt_queue.popleft()
                tc.steps.append(st)
                print '---Expt = ', st.expectedresults
            
            self.noTC = self.noTC + 1
            print 'Total testcases = ', self.noTC
            self.steps_queue = deque('', maxlen=15)
            self.data_queue = deque('', maxlen=15)
            self.expt_queue = deque('', maxlen=15)
        return tc 

    def parseRows(self):
        '''
        Main API exposed outside
        :param no_parsing_rows:
        '''

        # Top-level testsuite aggregator
        testsuites = []
        # dummy object assignment to rule out adding testsuite at first time
        ts = TestSuite()
        ts.name = AL.Col_TestSuite
        ### details
        ts.details = ''

        ### testcases
        ts.testcases = []

        re_title = re.compile(reAL.Title, re.I)
        re_steps = re.compile(reAL.Test_Step, re.I)
        re_cont = re.compile(reAL.Continue, re.I)
        re_ts = re.compile(reAL.TS, re.I)
        re_td = re.compile(reAL.TD, re.I)
        re_ex = re.compile(reAL.EX, re.I)
        re_cr = re.compile(reAL.CR, re.I)
        re_eof = re.compile(reAL.EOF, re.I)
        re_none = re.compile(reAL.NoData, re.I)
        nline = reAL.Newline

        ## Looping in rows
        
        flag_tc = False
        flag_st = False
        flag_dt = False
        flag_ex = False
        
        tc_no = 0
        prev =''
        
        for i in range(8, len(self.content)):
            row = self.content[i]
            print ' -------'
            print ': Row = ' , row
            if re_title.match(row):            # QE
                m = re_title.match(row)
                print '=> title row'
                tc = TestCase()
                tc.name = prev
#                 tc.name = m.group(2)
                flag_ex = False
                flag_tc = True
                tc_no = tc_no + 1
                
                # delay processing by one
                if tc_no!=1:
                    tc = self.createTestCase(tc)
                    ts.testcases.append(tc)
                prev = m.group(0)


            elif re_ts.match(row):             # Test Step 
                print '=> Test Step'
                flag_tc = False
                flag_st = True
            elif re_steps.match(row):          # 1 xxx 
                print '=> steps row'
                m = re_steps.match(row)
                self.steps_queue.append(m.group(2))
            elif re_td.match(row):             # Test Data 
                print '=> Test Data'
                flag_st = False
                flag_dt = True
            elif re_cont.match(row):           # *xxx
                m = re_cont.match(row)
                row_s = m.group(2)
                print '=> continued'
                if flag_st:
                    contd = self.steps_queue.pop() + nline + row_s
                    self.steps_queue.append(contd)
                if flag_dt:
                    contd = self.data_queue.pop() + nline + row_s
                    self.data_queue.append(contd)
                if flag_ex:
                    contd = self.expt_queue.pop() + nline + row_s
                    self.expt_queue.append(contd)
            elif re_none.match(row):           # @NoData 
                print '=> no data'
                if flag_dt:
                    self.data_queue.append('')
                if flag_ex:
                    self.expt_queue.append('')
            elif re_ex.match(row):             # Expected Result 
                print '=> Expected Result'
                flag_dt = False
                flag_ex = True
            elif re_cr.match(row):             # \n 
                print '=> newline'
            elif re_eof.match(row):            # EOF
                print 'Total no of testcases = ', tc_no
                tc = self.createTestCase(tc)
                ts.testcases.append(tc)
            else:                              # item for data/expected
                print '=> data/expected item'
                if flag_tc:
                    tc.name = tc.name + row
                if flag_dt:
                    self.data_queue.append(row)
                if flag_ex:
                    self.expt_queue.append(row)
        return ts
             

    def printTestSuites(self, testsuites):
        for ts in testsuites:
            print 'testsuite name is ', ts.name
            print ' beginning of testcases'
            for idx, tc in enumerate(ts.testcases):
                print 'testcase name is' , idx+1, tc.name
#                 print 'testsuite ID is ', tc.externalId
                print 'testcase precon is' , tc.preconditions
                for step in tc.steps:
                    print 'step=', step.step_number, ' :' , step.actions
                    if step.step_number == len(tc.steps):
                        print 'expected =', step.expectedresults


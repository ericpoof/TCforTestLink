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


class CellParser(object):
    def __init__(self):
        self.content = []
        self.noTC = 0
        self.noCont = 0
        self.noData = 0

    def readTextMD(self, file):
        """
        ATT Lookout
        create self.cellArr list of CellExl(s)
        @param file: custom markdown textfile
        @type file: str
        """
        with open(file) as f:
            self.content = f.readlines()


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
        steps_queue = deque('',maxlen=15)
        data_queue = deque('',maxlen=15)
        expt_queue = deque('',maxlen=15)
        
        flag_tc = False
        flag_st = False
        flag_dt = False
        flag_ex = False
        
        tc_no = 0
        
        for i in range(8, len(self.content)):
            row = self.content[i]
#             self.mapRow2TC(row, steps_queue, data_queue, expt_queue)
            print ' -------'
            print ': Row = ' , row
            if re_title.match(row):            # QE
                print '=> title row'
                tc = TestCase()
                tc.title = row
                flag_ex = False
                flag_tc = True
                tc_no = tc_no + 1
                st_no = 0
                
                if len(steps_queue) !=0 and (len(data_queue) == len(expt_queue)):
                    print '============= testcase ended====================='
                    flag_ex = False
                    # sanity check
                    if len(steps_queue) != len(data_queue):
                        print 'Mismatch in steps and data'
                        print 'len steps_queue', len(steps_queue)
                        print 'len data_queue', len(data_queue)
                    # Need to combine steps_queue and data_queue
                    for i in range(len(steps_queue)):
                        st = Step()
                        st.actions = steps_queue.popleft() + ':' + data_queue.popleft()
                        print '--- actions = ', st.actions
                        st.expectedresults = expt_queue.popleft()
                        print '---Expt = ', st.expectedresults
                    
                    self.noTC = self.noTC + 1
                    self.noData = self.noData + 1
                    self.noCont = self.noCont + 1
                    print 'noTC from noData', self.noData
                    print 'noTC from noCont', self.noCont
                    print 'Total testcases = ', self.noTC
                    steps_queue = deque('', maxlen=15)
                    data_queue = deque('', maxlen=15)
                    expt_queue = deque('', maxlen=15)

            elif re_ts.match(row):             # Test Step 
                print '=> Test Step'
                flag_tc = False
                flag_st = True
            elif re_steps.match(row):          # 1 xxx 
                print '=> steps row'
                steps_queue.append(row)
            elif re_td.match(row):             # Test Data 
                print '=> Test Data'
                flag_st = False
                flag_dt = True
            elif re_cont.match(row):           # *xxx
                print '=> continued'
                if flag_st:
                    contd = steps_queue.pop() + row
                    steps_queue.append(contd)
                if flag_dt:
                    contd = data_queue.pop() + row
                    data_queue.append(contd)
                if flag_ex:
                    contd = expt_queue.pop() + row
                    expt_queue.append(contd)
            elif re_none.match(row):           # @NoData 
                print '=> no data'
                if flag_dt:
                    data_queue.append('')
                if flag_ex:
                    expt_queue.append('')
            elif re_ex.match(row):             # Expected Result 
                print '=> Expected Result'
                flag_dt = False
                flag_ex = True
            elif re_cr.match(row):             # \n 
                print '=> newline'
            elif re_eof.match(row):            # EOF
                print 'Total no of testcases = ', tc_no
                if len(steps_queue) !=0 and (len(data_queue) == len(expt_queue)):
                    print '============= testcase ended====================='
                    flag_ex = False
                    # sanity check
                    if len(steps_queue) != len(data_queue):
                        print 'Mismatch in steps and data'
                        print 'len steps_queue', len(steps_queue)
                        print 'len data_queue', len(data_queue)
                    # Need to combine steps_queue and data_queue
                    for i in range(len(steps_queue)):
                        st = Step()
                        st.actions = steps_queue.popleft() + ':' + data_queue.popleft()
                        print '--- actions = ', st.actions
                        st.expectedresults = expt_queue.popleft()
                        print '---Expt = ', st.expectedresults
                    
                    self.noTC = self.noTC + 1
                    self.noData = self.noData + 1
                    self.noCont = self.noCont + 1
                    print 'noTC from noData', self.noData
                    print 'noTC from noCont', self.noCont
                    print 'Total testcases = ', self.noTC
                    steps_queue = deque('', maxlen=15)
                    data_queue = deque('', maxlen=15)
                    expt_queue = deque('', maxlen=15)
            else:                              # item for data/expected
                print '=> data/expected item'
                if flag_tc:
                    tc.title = tc.title + row
                if flag_dt:
                    data_queue.append(row)
                if flag_ex:
                    expt_queue.append(row)
             

#         testsuites = [ts]

        ## The end result before passing to #3 XmlTree converter
#         return testsuites                        
                        
                        
#     def mapRow2TC(self, row, steps_queue, data_queue, expt_queue):


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


'''
Created on Jul 1, 2013

@author: me.jung
'''

import xlrd
import re
from tcPattern import TMO_TV
from schema import TMOTV_Schema as S 
from test.test_iterlen import len

# SCHEMA
# col 0: Test Suit: Top, P[1..9] : testcase, XXX : Testsuite name 
# col 1: id: can be skipped at the moment
# col 2: Title: testacase name
# col 3: Description: Preconditions, Steps
# col 4: Expected result
# col 5: 

class REMatcher(object):
    def __init__(self, matchstring):
        self.matchstring = matchstring

    def match(self,regexp):
        self.rematch = re.match(regexp, self.matchstring)
        return bool(self.rematch)

    def group(self,i):
        return self.rematch.group(i)

m = REMatcher("tmp");

## 1
class XlsData(object):
    def __init__(self):
        self.cellArr = []
    def append(self, cell):
        self.cellArr.append(cell)
    def printXlsData(self):
        for cell in self.cellArr:
            cell.printCell()
    def getRowLength(self):
        cellArrLeng = len(self.cellArr)
        lastCell = self.cellArr[cellArrLeng -1]
        return lastCell.row_no + 1
    def getColLength(self):
        cellArrLeng = len(self.cellArr)
        lastCell = self.cellArr[cellArrLeng -1]
        return lastCell.col_no + 1
    def getRow(self, idx):
        start = idx*self.getColLength() 
        end = (idx+1)*self.getColLength() 
        return self.cellArr[start:end]
    def getRowType(self,row):
        tp_pattern = re.compile(S.Row_Suite)
        print 'cell_value =' ,row[S.Col_TestPlan].cell_value
        if tp_pattern.search(row[S.Col_TestPlan].cell_value) is None:
            print 'testsuite'
            return S.Row_Type_TS
        else:
            print 'testcase'
            return S.Row_Type_TC


    def tcType(self):
        for cell in self.cellArr:
            if cell.col_no == 0:
                #if re.search('^(Test Suit)', cell_value) is not None:
                if re.match('Test Suit', cell.cell_value) is not None:
                    return 'Top'
        #        if re.search('^P\d$', cell_value) is not None:
                if re.match('P\d$', cell.cell_value) is not None:
                    return 'testcase'
                return 'testsuite'
        
            if cell.col_no == 2:
                if cell.cell_value == '':
                    return 'None'
                if re.match('Title', cell.cell_value) is not None:
                    return 'Title'
                return cell.cell_value;
        
            # todo: parse Test Description into preconditions/steps 
            if cell.col_no == 3:
                pass
        
            # toda: parse Expected result
            if cell.col_no == 4:
                pass



class CellExl(object):
    def __init__(self, row_no, col_no, cell_value):
        self.row_no = row_no
        self.col_no =  col_no
        self.cell_value = cell_value
    def printCell(self):
        print self.row_no, self.col_no, self.cell_value
        
    

## 1-2
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
            parsedDesc = self.parseDesc(patClass, tc_desc)

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
                

    def parseDesc(self, patClass, str):
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


## 2
class TestSuite(object):
    def __init__(self):
        self.name = ''
        self.details = ''
        self.testcases = []

class TestCase(object): 
    def __init__(self):
        ## S.Col_TC_title
        self.name = ''
        ## S.Col_TC_Desc
        self.preconditions = []
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
        
## 3
# class XmlTree(object):
#     def __init__(self):
#         self.testsuite = Element('testsuite')

def get_tcTag(col_no, cell_value):
    if col_no == 0:
        #if re.search('^(Test Suit)', cell_value) is not None:
        if re.match('Test Suit', cell_value) is not None:
            return 'Top'
#        if re.search('^P\d$', cell_value) is not None:
        if re.match('P\d$', cell_value) is not None:
            return 'testcase'
        return 'testsuite'

    if col_no == 2:
        if cell_value == '':
            return 'None'
        if re.match('Title', cell_value) is not None:
            return 'Title'
        return cell_value;

    if col_no == 3:
        pass

    if col_no == 4:
        pass

    return 'none'

def tcData():
    pass

def readXLS():
    ## 0. read a spreadsheet with xlrd module
    workbook = xlrd.open_workbook('TmbieTV_tcs_short.xlsx')
    worksheet = workbook.sheet_by_name('Test Cases')
    num_rows = worksheet.nrows - 1
    num_cells = worksheet.ncols - 1
    
    ## 1st stage handling spreadsheet data
    xlsData = XlsData()
    curr_row = -1
    while curr_row < num_rows:
        curr_row += 1
        row = worksheet.row(curr_row)
        print 'Row:', curr_row
        curr_cell = -1
        while curr_cell < num_cells:
            curr_cell += 1
            ## Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
            cell_type = worksheet.cell_type(curr_row, curr_cell)
            cell_value = worksheet.cell_value(curr_row, curr_cell)
            ## Class XlsData operation with CellExl
            cell = CellExl(curr_row, curr_cell, cell_value);
            xlsData.append(cell)
            ## 
            print '    ', cell_type, ':', (curr_row, curr_cell), cell_value
            print get_tcTag(curr_cell, cell_value)
    print '------CLASS----------------------------------'
    print ' #1 step'
    ## xlsData.printXlsData()
    print 'row length = ', xlsData.getRowLength()
    print 'column length = ', xlsData.getColLength()
    
     
    ## 2nd stage after getting xlsData

    cellParser = CellParser(xlsData)

    ## pass no of rows to parse

    no_rows = xlsData.getColLength()
    testsuites = cellParser.parseRows(no_rows)
    print '-------------------------------------'
    print 'printing testsuites'
    print '-------------------------------------'
    cellParser.printTestSuites(testsuites)

    ## 3rd stage after getting testsuites


def buildTestSuite(xlsData):
    pass


if __name__ == '__main__':
    readXLS()

'''
Created on Jul 1, 2013

@author: me.jung
'''

import xlrd
import re
from xml.etree.ElementTree import Element
from TC_Pattern import TMO_TV
from Schema import TMOTV_Schema as S 

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
class XlsData():
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



class CellExl():
    def __init__(self, row_no, col_no, cell_value):
        self.row_no = row_no
        self.col_no =  col_no
        self.cell_value = cell_value
    def printCell(self):
        print self.row_no, self.col_no, self.cell_value
        
    

## 1-2
class CellParser():
    def __init__(self, xlsData):
        self.xlsData = xlsData
    def parseRows(self):
        colLeng = self.xlsData.getColLength()
        # Looping in rows
        for i in range(2, colLeng):
            tc = TestCase()
            row = self.xlsData.getRow(i)
            # print ' row = ', row[S.Col_TC_Desc].cell_value
            title =  row[S.Col_TC_title].cell_value
            desc =  row[S.Col_TC_Desc].cell_value
            expt =  row[S.Col_TC_Expt].cell_value
            tc.name = title
            self.parseDesc(desc)

    def parseDesc(self, str):
        pass


## 2
class TestSuite():
    def __init__(self):
        self.name = ''
        self.details = ''
        self.testcases = []

class TestCase(): 
    def __init__(self):
        self.name = ''
        self.steps = []
        
class Step():
    def __init__(self):
        self.step_number = 1
        self.actions = ''
        self.expectedresults = ''
        self.execution_type = 1
        
## 3
class XmlTree():
    def __init__(self):
        self.testsuite = Element('testsuite')

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
    workbook = xlrd.open_workbook('TmbieTV_tcs_short.xlsx')
    worksheet = workbook.sheet_by_name('Test Cases')
    num_rows = worksheet.nrows - 1
    num_cells = worksheet.ncols - 1
    xlsData = XlsData()
    curr_row = -1
    while curr_row < num_rows:
        curr_row += 1
        row = worksheet.row(curr_row)
        print 'Row:', curr_row
        curr_cell = -1
        while curr_cell < num_cells:
            curr_cell += 1
            # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
            cell_type = worksheet.cell_type(curr_row, curr_cell)
            cell_value = worksheet.cell_value(curr_row, curr_cell)
            #### Class XlsData operation with CellExl
            cell = CellExl(curr_row, curr_cell, cell_value);
            xlsData.append(cell)
            #### 
            print '    ', cell_type, ':', (curr_row, curr_cell), cell_value
            print get_tcTag(curr_cell, cell_value)
    print '------CLASS----------------------------------'
    print ' #1 step'
    # xlsData.printXlsData()
    print 'row length = ', xlsData.getRowLength()
    print 'column length = ', xlsData.getColLength()
    cellParser = CellParser(xlsData)
    cellParser.parseRows()

def buildTestSuite(xlsData):
    pass


if __name__ == '__main__':
    readXLS()

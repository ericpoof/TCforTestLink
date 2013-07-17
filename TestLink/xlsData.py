'''
Created on Jul 17, 2013

@author: Eric
'''
import re
import xlrd
from schema import TMOTV_Schema as S 

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


    def get_tcTag(self, col_no, cell_value):
        """
        deprecated
        """
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
        
    def readXls(self):
        ## 0. read a spreadsheet with xlrd module
        workbook = xlrd.open_workbook('TmbieTV_tcs_short.xlsx')
        worksheet = workbook.sheet_by_name('Test Cases')
        num_rows = worksheet.nrows - 1
        num_cells = worksheet.ncols - 1
        
        ## 1st stage handling spreadsheet data
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
                self.append(cell)
                ## 
                ##print '    ', cell_type, ':', (curr_row, curr_cell), cell_value
                ##print get_tcTag(curr_cell, cell_value)
        print '------CLASS----------------------------------'
        print ' #1 step'
        ## xlsData.printXlsData()
        print 'row length = ', self.getRowLength()
        print 'column length = ', self.getColLength()
        
class CellExl(object):
    def __init__(self, row_no, col_no, cell_value):
        self.row_no = row_no
        self.col_no =  col_no
        self.cell_value = cell_value
    def printCell(self):
        print self.row_no, self.col_no, self.cell_value
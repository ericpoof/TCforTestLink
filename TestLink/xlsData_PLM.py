'''
Created on Jul 17, 2013

@author: Eric
'''
import xlrd

class XlsData(object):
    Debug = False
    def __init__(self):
        """
        array of CellExl()
        """
        self.cellArr = []

    def append(self, cell):
        self.cellArr.append(cell)
        
    def getCells(self):
        return self.cellArr

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
        
    def readXls(self, file, sheet):
        """
        TMO TV
        create self.cellArr list of CellExl(s)
        @param file: workdbook name
        @type file: str
        @param sheet: sheet name
        @type sheet: str
        """
        ## 0. read a spreadsheet with xlrd module
        workbook = xlrd.open_workbook(file)
        worksheet = workbook.sheet_by_name(sheet)
        num_rows = worksheet.nrows - 1
        num_cells = worksheet.ncols - 1
        
        ## 1st stage handling spreadsheet data
        curr_row = -1
        while curr_row < num_rows:
            curr_row += 1
            row = worksheet.row(curr_row)
            #print 'Row:', curr_row
            curr_cell = -1
            while curr_cell < num_cells:
                curr_cell += 1
                ## Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                cell_type = worksheet.cell_type(curr_row, curr_cell)
                cell_value = worksheet.cell_value(curr_row, curr_cell)
                ## Class XlsData operation with CellExl
                cell = CellExl(curr_row, curr_cell, cell_value.encode('utf-8'));
                self.append(cell)
                ## 
                ##print '    ', cell_type, ':', (curr_row, curr_cell), cell_value
                ##print get_tcTag(curr_cell, cell_value)
        #print '------CLASS----------------------------------'
        #print ' #1 step'
        ## xlsData.printXlsData()
        #print 'row length = ', self.getRowLength()
        #print 'column length = ', self.getColLength()
    
    def readCsv(self, file):
        """
        ATT Family Map
        create self.cellArr list of CellExl(s)
        @param file: CSV name
        @type file: str
        """

        import csv, sys

        reader = csv.reader(open(file, "rb"))
        try:
            for idx_row, row in enumerate(reader):
                if XlsData.Debug:
                    print 'tittle = ',idx_row,  row[1]
                    print  'precon = ', row[2]
                    print  'steps = ', row[3]
                    print  'expected = ', row[4]
                for idx_col, col in enumerate(row):
                    cell = CellExl(idx_row, idx_col, col)
                    self.append(cell)
#                     print 'cell = ', idx_row, idx_col, col
        except csv.Error, e:
            sys.exit('file %s, line %d: %s' % (file, reader.line_num, e))

class CellExl(object):
    def __init__(self, row_no, col_no, cell_value):
        self.row_no = row_no
        self.col_no =  col_no
        self.cell_value = cell_value
    def printCell(self):
        print self.row_no, self.col_no, self.cell_value
        
        
        
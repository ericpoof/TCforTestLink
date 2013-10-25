'''
Created on Oct 17, 2013

@author: Eric
'''

# 
# Quick way to test Python regex 
# http://pythex.org/

import re
import xlwt
import sys
sys.path.append('/Users/Eric/Documents/workspace/TCforTestLink/TestLink')
from xlsData_PLM import XlsData
from schemaPLM import PLM_Schema as Pcell

traversingCells = [ Pcell.Col_Title, Pcell.Col_Problem, Pcell.Col_Reproduction, \
                   Pcell.Col_Cause, Pcell.Col_Countermeasure ]

def main():
    
    # 1. read a template file for app search patterns and create a list of app patterns 
    filename = '/Users/Eric/Documents/workspace/TCforTestLink/TestLink/TmoApps.txt'
    with open(filename, 'r') as the_file:
        appList = the_file.readlines()
        
    
    allApps = []
    for idx, line in enumerate(appList):
        preloadApp = PreloadApp()
        appInfoList = line.split(':')
        preloadApp.name = appInfoList[0].strip()
        preloadApp.pattern = appInfoList[1].strip()
        allApps.append(preloadApp)
    
#     for app in allApps:
#         print 'name =', app.name, '  pattern = ', app.pattern
   
    # 2. read a excel file and create cell data CellExl()
    absolutePath = '/Users/Eric/Documents/workspace/TCforTestLink/TestLink/'
    xlsLocalFile = 'Testcases/Garda_issues_1015.xls'
    xlsFile = absolutePath + xlsLocalFile
    worksheet = 'DEFECT'
    
    xlsData = XlsData()
    xlsData.readXls(xlsFile, worksheet)
#     xlsData.printXlsData()
    
    # 3. traverse chosen cells and search for patterns
    # TODO: better be flexible by getting user input 
    
#     print '                                 '
#     print ' ==== PLM issues app breakdown ===== '
#     print '                                 '

    prettyForm = "testText"
    filename = absolutePath + "convertedXL.txt"
    outfile = open(filename, 'w') 
    outfile.write(prettyForm)
    
    traversingCells = [ Pcell.Col_Title, Pcell.Col_Problem, Pcell.Col_Reproduction, \
                   Pcell.Col_Cause, Pcell.Col_Countermeasure ]

    rowlen = xlsData.getRowLength()
    rowflag = [False]*rowlen
    for cell in xlsData.getCells():
            if cell.col_no in traversingCells:
    #             print 'row = ', cell.row_no, ' col = ', cell.col_no, ' value = ', cell.cell_value
                for app in allApps:
#                     print 'cell_value to match' , app.pattern, ': ' , cell.cell_value
                    appRe = re.compile(app.pattern, re.I)
#                     print appRe.search(cell.cell_value)
                    if appRe.search(cell.cell_value) is not None:
                        if not rowflag[cell.row_no]:
                            rowflag[cell.row_no] = True
#                             print 'row = ', cell.row_no, ' is ' , app.name , ' issue: ' 
#                         print 'cell_value to match' , app.pattern, ': ' , cell.cell_value
#     print '                                 '
#     print ' ==== PLM issues not classfied ===== '
#     print '                                 '

    noClass = []
    for idx, row in enumerate(rowflag):
        if not row:
#             notClassfied = 'row = ', row, '' , idx, ' cannot be determined which app it is\n' 
            notClassfied = idx
            noClass.append(notClassfied) 
            outfile.writelines(str(notClassfied))
    print noClass 
    
    # 4. create a spreadsheet based on matching lists
    traversingCells = [ Pcell.Col_Title, Pcell.Col_Problem, Pcell.Col_Reproduction, \
                       Pcell.Col_Cause, Pcell.Col_Countermeasure ]
#     hdngsNo =  traversingCells
    hdngsNo =  traversingCells.insert(0, Pcell.Col_Casecode)
    hdngsNo = [ Pcell.Col_Casecode, Pcell.Col_Title, Pcell.Col_Problem, Pcell.Col_Reproduction, \
                       Pcell.Col_Cause, Pcell.Col_Countermeasure ]
    print "Hello"
    print hdngsNo
    ## Looping in rows to get a row with selected index
    rowData = []
    for i in range(0, xlsData.getRowLength()):
        row = xlsData.getRow(i)
        newRow = []
        for colSel in hdngsNo:
            newRow.append(row[colSel])
        rowData.append(newRow)
    print rowData
#      
    create_xls(rowData)
    

class PreloadApp(object): 
    def __init__(self):
        ## app name
        self.name = ''
        ## search pattern
        self.pattern = ''    


def write_xls(file_name, sheet_name, headings, data, data_xfs, col_width):
    ezxf = xlwt.easyxf
    heading_xf = ezxf('font: bold on; align: wrap on, vert centre, horiz center;  \
                     pattern: pattern solid, fore-colour yellow; \
                     borders: left thin, right thin, top thin, bottom thin;' \
                     )
    book = xlwt.Workbook()
    sheet = book.add_sheet(sheet_name, cell_overwrite_ok=True)
#     sheet = book.add_sheet(sheet_name)
    rowx = 0
    for colx, value in enumerate(headings):
        sheet.write(rowx, colx, value, heading_xf)
    sheet.set_panes_frozen(True) # frozen headings instead of split panes
    sheet.set_horz_split_pos(rowx+1) # in general, freeze after last heading row
    sheet.set_remove_splits(True) # if user does unfreeze, don't leave a split there
    ts_re = re.compile('ts', re.I)
    
    for i in range(len(col_width)):
        sheet.col(i).width = col_width[i]
    
    ts_style_pre ='font: bold on; align: wrap on, vert centre, horiz center;  \
                 borders: left thin, right thin, top thin, bottom thin;  \
                 pattern: pattern solid, fore-colour ' 
    ts_color = ['light_blue;', 'light_green', 'light_orange', 'light_turquoise' ]            

    prev_row  = []
    steps = 0
    for row in data:
        rowx = rowx + 1
        for colx, cell in enumerate(row):
#             pass
#             print colx
            if rowx < 6:
#             if rowx < len(data) -1:
                print type(cell.cell_value), cell.cell_value
                sheet.write(rowx, colx, cell.cell_value, data_xfs[colx])
    book.save(file_name)


def create_xls( rowData ):

    # step 1: prepare heading data
    traversingCells = [ Pcell.Col_Title, Pcell.Col_Problem, Pcell.Col_Reproduction, \
                       Pcell.Col_Cause, Pcell.Col_Countermeasure ]
    hdngsNo =  traversingCells.insert(0, Pcell.Col_Casecode)
    hdngs =  ["CaseCode", "Title", "Problem", "Reproduction", "Cause", "CounterMeasure"]

    kinds =  'textId   textTitle   textCont  textCont  textCont   textComt'.split()
    colChs = [8,         40,        40,          50,         50,         30  ]
    colWidth = [256*x for x in colChs]

    
    # step 2: prepare cell style with easyxf
    ezxf = xlwt.easyxf
    kind_to_xf_map = {
        'date': ezxf(num_format_str='yyyy-mm-dd'),
        'int': ezxf(num_format_str='#,##0'),
        'money': ezxf('font: italic on; pattern: pattern solid, fore-colour grey25',
            num_format_str='$#,##0.00'),
        'price': ezxf(num_format_str='#0.000000'),
        'textId': ezxf('align: vert center, horiz center, wrap on'),
        'textTitle': ezxf('align: vert top, horiz left, wrap on'),
        'textCont': ezxf('align: vert top, horiz left, wrap on'),
        'textComt': ezxf('align: vert top, horiz left, wrap on'),
        }
    data_xfs = [kind_to_xf_map[k] for k in kinds]
    # step 3: write in sheet


    write_xls('appBreakdown.xls', 'Demo', hdngs, rowData, data_xfs, colWidth)


if __name__ == '__main__':
    main()
    
    
    
    
    
    
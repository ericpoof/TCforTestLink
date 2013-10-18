'''
Created on Oct 17, 2013

@author: Eric
'''

# 
# Quick way to test Python regex 
# http://pythex.org/

import re
import sys
sys.path.append('/Users/Eric/Documents/workspace/TCforTestLink/TestLink')
from xlsData_PLM import XlsData
from schemaPLM import PLM_Schema as Pcell

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
    
    for app in allApps:
        print 'name =', app.name, '  pattern = ', app.pattern
   
    # 2. read a excel file and create cell data CellExl()
    absolutePath = '/Users/Eric/Documents/workspace/TCforTestLink/TestLink/'
    xlsLocalFile = 'Testcases/Garda_issues_1015.xls'
    xlsFile = absolutePath + xlsLocalFile
    worksheet = 'DEFECT'
    
    xlsData = XlsData()
    xlsData.readXls(xlsFile, worksheet)
    xlsData.printXlsData()
    
    # 3. traverse chosen cells and search for patterns
    # => better be flexible by getting user input 
    traversingCells = [ Pcell.Col_Title, Pcell.Col_Problem, Pcell.Col_Reproduction, \
                       Pcell.Col_Cause, Pcell.Col_Countermeasure ]
    
    print '                                 '
    print ' ==== PLM issue breakdown ===== '
    print '                                 '
    for cell in xlsData.getCells():
            if cell.col_no in traversingCells:
    #             print 'row = ', cell.row_no, ' col = ', cell.col_no, ' value = ', cell.cell_value
                for app in allApps:
#                     print 'cell_value to match' , app.pattern, ': ' , cell.cell_value
                    appRe = re.compile(app.pattern, re.I)
#                     print appRe.search(cell.cell_value)
                    if appRe.search(cell.cell_value) is not None:
                        print 'row = ', cell.row_no, ' is ' , app.name , ' issue: ' 
#                         print 'cell_value to match' , app.pattern, ': ' , cell.cell_value

                
    

    
    
    
    # 4. create a spreadsheet based on matching lists
    

class PreloadApp(object): 
    def __init__(self):
        ## app name
        self.name = ''
        ## search pattern
        self.pattern = ''    

    



if __name__ == '__main__':
    main()
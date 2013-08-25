'''
Created on Jul 1, 2013

@author: me.jung
'''

import xlrd
import re
from testsuite2LXml_ALO import Testsuite2LXml
from xlsData import XlsData
from cellParser_ALO import CellParser
from testSuite import TestSuite, TestCase, Step
from lxml import etree
from _pyio import BytesIO
from schema import ATTLookout_Schema as AL
import xlwt
import datetime

# Conversion Flow

def parseOneLevel():
    file = 'Testcases/Attfamilymapsample2.xml'
    with open(file, 'r') as f:
        print f
        tree = etree.parse(f)
#     TString = etree.tostring(tree)
#     print TString

#     some_xml_data = "<root>data</root>"
#     root = etree.fromstring(some_xml_data)
#     print(root.tag)
#     TString = etree.tostring(root)
#     print TString
#     etree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=False)    

#     some_file_like_object = BytesIO("<root>data</root>")
#     tree = etree.parse(some_file_like_object)
#     etree.tostring(tree)

    r = tree.xpath('//testcase')
    print type(r)
    for tc in r:
#         print 'tc type = ', type(tc)
        print ""
        print " === testcase ==="
        print tc.get('name')
        for tc_el in tc:
            print ' %s : %s' % (tc_el.tag, tc_el.text)
            if tc_el.tag == 'steps':
                print 'steps type? = ', tc_el.tag
                for st in tc_el:
                    print 'type_tc_el = ', type(st)
                    st_tree = etree.ElementTree(st)
                    print 'step in etree : ', etree.tostring(st_tree)
                    for st_el in st:
                        print ' %s : %s' % (st_el.tag, st_el.text)

def Element_recursive(root, ts_root):
    for elm in root:
        if elm.tag == 'testsuite':
            new_ts = TestSuite()
            new_ts.name = elm.get('name')
            new_ts = Element_recursive(elm, new_ts )
            ts_root.testsuites.append(new_ts)
        elif elm.tag == 'testcase':
            new_tc = TestCase()
            new_tc.name = elm.get('name')
            for sub_elm in elm:
                if sub_elm.tag == 'preconditions':
                    new_tc.preconditions = sub_elm.text
                if sub_elm.tag == 'steps':
                    for st in sub_elm:
                        new_st = Step()
                        for st_elm in st:
                            if st_elm.tag == 'actions':
                                new_st.actions = st_elm.text
                            if st_elm.tag == 'expectedresults':
                                new_st.expectedresults = st_elm.text
                        new_tc.steps.append(new_st)
            ts_root.testcases.append(new_tc)
    return ts_root
    
                        

# def write_xls(file_name, sheet_name, headings, data, heading_xf, data_xfs, col_width):
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

    prev_value = ''
    for row in data:
        rowx += 1
        if ts_re.match(row[0]):
            ts_style = ts_style_pre + ts_color[row[6] % 4]
            heading_xf = ezxf(ts_style)
            sheet.write(rowx, 0, row[0], heading_xf)
            sheet.write_merge(rowx, rowx, 1, 5, row[1], heading_xf)
        else:
            if row[1] == prev_value:
                merge_flag = True
            else:
#                 print 'row[1]: ' , row[1]
#                 print 'prev_value: ', prev_value
                merge_flag = False
            prev_value = row[1]

            for colx, value in enumerate(row):
                    sheet.write(rowx, colx, value, data_xfs[colx])

#             if merge_flag:
#                 m_style = ezxf('align: vert center, horiz left, wrap on')
#                 sheet.write(rowx-1, 0, '' )
#                 sheet.write(rowx-1, 1, '' )
#                 sheet.write(rowx-1, 2, '' )
#                 sheet.write_merge(rowx-1,rowx, 0,0, row[0], m_style)
#                 sheet.write_merge(rowx-1,rowx, 1,1, row[1], m_style)
#                 sheet.write_merge(rowx-1,rowx, 2,2, row[2], m_style)
#             else:
#                 for colx, value in enumerate(row):
#                         sheet.write(rowx, colx, value, data_xfs[colx])
                
    book.save(file_name)


def create_xls( testsuite ):
    import sys
    # Testcase
    hdngs = ['ID', 'Title', 'Preconditions', 'Steps', 'Expected', 'Comment']
    kinds =  'textId   textTitle   textCont  textCont  textCont   textComt'.split()
    colChs = [8,         40,        40,          50,         50,         30  ]
    colWidth = [256*x for x in colChs]

#     kinds =  'date    text          int         price         money    text'.split()

    ts = testsuite
    data = []
    level = 0
    def TS_recursive(ts_top, level):
        if len(ts_top.testsuites) > 0:
            level = level + 1
            for ts_elm in ts_top.testsuites:
                ts_title = ts_elm.name
                row = [ 'ts', ts_title, '', '', '', '' , level]
                data.append(row)
                if len(ts_elm.testcases) > 0:
                    for tc in ts_elm.testcases:
                        tc_title = tc.name
                        tc_precon = tc.preconditions
                        for st in tc.steps:
                            st_desc = st.actions
                            st_expt = st.expectedresults
                            row = [ 'tc_no', tc_title, tc_precon, st_desc, st_expt, '' ]
                            data.append(row)
                if len(ts_elm.testsuites) > 0:
                    TS_recursive(ts_elm, level)
        if len(ts_top.testcases) > 0:
                    for tc in ts_top.testcases:
                        tc_title = tc.name
                        tc_precon = tc.preconditions
                        for st in tc.steps:
                            st_desc = st.actions
                            st_expt = st.expectedresults
                            row = [ 'tc_no', tc_title, tc_precon, st_desc, st_expt, '' ]
                            data.append(row)
                    
    TS_recursive(ts, level)

    ezxf = xlwt.easyxf
#     heading_xf = ezxf('font: bold on; align: wrap on, vert centre, horiz center;  \
#                      pattern: pattern solid, fore-colour yellow; \
#                      borders: left thin, right thin, top thin, bottom thin;' \
#                      )
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
#     write_xls('Home_testsuite_conv.xls', 'Demo', hdngs, data, heading_xf, data_xfs, colWidth)
    write_xls('Home_testsuite_conv.xls', 'Demo', hdngs, data, data_xfs, colWidth)
    
    
def main():

#     parseOneLevel()
    file = 'Testcases/Home.testsuite-deep2.xml'
    with open(file, 'r') as f:
        tree = etree.parse(f)
#     print etree.tostring(tree)
    root = tree.getroot()
    print 'root = ', root.tag, root.get('name'), type(root)
    
    ts_root = TestSuite()
    ts_root.name = root.get('name')
    
    ts_root = Element_recursive(root, ts_root)
    print 'recursive done'
    
    create_xls(ts_root)
     
    print 'done'

if __name__ == '__main__':
    main()

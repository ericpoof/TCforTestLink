'''
Created on Jul 2, 2013

@author: me.jung
'''



import xml.etree.ElementTree as ET
#import TCforTestLink.SampleElementTree 
from TCforTestLink.SampleElementTree import SampleElement


tree = ET.parse('Home_tc_sample.xml')
testsuite = tree.getroot()


print '----TOP----------'
print '"Top level"'
print testsuite.tag, testsuite.attrib

for child in testsuite:   # testsuite
    print "   ", '"one level down"'
    print "   ", child.tag, child.attrib
    for another_child in child: # detail/testcase 
        print "      ", '"two level down"'
        print "      ", another_child.tag, another_child.text
        for third_child in another_child:   # steps
            print "         ", '"three level down"'
            print "         ", third_child.tag, third_child.text
            for fourth_child in third_child:   # step
                print "         ", '"three level down"'
                print "         ", fourth_child.tag, fourth_child.text
                
#sampleXML = TCforTestLink.SampleElementTree.SampleElement()
sampleXML = SampleElement()
print sampleXML
    

'''
for step in testsuite.iter('exactpectedresults'):
    print step.text 

for step in testsuite.iter('step_number'):
    print step.text 

for step in testsuite.iter('actions'):
    print step.text 
'''

if __name__ == '__main__':
    pass
#!/usr/bin/env python
# Usage: python alto_ocr_confidence.py <altofile>

import sys
import xml.etree.cElementTree as ET

namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO', 'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#', 'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#'}
tree = ET.parse(sys.argv[1])
score = 0
count = 0

for elem in tree.findall('.//alto-2:String', namespace): # make sure the correct namespace is selected
	wc = elem.attrib.get('WC')
	score += float(wc)
	count += 1

confidence = score/count
result = round(100 * (confidence), 2)

print(result)
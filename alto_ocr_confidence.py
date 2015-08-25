#!/usr/bin/env python
# Usage: python alto_ocr_confidence.py <altofile>

import sys
import xml.etree.cElementTree as ET

score = float(0)
count = 0
ET.register_namespace('alto-1', 'http://schema.ccs-gmbh.com/ALTO')
ET.register_namespace('alto-2', 'http://www.loc.gov/standards/alto/ns-v2#')
ET.register_namespace('alto-3', 'http://www.loc.gov/standards/alto/ns-v3#')

tree = ET.parse(sys.argv[1])

for elem in tree.getroot().findall('.//{http://www.loc.gov/standards/alto/ns-v2#}String'):	# findall requires explicit namespace declaration
	wc = elem.attrib.get('WC')
	score += float(wc)
	count += 1

confidence = score/count
result = round(100 * (confidence), 2)

print(result)
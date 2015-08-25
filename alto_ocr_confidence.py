#!/usr/bin/env python
# Usage: python alto_ocr_confidence.py <inputdir>

import os
import sys
import xml.etree.cElementTree as ET

namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO', 'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#', 'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#'}

for root, dirs, files in os.walk(sys.argv[1]):
	for file in files:
		if file.endswith('.xml') or file.endswith('.alto'):
			fname = open(os.path.join(root, file))
			for f in fname:
				tree = ET.parse(fname)
				score = 0
				count = 0
				for elem in tree.iterfind('.//alto-2:String', namespace): # make sure the correct namespace is set
					wc = elem.attrib.get('WC')
					score += float(wc)
					count += 1
				confidence = score/count
				result = round(100 * (confidence), 2)
				print('Filename: %s, Confidence: %s' % (file, result))
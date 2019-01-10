#!/usr/bin/env python
# Usage: python alto_ocr_text.py <altofile>

import codecs
import os
import sys
import xml.etree.ElementTree as ET


if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
                 'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
                 'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#'}
    tree = ET.parse(sys.argv[1])
    xmlns = tree.getroot().tag.split('}')[0].strip('{')
    if xmlns in namespace.values():
        for lines in tree.iterfind('.//{%s}TextLine' % xmlns):
            sys.stdout.write('\n')
            for line in lines.findall('{%s}String' % xmlns):
                text = line.attrib.get('CONTENT') + ' '
                sys.stdout.write(text)
    else:
        print('ERROR: Not a valid ALTO file (namespace declaration missing)')
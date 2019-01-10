#!/usr/bin/env python
# Usage: python alto_ocr_confidence.py <inputdir>

import os
import sys
import xml.etree.ElementTree as ET

namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
             'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
             'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#'}

def parse_alto(fh):
    tree = ET.parse(fh)
    score = 0
    count = 0
    xmlns = tree.getroot().tag.split('}')[0].strip('{')  # extract namespace from root
    if xmlns in namespace.values():
        for elem in tree.iterfind('.//{%s}String' % xmlns):
                wc = elem.attrib.get('WC')
                score += float(wc)
                count += 1
        if count > 0:
            confidence = score / count
            result = round(100 * confidence, 2)
            sys.stdout.write('\nFile: %s, Confidence: %s' % (fh.name, result))
        else:
            sys.stdout.write('\nFile: %s, Confidence: 00.00' % (fh.name))
    else:
        sys.stdout.write('\nERROR: File "%s" does not appear to be a valid ALTO file (namespace declaration missing)' % fh.name)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python %s <inputdir>" % os.path.basename(__file__))
        sys.exit(-1)

    for root, dirs, files in os.walk(sys.argv[1]):
        for filename in files:
            if filename.endswith('.xml') or filename.endswith('.alto'):
                fh = open(os.path.join(root, filename), 'r', encoding='UTF8')
                for f in fh:
                    parse_alto(fh)
                fh.close()

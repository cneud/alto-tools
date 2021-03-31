#!/usr/bin/env python

""" alto_tools.py: simple methods to perform operations on ALTO xml files """

import argparse
import codecs
import io
import os
import sys
import xml.etree.ElementTree as ET

__version__ = '0.0.2'


def alto_parse(alto):
    """ Convert ALTO xml file to element tree """
    try:
        xml = ET.parse(alto)
    except ET.ParseError as e:
        sys.stdout.write('\nERROR: Failed parsing "%s" - ' % alto.name + str(e))
    # Register ALTO namespaces
    # https://www.loc.gov/standards/alto/ | https://github.com/altoxml
    # alto-bnf (unoffical) BnF ALTO dialect - for further info see
    # http://bibnum.bnf.fr/alto_prod/documentation/alto_prod.html
    namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
                 'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
                 'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#',
                 'alto-4': 'http://www.loc.gov/standards/alto/ns-v4#',
                 'alto-bnf': 'http://bibnum.bnf.fr/ns/alto_prod'}
    # Extract namespace from document root
    if 'http://' in str(xml.getroot().tag.split('}')[0].strip('{')):
        xmlns = xml.getroot().tag.split('}')[0].strip('{')
    else:
        try:
            ns = xml.getroot().attrib
            xmlns = str(ns).split(' ')[1].strip('}').strip("'")
        except IndexError:
            sys.stdout.write('\nWARNING: File "%s": no namespace declaration found.' % alto.name)
            xmlns = 'no_namespace_found'
    if xmlns in namespace.values():
        return alto, xml, xmlns
    else:
        sys.stdout.write('\nWARNING: File "%s": namespace is not registered.' % alto.name)


def alto_text(xml, xmlns):
    """ Extract text content from ALTO xml file """
    # Ensure use of UTF-8
    if isinstance(sys.stdout, io.TextIOWrapper) and sys.stdout.encoding != 'UTF-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    # Find all <TextLine> elements
    for lines in xml.iterfind('.//{%s}TextLine' % xmlns):
        # New line after every <TextLine> element
        sys.stdout.write('\n')
        # Find all <String> elements
        for line in lines.findall('{%s}String' % xmlns):
            # Get value of attribute @CONTENT from all String elements
            text = line.attrib.get('CONTENT') + ' '
            sys.stdout.write(text)


def alto_illustrations(xml, xmlns):
    """ Extract bounding boxes of illustration from ALTO xml file """
    # Find all <Illustration> elements
    for illustration in xml.iterfind('.//{%s}Illustration' % xmlns):
        # Get @ID of <Illustration> element
        illustration_id = illustration.attrib.get('ID')
        # Get coordinates of <Illustration> element
        illustration_coords = (illustration.attrib.get('HEIGHT') + ','
                            + illustration.attrib.get('WIDTH') + ','
                            + illustration.attrib.get('VPOS') + ','
                            + illustration.attrib.get('HPOS'))
        sys.stdout.write('\n')
        illustrations = illustration_id + '=' + illustration_coords
        sys.stdout.write(illustrations)


def alto_confidence(alto, xml, xmlns):
    """ Calculate word confidence for ALTO xml file """
    score = 0
    count = 0
    # Find all <String> elements
    for conf in xml.iterfind('.//{%s}String' % xmlns):
        # Get value of attribute @WC (Word Confidence) of all <String> elements
        wc = conf.attrib.get('WC')
        # Calculate sum of all @WC values as float
        score += float(wc)
        # Increment counter for each word
        count += 1
        # Divide sum of @WC values by number of words
    if count > 0:
        confidence = score / count
        result = round(100 * confidence, 2)
        sys.stdout.write('\nFile: %s, Confidence: %s' % (alto.name, result))
    else:
        sys.stdout.write('\nFile: %s, Confidence: 00.00' % alto.name)


def write_output(alto, output, args):
    """ Write output to file(s) instead of stdout """
    if len(output) == 0:
        sys.stdout.write()
    else:
        if args.text:
            output_filename = alto.name + '.txt'
            sys.stdout = open(output_filename, 'w')
            sys.stdout.write('writing output file: ' + alto.name + '.txt')
        if args.illustrations:
            output_filename = alto.name + '.img.txt'
            sys.stdout = open(output_filename, 'w')
            sys.stdout.write('writing output file: ' + alto.name + '.img.txt')
        if args.confidence:
            output_filename = alto.name + '.conf.txt'
            sys.stdout = open(output_filename, 'w')
            sys.stdout.write('writing output file: ' + alto.name + '.conf.txt')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="ALTO Tools: simple methods to perform operations on ALTO xml files",
        add_help=True,
        prog='alto_tools.py',
        usage='python %(prog)s INPUT [options]')
    parser.add_argument('INPUT',
                        nargs='+',
                        help='path to ALTO file')
    parser.add_argument('-o', '--output',
                        default='',
                        dest='output',
                        help='path to output directory (if none specified, CWD is used)')
    parser.add_argument('-v', '--version',
                        action='version',
                        version=__version__,
                        help='show version number and exit')
    parser.add_argument('-c', '--confidence',
                        action='store_true',
                        default=False,
                        dest='confidence',
                        help='calculate OCR page confidence from ALTO file')
    parser.add_argument('-t', '--text',
                        action='store_true',
                        default=False,
                        dest='text',
                        help='extract text content from ALTO file')
    parser.add_argument('-l', '--illustrations',
                        action='store_true',
                        default=False,
                        dest='illustrations',
                        help='extract bounding boxes of illustrations from ALTO file')
    args = parser.parse_args()
    return args


def walker(inputs, fnfilter=lambda fn: True):
    """
    Returns all file names in inputs, and recursively for directories.

    If an input is
    - a file:      return as is
    - a directory: return all files in it, recursively, filtered by fnfilter.
    """
    for i in inputs:
        if os.path.isfile(i):
            yield i
        else:
            for root, _, files in os.walk(i):
                for f in files:
                    if fnfilter(f):
                        yield os.path.join(root, f)


def main():
    if sys.version_info < (3, 0):
        sys.stdout.write('Python 3 is required.\n')
        sys.exit(-1)

    args = parse_arguments()
    if not len(sys.argv) > 2:
        sys.stdout.write('\nNo operation specified, ')
        os.system('python alto_tools.py -h')
        sys.exit(-1)
    else:
        #fnfilter = lambda fn: fn.endswith('.xml') or fn.endswith('.alto')
        #for filename in walker(args.INPUT, fnfilter):
            alto = open((sys.argv[1]), 'r', encoding='UTF8')
            try:
                alto, xml, xmlns = alto_parse(alto)
            except IndexError:
                pass
            if args.confidence:
                alto_confidence(alto, xml, xmlns)
            if args.text:
                alto_text(xml, xmlns)
            if args.illustrations:
                alto_illustrations(xml, xmlns)


if __name__ == "__main__":
    main()

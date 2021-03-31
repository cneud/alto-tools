#!/usr/bin/env python

""" alto_tools.py: simple methods to perform operations on ALTO xml files """

import argparse
import codecs
import io
import os
import sys
import xml.etree.ElementTree as etree

__version__ = '0.0.1'


def alto_parse(alto):
    """ Convert ALTO xml file to element tree """
    try:
        xml = etree.parse(alto)
    except etree.ParseError as e:
        sys.stdout.write('\nERROR: Failed parsing "%s" - '
                         % alto.name + str(e))
    # Register ALTO namespaces
    namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
                 'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
                 'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#',
                 'alto-4': 'http://www.loc.gov/standards/alto/ns-v4#',
                 # BnF ALTO (unoffical) - for further info see
                 # http://bibnum.bnf.fr/alto_prod/documentation/alto_prod.html
                 'alto-bnf': 'http://bibnum.bnf.fr/ns/alto_prod'}
    # Extract namespace from document root
    if 'http://' in str(xml.getroot().tag.split('}')[0].strip('{')):
        xmlns = xml.getroot().tag.split('}')[0].strip('{')
    else:
        try:
            ns = xml.getroot().attrib
            xmlns = str(ns).split(' ')[1].strip('}').strip("'")
        except IndexError:
            sys.stdout.write('\nWARNING: File "%s": no namespace declaration '
                             'found.' % alto.name)
            xmlns = 'no_namespace_found'
    if xmlns in namespace.values():
        return alto, xml, xmlns
    else:
        sys.stdout.write('\nWARNING: File "%s": namespace is not registered.'
                         % alto.name)


def alto_text(xml, xmlns):
    """ Extract text content from ALTO xml file """
    # Make sure to use UTF-8
    if isinstance(sys.stdout, io.TextIOWrapper) and sys.stdout.encoding != 'UTF-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    # Find all TextLine elements
    for lines in xml.iterfind('.//{%s}TextLine' % xmlns):
        # New line after every TextLine element
        sys.stdout.write('\n')
        # Find all String elements
        for line in lines.findall('{%s}String' % xmlns):
            # Get value of attribute CONTENT from all String elements
            text = line.attrib.get('CONTENT') + ' '
            sys.stdout.write(text)


def alto_graphic(xml, xmlns):
    """ Extract coordinates of illustrations from ALTO xml file """
    # Find all GraphicalElement elements
    for graphical in xml.iterfind('.//{%s}GraphicalElement' % xmlns):
        # Get ID of GraphicalElement element
        graphical_id = graphical.attrib.get('ID')
        # Get coordinates of GraphicalElement element
        graphical_coords = (graphical.attrib.get('HEIGHT') + ','
                            + graphical.attrib.get('WIDTH') + ','
                            + graphical.attrib.get('VPOS') + ','
                            + graphical.attrib.get('HPOS'))
        sys.stdout.write('\n')
        graphical_elements = graphical_id + '=' + graphical_coords
        sys.stdout.write(graphical_elements)


def alto_confidence(alto, xml, xmlns):
    """ Calculate word confidence for ALTO xml file """
    score = 0
    count = 0
    # Find all String elements
    for elem in xml.iterfind('.//{%s}String' % xmlns):
        # Get value of attribute WC (Word Confidence) of all String elements
        wc = elem.attrib.get('WC')
        # Calculate sum of all WC values as float
        score += float(wc)
        # Increment counter for each word
        count += 1
        # Divide sum of WC values by number of words
        if count > 0:
            confidence = score / count
            result = round(100 * confidence, 2)
            sys.stdout.write('\nFile: %s, Confidence: %s' %
                             (alto.name, result))
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
        if args.graphic:
            output_filename = alto.name + '.graphic.txt'
            sys.stdout = open(output_filename, 'w')
            sys.stdout.write('writing output file: ' + alto.name +
                             '.graphic.txt')
        if args.confidence:
            output_filename = alto.name + '.conf.txt'
            sys.stdout = open(output_filename, 'w')
            sys.stdout.write('writing output file: ' + alto.name + '.conf.txt')


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="ALTO Tools: "
                    "simple methods to perform operations on ALTO xml files",
        add_help=True,
        prog='alto_tools.py',
        usage='python %(prog)s INPUT [options]')
    parser.add_argument('INPUT',
                        nargs='+',
                        help='path to ALTO file or directory containing '
                             'ALTO file(s)')
    parser.add_argument('-o', '--output',
                        default='',
                        dest='output',
                        help='path to output directory (if none specified, '
                             'stdout is used)')
    parser.add_argument('-v', '--version',
                        action='version',
                        version=__version__,
                        help='show version number and exit')
    parser.add_argument('-c', '--confidence',
                        action='store_true',
                        default=False,
                        dest='confidence',
                        help='calculate page confidence of the ALTO '
                             'document(s)')
    parser.add_argument('-t', '--text',
                        action='store_true',
                        default=False,
                        dest='text',
                        help='extract text content of the ALTO document(s)')
    parser.add_argument('-g', '-graphic',
                        action='store_true',
                        default=False,
                        dest='graphic',
                        help='extract coordinates of graphical elements from '
                             'the ALTO document(s)')
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
        fnfilter = lambda fn: fn.endswith('.xml') or fn.endswith('.alto')
        for filename in walker(args.INPUT, fnfilter):
            alto = open(filename, 'r', encoding='UTF8')
            try:
                alto, xml, xmlns = alto_parse(alto)
            except IndexError:
                pass
            if args.confidence:
                alto_confidence(alto, xml, xmlns)
            if args.text:
                alto_text(xml, xmlns)
            if args.graphic:
                alto_graphic(xml, xmlns)


if __name__ == "__main__":
    main()

#!/usr/bin/env python

""" alto_tools.py: simple methods to perform operations on ALTO xml files """

import argparse
import codecs
import os
import sys
from lxml import etree
# http://lxml.de/installation.html
# http://lxml.de/compatibility.html

__version__ = '0.0.1'


def alto_parse(alto):
    """ Convert ALTO xml file to element tree """
    try:
        xml = etree.parse(alto)
    except etree.ParseError as e:
        sys.stdout.write('\nERROR: Failed parsing "%s" - '
                         % alto.name + str(e))
    # http://lxml.de/tutorial.html#namespaces
    # Register ALTO namespaces
    namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
                 'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
                 'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#'}
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
    if sys.stdout.encoding != 'UTF-8':
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


def alto_transform(xml):
    """ Transform ALTO xml with XSLT """
    # http://lxml.de/xpathxslt.html#xslt
    xsl = open('xsl', 'r', encoding='UTF8')
    try:
        dom = etree.parse(xml)
        xslt = etree.parse(xsl)
        transform = etree.XSLT(xslt)
        newdom = transform(dom)
        print(etree.tostring(newdom))
    except AttributeError:
        pass

def alto_metadata(xml, xmlns):
    """ Extract metadata from ALTO xml file """
    # Description
    sys.stdout.write('\n<Description>\n')
    try:
        xml.find(('.//{%s}Description' % xmlns).find
                 ('{%s}sourceImageInformation' % xmlns).find
                 ('{%s}fileName' % xmlns).text is not None)
        sys.stdout.write(('\nfileName                   =   %s' % xml.find
                         ('.//{%s}Description' % xmlns).find
                         ('{%s}sourceImageInformation' % xmlns).find
                         ('{%s}fileName' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nfileName                   =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}Description' % xmlns).find
                 ('{%s}sourceImageInformation' % xmlns).find
                 ('{%s}fileIdentifier' % xmlns).text is not None)
        sys.stdout.write(('\nfileIdentifier             =   %s' % xml.find
                         ('.//{%s}Description' % xmlns).find
                         ('{%s}sourceImageInformation' % xmlns).find
                         ('{%s}fileIdentifier' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nfileIdentifier             =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}Description' % xmlns).find
                 ('{%s}sourceImageInformation' % xmlns).find
                 ('{%s}documentIdentifier' % xmlns).text is not None)
        sys.stdout.write(('\ndocumentIdentifier         =   %s' % xml.find
                         ('.//{%s}Description' % xmlns).find
                         ('{%s}sourceImageInformation' % xmlns).find
                         ('{%s}documentIdentifier' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\ndocumentIdentifier         =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}Description' % xmlns).find
                 ('{%s}MeasurementUnit' % xmlns).text is not None)
        sys.stdout.write(('\nMeasurementUnit            =   %s' % xml.find
                         ('.//{%s}Description' % xmlns).find
                         ('{%s}MeasurementUnit' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nMeasurementUnit            =   -- NOT_DEFINED --')
    # OCRProcessing
    sys.stdout.write('\n\n<OCRProcessing>\n')
    try:
        xml.find(('.//{%s}OCRProcessing' % xmlns).text is not None)
        sys.stdout.write('\nID                         =   %s' % xml.find
                         ('.//{%s}OCRProcessing' % xmlns).attrib.get('ID'))
    except AttributeError:
        sys.stdout.write(
            '\nID                         =   -- NOT_DEFINED --')
    # preProcessingStep
    sys.stdout.write('\n\n<preProcessingStep>\n')
    try:
        xml.find(('.//{%s}preProcessingStep' % xmlns).find
                 ('{%s}processingDateTime' % xmlns).text is not None)
        sys.stdout.write(('\nprocessingDateTime         =   %s' % xml.find
                         ('.//{%s}preProcessingStep' % xmlns).find
                         ('{%s}processingDateTime' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nprocessingDateTime         =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}preProcessingStep' % xmlns).find
                 ('{%s}processingAgency' % xmlns).text is not None)
        sys.stdout.write(('\nprocessingAgency           =   %s' % xml.find
                         ('.//{%s}preProcessingStep' % xmlns).find
                         ('{%s}processingAgency' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nprocessingAgency           =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}preProcessingStep' % xmlns).find
                 ('{%s}processingStepDescription' % xmlns).text is not None)
        sys.stdout.write(('\nprocessingStepDescription  =   %s' % xml.find
                         ('.//{%s}preProcessingStep' % xmlns).find
                         ('{%s}processingStepDescription' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nprocessingStepDescription  =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}preProcessingStep' % xmlns).find
                 ('{%s}processingStepSettings' % xmlns).text is not None)
        sys.stdout.write(('\nprocessingStepSettings     =   %s' % xml.find
                         ('.//{%s}preProcessingStep' % xmlns).find
                         ('{%s}processingStepSettings' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nprocessingStepSettings     =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}preProcessingStep' % xmlns).find
                 ('{%s}processingSoftware' % xmlns).find
                 ('{%s}softwareCreator' % xmlns).text is not None)
        sys.stdout.write(('\nsoftwareCreator            =   %s' % xml.find
                         ('.//{%s}preProcessingStep' % xmlns).find
                         ('{%s}processingSoftware' % xmlns).find
                         ('{%s}softwareCreator' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareCreator            =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}preProcessingStep' % xmlns).find
                 ('{%s}processingSoftware' % xmlns).find
                 ('{%s}softwareName' % xmlns).text is not None)
        sys.stdout.write(('\nsoftwareName               =   %s' % xml.find
                         ('.//{%s}preProcessingStep' % xmlns).find
                         ('{%s}processingSoftware' % xmlns).find
                         ('{%s}softwareName' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareName               =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}preProcessingStep' % xmlns).find
                 ('{%s}processingSoftware' % xmlns).find
                 ('{%s}softwareVersion' % xmlns).text is not None)
        sys.stdout.write(('\nsoftwareVersion            =   %s' % xml.find
                         ('.//{%s}preProcessingStep' % xmlns).find
                         ('{%s}processingSoftware' % xmlns).find
                         ('{%s}softwareVersion' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareVersion            =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}preProcessingStep' % xmlns).find
                 ('{%s}processingSoftware' % xmlns).find
                 ('{%s}applicationDescription' % xmlns).text is not None)
        sys.stdout.write(('\napplicationDescription     =   %s' % xml.find
                         ('.//{%s}preProcessingStep' % xmlns).find
                         ('{%s}processingSoftware' % xmlns).find
                         ('{%s}applicationDescription' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\napplicationDescription     =   -- NOT_DEFINED --')
    # ocrProcessingStep
    sys.stdout.write('\n\n<ocrProcessingStep>\n')
    try:
        xml.find(('.//{%s}ocrProcessingStep' % xmlns).find
                 ('{%s}processingDateTime' % xmlns).text is not None)
        sys.stdout.write(('\nprocessingDateTime         =   %s' % xml.find
                         ('.//{%s}ocrProcessingStep' % xmlns).find
                         ('{%s}processingDateTime' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nprocessingDateTime         =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}ocrProcessingStep' % xmlns).find
                 ('{%s}processingAgency' % xmlns).text is not None)
        sys.stdout.write(('\nprocessingAgency           =   %s' % xml.find
                         ('.//{%s}ocrProcessingStep' % xmlns).find
                         ('{%s}processingAgency' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nprocessingAgency           =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}ocrProcessingStep' % xmlns).find
                 ('{%s}processingStepDescription' % xmlns).text is not None)
        sys.stdout.write(('\nprocessingStepDescription  =   %s' % xml.find
                         ('.//{%s}ocrProcessingStep' % xmlns).find
                         ('{%s}processingStepDescription' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nprocessingStepDescription  =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}ocrProcessingStep' % xmlns).find
                 ('{%s}processingStepSettings' % xmlns).text is not None)
        sys.stdout.write(('\nprocessingStepSettings     =   %s' % xml.find
                         ('.//{%s}ocrProcessingStep' % xmlns).find
                         ('{%s}processingStepSettings' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nprocessingStepSettings     =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}ocrProcessingStep' % xmlns).find
                 ('{%s}processingSoftware' % xmlns).find
                 ('{%s}softwareCreator' % xmlns).text is not None)
        sys.stdout.write(('\nsoftwareCreator            =   %s' % xml.find
                         ('.//{%s}ocrProcessingStep' % xmlns).find
                         ('{%s}processingSoftware' % xmlns).find
                         ('{%s}softwareCreator' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareCreator            =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}ocrProcessingStep' % xmlns).find
                 ('{%s}processingSoftware' % xmlns).find
                 ('{%s}softwareName' % xmlns).text is not None)
        sys.stdout.write(('\nsoftwareName               =   %s' % xml.find
                         ('.//{%s}ocrProcessingStep' % xmlns).find
                         ('{%s}processingSoftware' % xmlns).find
                         ('{%s}softwareName' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareName               =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}ocrProcessingStep' % xmlns).find
                 ('{%s}processingSoftware' % xmlns).find
                 ('{%s}softwareVersion' % xmlns).text is not None)
        sys.stdout.write(('\nsoftwareVersion            =   %s' % xml.find
                         ('.//{%s}ocrProcessingStep' % xmlns).find
                         ('{%s}processingSoftware' % xmlns).find
                         ('{%s}softwareVersion' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareVersion            =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}ocrProcessingStep' % xmlns).find
                 ('{%s}processingSoftware' % xmlns).find
                 ('{%s}applicationDescription' % xmlns).text is not None)
        sys.stdout.write(('\napplicationDescription     =   %s' % xml.find
                         ('.//{%s}ocrProcessingStep' % xmlns).find
                         ('{%s}processingSoftware' % xmlns).find
                         ('{%s}applicationDescription' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\napplicationDescription     =   -- NOT_DEFINED --')
    # postProcessingStep 
    sys.stdout.write('\n\n<postProcessingStep>\n')
    try:
        xml.find(('.//{%s}postProcessingStep' % xmlns).find
                 ('{%s}processingDateTime' % xmlns).text is not None)
        sys.stdout.write(('\nprocessingDateTime         =   %s' % xml.find
                         ('.//{%s}postProcessingStep' % xmlns).find
                         ('{%s}processingDateTime' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nprocessingDateTime         =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}postProcessingStep' % xmlns).find
                 ('{%s}processingAgency' % xmlns).text is not None)
        sys.stdout.write(('\nprocessingAgency           =   %s' % xml.find
                         ('.//{%s}postProcessingStep' % xmlns).find
                         ('{%s}processingAgency' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nprocessingAgency           =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}postProcessingStep' % xmlns).find
                 ('{%s}processingStepDescription' % xmlns).text is not None)
        sys.stdout.write(('\nprocessingStepDescription  =   %s' % xml.find
                         ('.//{%s}postProcessingStep' % xmlns).find
                         ('{%s}processingStepDescription' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nprocessingStepDescription  =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}postProcessingStep' % xmlns).find
                 ('{%s}processingStepSettings' % xmlns).text is not None)
        sys.stdout.write(('\nprocessingStepSettings     =   %s' % xml.find
                         ('.//{%s}postProcessingStep' % xmlns).find
                         ('{%s}processingStepSettings' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nprocessingStepSettings     =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}postProcessingStep' % xmlns).find
                 ('{%s}processingSoftware' % xmlns).find
                 ('{%s}softwareCreator' % xmlns).text is not None)
        sys.stdout.write(('\nsoftwareCreator            =   %s' % xml.find
                         ('.//{%s}postProcessingStep' % xmlns).find
                         ('{%s}processingSoftware' % xmlns).find
                         ('{%s}softwareCreator' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareCreator            =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}postProcessingStep' % xmlns).find
                 ('{%s}processingSoftware' % xmlns).find
                 ('{%s}softwareName' % xmlns).text is not None)
        sys.stdout.write(('\nsoftwareName               =   %s' % xml.find
                         ('.//{%s}postProcessingStep' % xmlns).find
                         ('{%s}processingSoftware' % xmlns).find
                         ('{%s}softwareName' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareName               =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}postProcessingStep' % xmlns).find
                 ('{%s}processingSoftware' % xmlns).find
                 ('{%s}softwareVersion' % xmlns).text is not None)
        sys.stdout.write(('\nsoftwareVersion            =   %s' % xml.find
                         ('.//{%s}postProcessingStep' % xmlns).find
                         ('{%s}processingSoftware' % xmlns).find
                         ('{%s}softwareVersion' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareVersion            =   -- NOT_DEFINED --')
    try:
        xml.find(('.//{%s}postProcessingStep' % xmlns).find
                 ('{%s}processingSoftware' % xmlns).find
                 ('{%s}applicationDescription' % xmlns).text is not None)
        sys.stdout.write(('\napplicationDescription     =   %s' % xml.find
                         ('.//{%s}postProcessingStep' % xmlns).find
                         ('{%s}processingSoftware' % xmlns).find
                         ('{%s}applicationDescription' % xmlns).text))
    except AttributeError:
        sys.stdout.write(
            '\napplicationDescription     =   -- NOT_DEFINED --')
    sys.stdout.write('\n')


def alto_query(xml, xmlns):
    """ Query ALTO xml file using XPath expressions """
    # http://lxml.de/xpathxslt.html#xpath
    from lxml import etree

    query = input('Enter XPATH expression: ')
    try:
        result = etree.XPath(xml, xmlns, **query)
        sys.stdout.write(result)
        return result
    except AttributeError:
        sys.stdout.write('Not a valid XPATH expression')


def write_output(alto, output, args):
    """ Write output to file(s) instead of stdout """
    if len(output) == 0:
        sys.stdout.write()
    else:
        if args.text:
            output_filename = alto.name + '.txt'
            sys.stdout = open(output_filename, 'w')
            sys.stdout.write('writing output file: ' + alto.name + '.txt')
        if args.metadata:
            output_filename = alto.name + '.md.txt'
            sys.stdout = open(output_filename, 'w')
            sys.stdout.write('writing output file: ' + alto.name + '.md.txt')
        if args.graphic:
            output_filename = alto.name + '.graphic.txt'
            sys.stdout = open(output_filename, 'w')
            sys.stdout.write('writing output file: ' + alto.name +
                             '.graphic.txt')
        if args.confidence:
            output_filename = alto.name + '.conf.txt'
            sys.stdout = open(output_filename, 'w')
            sys.stdout.write('writing output file: ' + alto.name + '.conf.txt')
        if args.transform:
            output_filename = alto.name
            sys.stdout = open(output_filename, 'w')
            sys.stdout.write('writing output file: ' + alto.name)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="ALTO Tools: "
                    "simple methods to perform operations on ALTO xml files",
        add_help=True,
        prog='alto_tools.py',
        usage='python %(prog)s INPUT [options]')
    parser.add_argument('INPUT',
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
    parser.add_argument('-m', '--metadata',
                        action='store_true',
                        default=False,
                        dest='metadata',
                        help='extract metadata of the ALTO document(s)')
    parser.add_argument('-x', '--transform',
                        dest='transform',
                        help='transform ALTO document(s) to target format')
    parser.add_argument('-q', '--query',
                        dest='query',
                        help='query elements and attributes of the ALTO '
                             'document(s)')
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
    args = parse_arguments()
    if not len(sys.argv) > 2:
        sys.stdout.write('\nNo operation specified, ')
        os.system('python alto_tools.py -h')
        sys.exit(-1)
    else:
        fnfilter = lambda fn: fn.endswith('.xml') or fn.endswith('.alto')
        for filename in walker(sys.argv[1:], fnfilter):
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
            if args.metadata:
                alto_metadata(xml, xmlns)
            if args.transform:
                alto_transform(xml)
            if args.query:
                alto_query(xml, xmlns)


if __name__ == "__main__":
    main()

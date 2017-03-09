#!/usr/bin/env python

""" alto_tools.py: simple methods to perform operations on ALTO xml files """

import argparse
import codecs
import os
import sys
import xml.etree.ElementTree as ElementTree

import web

# Define scriptName when called from Java/Jython
scriptPath, scriptName = os.path.split(sys.argv[0])
if len(scriptName) == 0:
    scriptName = 'alto_tools'

__version__ = '0.0.1'


def alto_parse(alto):
    """ Convert ALTO xml file to element tree """
    try:
        xml = ElementTree.parse(alto)
    except ElementTree.ParseError as e:
        sys.stdout.write('\nERROR: Failed parsing "%s" - '
                         % alto.name + str(e))
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
                return text


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


def alto_ngrams(xml, xmlns):
    """ Generate ngrams from ALTO xml file """
    text = alto_text(xml, xmlns)
    # Set n 
    n = 3
    # Generate ngrams with zip()
    ngrams = ["".join(j) for j in zip(*[text[i:] for i in range(n)])]
    return ngrams


def alto_transform(xml):
    """ Transform ALTO xml with XSLT """
    xsl = open('xsl', 'r', encoding='UTF8')
    # Detect if running on Windows
    if os.name == 'nt':
        # Check if msxsl.exe is present
        from os.path import join
        print('Searching for XSLT processor...')
        xsltproc = 'msxsl.exe'
        for root, dirs, files in os.walk('C:\\'):
            if xsltproc in files:
                print('Found: %s' % join(root, xsltproc))
            else:
                print('No suitable XSLT processor found. '
                      'Please make sure "msxsl.exe" is installed.')
    else:
        try:
            import lxml.etree.XSLT as XSLT
        except ImportError:
            raise ImportError('No suitable XSLT processor found. '
                              'Please make sure "lxml" is installed.')
    dom = ElementTree.parse(xml)
    xslt = ElementTree.parse(xsl)
    transform = XSLT(xslt)
    newdom = transform(dom)
    print(ElementTree.tostring(newdom))


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
    query = input('Enter XPATH expression: ')
    try:
        result = query(xml % xmlns)
        return result
    except AttributeError:
        sys.stdout.write('Not a valid XPATH expression')

#  Supported XPath syntax
#  ----------------------
#  Predicates (expressions within square brackets) must be preceded by a tag 
#  name, an asterisk, or another predicate. 'position' predicates must be 
#  preceded by a tag name.
#  --------------------------------------------------------------------------
# |        tag        |  Selects all child elements with the given tag.      |
# |                   |  For example,'spam' selects all child elements named |
# |                   |  'spam', and 'spam/egg' selects all grandchildren    |
# |                   |  named 'egg' in all children named 'spam'.           |
# |--------------------------------------------------------------------------|
# |         *         |  Selects all child elements. For example, '*/egg'    |
# |                   |  selects all children named 'egg'.                   |
# |--------------------------------------------------------------------------|
# |         .         |  Selects the current node. This is mostly useful at  |
# |                   |  the beginning of the path, to indicate that it's a  |
# |                   |  relative path.                                      |
# |--------------------------------------------------------------------------|
# |         //        |  Selects all subelements, on all levels beneath the  |
# |                   |  current element. For example, './/egg' selects all  |
# |                   |  egg elements in the entire tree.                    |
# |--------------------------------------------------------------------------|
# |         ..        |  Selects the parent element. Returns 'None' if the   | 
# |                   |  path attempts to reach the ancestors of the start   |
# |                   |  element (the element 'find' was called on).         |
# |--------------------------------------------------------------------------|
# |     [@attrib]     |  Selects all elements that have the given attribute. |
# |--------------------------------------------------------------------------|
# | [@attrib='value'] |  Selects all elements for which the given attribute  |
# |                   |  has the given value. The value cannot contain       |
# |                   |  quotes.                                             |
# |--------------------------------------------------------------------------|
# |       [tag]       |  Selects all elements that have a child named 'tag'. |
# |                   |  Only immediate children are supported.              |
# |--------------------------------------------------------------------------|
# |    [tag='text']   |  Selects all elements that have a child named 'tag'  | 
# |                   |  whose complete text content, including descendants, |
# |                   |  equals the given 'text'.                            |
# |--------------------------------------------------------------------------|
# |     [position]    |  Selects all elements that are located at the given  |
# |                   |  position. The position can be either an integer (1  |
# |                   |  (1 is the first position), the expression 'last()'  |
# |                   |  (for the last position), or a position relative to  |
# |                   |  the last position (e.g. 'last()-1').                |
#  --------------------------------------------------------------------------


def write_output(alto, output, args):
    """ Write output to file(s) instead of stdout """
    if len(output) == 0:
        sys.stdout.write()
    else:
        if args.text:
            output_filename = alto.name + '.txt'
            sys.stdout = open(output_filename, 'w')
        if args.metadata:
            output_filename = alto.name + '.md.txt'
            sys.stdout = open(output_filename, 'w')
        if args.graphic:
            output_filename = alto.name + '.graphic.txt'
            sys.stdout = open(output_filename, 'w')
        if args.confidence:
            output_filename = alto.name + '.conf.txt'
            sys.stdout = open(output_filename, 'w')
        if args.transform:
            output_filename = alto.name
            sys.stdout = open(output_filename, 'w')
        if args.ngram:
            output_filename = alto.name + 'ngrams.txt'
            sys.stdout = open(output_filename, 'w')


def web_app(xml):
    """ Simple webapp """
    root = xml.getroot()
    # Create a web server to serve up the requests
    urls = (
        '/', 'index',
        '/elements', 'listElements',
        '/attributes/(.*)', 'getAttributes')
    app = web.application(urls, globals())
    # Bind to localhost port 8888
    app.run('0.0.0.0:8888')

    class Index:
        @staticmethod
        def get():
            return ('<a href="https://github.com/cneud/alto-tools">'
                    'ALTO Tools</a>: '
                    'simple methods to perform operations on ALTO xml files')

    class ListElements:
        @staticmethod
        def get():
            output = 'elements:['
            for child in root:
                print('child', child.tag, child.attrib)
                output += str(child.attrib) + ','
                output += ']'
                return output

    class GetAttributes:
        @staticmethod
        def get(value):
            output = 'attributes:['
            for child in root:
                if child.attrib['id'] == value:
                    output += str(child.attrib) + ','
                    output += ']'
                    return output


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
    parser.add_argument('-n', '--ngram',
                        action='store_true',
                        default=False,
                        dest='ngram',
                        help='generate ngrams from the ALTO document(s)')
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
    parser.add_argument('-w', '--web',
                        action='store_true',
                        default=False,
                        dest='web',
                        help='start webapp')
    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()
    if not len(sys.argv) > 2:
        sys.stdout.write('\nNo operation specified, ')
        os.system('python alto_tools.py -h')
        sys.exit(-1)
    else:
        for (root, dirs, files) in os.walk(sys.argv[1]):
            for filename in files:
                if filename.endswith('.xml') or filename.endswith('.alto'):
                    alto = open(os.path.join(root, filename),
                                'r', encoding='UTF8')
                    try:
                        alto, xml, xmlns = alto_parse(alto)
                    except IndexError:
                        pass
                    if args.confidence:
                        alto_confidence(alto, xml, xmlns)
                    if args.ngram:
                        alto_ngrams(xml, xmlns)
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
                    if args.web:
                        web_app(xml)


if __name__ == "__main__":
    main()

#!/usr/bin/env python

'''alto_tools.py: simple methods to perform operations on ALTO xml files'''

import os
import sys
import codecs
import argparse

import xml.etree.ElementTree as ET

# Define scriptName when called from Java/Jython
scriptPath, scriptName = os.path.split(sys.argv[0])
if len(scriptName) == 0:
    scriptName = 'alto_tools'

__version__= '0.0.1'


def alto_parse(alto):
    ''' Convert ALTO xml file to element tree '''
    try:
        xml = ET.parse(alto)
    except ET.ParseError as e:
        sys.stdout.write('\nERROR: Failed parsing "%s" - ' % alto.name + str(e))
    #Register ALTO namespaces    
    namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO', 
                 'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
                 'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#'}
                 # TODO: Handle xsi/xlink
    # Extract namespace from document root
    xmlns = xml.getroot().tag.split('}')[0].strip('{')
    if xmlns in namespace.values():
        return xml, xmlns
    else:
        sys.stdout.write('ERROR: File "%s" appears not to be a valid ALTO \
            file (namespace declaration missing or not registered)' % alto.name)

def alto_text(alto):
    ''' Extract text content from ALTO xml file '''
    xml, xmlns = alto_parse(alto)
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

def alto_confidence(alto):
    ''' Calculate word confidence for ALTO xml file '''
    xml, xmlns = alto_parse(alto)
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
        confidence = score / count
        result = round(100 * confidence, 2)
        sys.stdout.write('\nFile: %s, Confidence: %s' % (alto.name, result))

def alto_transform(alto, xsl):
    ''' Transform ALTO xml with XSLT '''
    xml, xmlns = alto_parse(alto)
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
                print('No suitable XSLT processor found. Please make sure \
                "msxsl.exe" is installed.')
    else:
        try: 
            import lxml.etree.XSLT as X
        except ImportError:
            raise ImportError('No suitable XSLT processor found. Please make \
                sure "lxml" is installed.')
    dom = ET.parse(xml)
    xslt = ET.parse(xsl)
    transform = X(xslt)
    newdom = transform(dom)
    print(ET.tostring(newdom, pretty_print=True))

def alto_metadata(alto):
    ''' Extract metadata from ALTO xml file '''
    xml, xmlns = alto_parse(alto)
    # Description
    sys.stdout.write('\n<Description>\n')
    try:
        xml.find('.//{%s}Description' % xmlns).find\
        ('{%s}sourceImageInformation' % xmlns).find\
        ('{%s}fileName' % xmlns).text != None
        sys.stdout.write('\nfileName                   =   %s' % xml.find\
            ('.//{%s}Description' % xmlns).find\
            ('{%s}sourceImageInformation' % xmlns).find\
            ('{%s}fileName' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nfileName                   =   -- NOT_DEFINED --')
    try:
        xml.find('.//{%s}Description' % xmlns).find\
        ('{%s}sourceImageInformation' % xmlns).find\
        ('{%s}fileIdentifier' % xmlns).text != None
        sys.stdout.write('\nfileIdentifier             =   %s' % xml.find\
            ('.//{%s}Description' % xmlns).find\
            ('{%s}sourceImageInformation' % xmlns).find\
            ('{%s}fileIdentifier' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nfileIdentifier             =   -- NOT_DEFINED --')
    try:
        xml.find('.//{%s}Description' % xmlns).find\
        ('{%s}sourceImageInformation' % xmlns).find\
        ('{%s}documentIdentifier' % xmlns).text != None
        sys.stdout.write('\ndocumentIdentifier         =   %s' % xml.find\
            ('.//{%s}Description' % xmlns).find\
            ('{%s}sourceImageInformation' % xmlns).find\
            ('{%s}documentIdentifier' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\ndocumentIdentifier         =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}Description' % xmlns).find\
        ('{%s}MeasurementUnit' % xmlns).text != None
        sys.stdout.write('\nMeasurementUnit            =   %s' % xml.find\
            ('.//{%s}Description' % xmlns).find\
            ('{%s}MeasurementUnit' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nMeasurementUnit            =   -- NOT_DEFINED --')
    # OCRProcessing
    sys.stdout.write('\n\n<OCRProcessing>\n')
    try: 
        xml.find('.//{%s}OCRProcessing' % xmlns).text != None
        sys.stdout.write('\nID                         =   %s' % xml.find\
            ('.//{%s}OCRProcessing' % xmlns).attrib.get('ID'))
    except AttributeError:
        sys.stdout.write(
            '\nID                         =   -- NOT_DEFINED --')
    # preProcessingStep
    sys.stdout.write('\n\n<preProcessingStep>\n')
    try: 
        xml.find('.//{%s}preProcessingStep' % xmlns).find\
        ('{%s}processingDateTime' % xmlns).text != None
        sys.stdout.write('\nprocessingDateTime         =   %s' % xml.find\
            ('.//{%s}preProcessingStep' % xmlns).find\
            ('{%s}processingDateTime' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nprocessingDateTime         =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}preProcessingStep' % xmlns).find\
        ('{%s}processingAgency' % xmlns).text != None
        sys.stdout.write('\nprocessingAgency           =   %s' % xml.find\
            ('.//{%s}preProcessingStep' % xmlns).find\
            ('{%s}processingAgency' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nprocessingAgency           =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}preProcessingStep' % xmlns).find\
        ('{%s}processingStepDescription' % xmlns).text != None
        sys.stdout.write('\nprocessingStepDescription  =   %s' % xml.find\
            ('.//{%s}preProcessingStep' % xmlns).find\
            ('{%s}processingStepDescription' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nprocessingStepDescription  =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}preProcessingStep' % xmlns).find\
        ('{%s}processingStepSettings' % xmlns).text != None
        sys.stdout.write('\nprocessingStepSettings     =   %s' % xml.find\
            ('.//{%s}preProcessingStep' % xmlns).find\
            ('{%s}processingStepSettings' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nprocessingStepSettings     =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}preProcessingStep' % xmlns).find\
        ('{%s}processingSoftware' % xmlns).find\
        ('{%s}softwareCreator' % xmlns).text != None
        sys.stdout.write('\nsoftwareCreator            =   %s' % xml.find\
            ('.//{%s}preProcessingStep' % xmlns).find\
            ('{%s}processingSoftware' % xmlns).find\
            ('{%s}softwareCreator' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareCreator            =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}preProcessingStep' % xmlns).find\
        ('{%s}processingSoftware' % xmlns).find\
        ('{%s}softwareName' % xmlns).text != None
        sys.stdout.write('\nsoftwareName               =   %s' % xml.find\
            ('.//{%s}preProcessingStep' % xmlns).find\
            ('{%s}processingSoftware' % xmlns).find\
            ('{%s}softwareName' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareName               =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}preProcessingStep' % xmlns).find\
        ('{%s}processingSoftware' % xmlns).find\
        ('{%s}softwareVersion' % xmlns).text != None
        sys.stdout.write('\nsoftwareVersion            =   %s' % xml.find\
            ('.//{%s}preProcessingStep' % xmlns).find\
            ('{%s}processingSoftware' % xmlns).find\
            ('{%s}softwareVersion' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareVersion            =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}preProcessingStep' % xmlns).find\
        ('{%s}processingSoftware' % xmlns).find\
        ('{%s}applicationDescription' % xmlns).text != None
        sys.stdout.write('\napplicationDescription     =   %s' % xml.find\
            ('.//{%s}preProcessingStep' % xmlns).find\
            ('{%s}processingSoftware' % xmlns).find\
            ('{%s}applicationDescription' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\napplicationDescription     =   -- NOT_DEFINED --')
    # ocrProcessingStep
    sys.stdout.write('\n\n<ocrProcessingStep>\n')
    try: 
        xml.find('.//{%s}ocrProcessingStep' % xmlns).find\
        ('{%s}processingDateTime' % xmlns).text != None
        sys.stdout.write('\nprocessingDateTime         =   %s' % xml.find\
            ('.//{%s}ocrProcessingStep' % xmlns).find\
            ('{%s}processingDateTime' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nprocessingDateTime         =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}ocrProcessingStep' % xmlns).find\
        ('{%s}processingAgency' % xmlns).text != None
        sys.stdout.write('\nprocessingAgency           =   %s' % xml.find\
            ('.//{%s}ocrProcessingStep' % xmlns).find\
            ('{%s}processingAgency' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nprocessingAgency           =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}ocrProcessingStep' % xmlns).find\
        ('{%s}processingStepDescription' % xmlns).text != None
        sys.stdout.write('\nprocessingStepDescription  =   %s' % xml.find\
            ('.//{%s}ocrProcessingStep' % xmlns).find\
            ('{%s}processingStepDescription' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nprocessingStepDescription  =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}ocrProcessingStep' % xmlns).find\
        ('{%s}processingStepSettings' % xmlns).text != None
        sys.stdout.write('\nprocessingStepSettings     =   %s' % xml.find\
            ('.//{%s}ocrProcessingStep' % xmlns).find\
            ('{%s}processingStepSettings' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nprocessingStepSettings     =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}ocrProcessingStep' % xmlns).find\
        ('{%s}processingSoftware' % xmlns).find\
        ('{%s}softwareCreator' % xmlns).text != None
        sys.stdout.write('\nsoftwareCreator            =   %s' % xml.find\
            ('.//{%s}ocrProcessingStep' % xmlns).find\
            ('{%s}processingSoftware' % xmlns).find\
            ('{%s}softwareCreator' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareCreator            =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}ocrProcessingStep' % xmlns).find\
        ('{%s}processingSoftware' % xmlns).find\
        ('{%s}softwareName' % xmlns).text != None
        sys.stdout.write('\nsoftwareName               =   %s' % xml.find\
            ('.//{%s}ocrProcessingStep' % xmlns).find\
            ('{%s}processingSoftware' % xmlns).find\
            ('{%s}softwareName' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareName               =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}ocrProcessingStep' % xmlns).find\
        ('{%s}processingSoftware' % xmlns).find\
        ('{%s}softwareVersion' % xmlns).text != None
        sys.stdout.write('\nsoftwareVersion            =   %s' % xml.find\
            ('.//{%s}ocrProcessingStep' % xmlns).find\
            ('{%s}processingSoftware' % xmlns).find\
            ('{%s}softwareVersion' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareVersion            =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}ocrProcessingStep' % xmlns).find\
        ('{%s}processingSoftware' % xmlns).find\
        ('{%s}applicationDescription' % xmlns).text != None
        sys.stdout.write('\napplicationDescription     =   %s' % xml.find\
            ('.//{%s}ocrProcessingStep' % xmlns).find\
            ('{%s}processingSoftware' % xmlns).find\
            ('{%s}applicationDescription' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\napplicationDescription     =   -- NOT_DEFINED --')
    # postProcessingStep 
    sys.stdout.write('\n\n<postProcessingStep>\n')
    try: 
        xml.find('.//{%s}postProcessingStep' % xmlns).find\
        ('{%s}processingDateTime' % xmlns).text != None
        sys.stdout.write('\nprocessingDateTime         =   %s' % xml.find\
            ('.//{%s}postProcessingStep' % xmlns).find\
            ('{%s}processingDateTime' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nprocessingDateTime         =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}postProcessingStep' % xmlns).find\
        ('{%s}processingAgency' % xmlns).text != None
        sys.stdout.write('\nprocessingAgency           =   %s' % xml.find\
            ('.//{%s}postProcessingStep' % xmlns).find\
            ('{%s}processingAgency' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nprocessingAgency           =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}postProcessingStep' % xmlns).find\
        ('{%s}processingStepDescription' % xmlns).text != None
        sys.stdout.write('\nprocessingStepDescription  =   %s' % xml.find\
            ('.//{%s}postProcessingStep' % xmlns).find\
            ('{%s}processingStepDescription' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nprocessingStepDescription  =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}postProcessingStep' % xmlns).find\
        ('{%s}processingStepSettings' % xmlns).text != None
        sys.stdout.write('\nprocessingStepSettings     =   %s' % xml.find\
            ('.//{%s}postProcessingStep' % xmlns).find\
            ('{%s}processingStepSettings' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nprocessingStepSettings     =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}postProcessingStep' % xmlns).find\
        ('{%s}processingSoftware' % xmlns).find\
        ('{%s}softwareCreator' % xmlns).text != None
        sys.stdout.write('\nsoftwareCreator            =   %s' % xml.find\
            ('.//{%s}postProcessingStep' % xmlns).find\
            ('{%s}processingSoftware' % xmlns).find\
            ('{%s}softwareCreator' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareCreator            =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}postProcessingStep' % xmlns).find\
        ('{%s}processingSoftware' % xmlns).find\
        ('{%s}softwareName' % xmlns).text != None
        sys.stdout.write('\nsoftwareName               =   %s' % xml.find\
            ('.//{%s}postProcessingStep' % xmlns).find\
            ('{%s}processingSoftware' % xmlns).find\
            ('{%s}softwareName' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareName               =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}postProcessingStep' % xmlns).find\
        ('{%s}processingSoftware' % xmlns).find\
        ('{%s}softwareVersion' % xmlns).text != None
        sys.stdout.write('\nsoftwareVersion            =   %s' % xml.find\
            ('.//{%s}postProcessingStep' % xmlns).find\
            ('{%s}processingSoftware' % xmlns).find\
            ('{%s}softwareVersion' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\nsoftwareVersion            =   -- NOT_DEFINED --')
    try: 
        xml.find('.//{%s}postProcessingStep' % xmlns).find\
        ('{%s}processingSoftware' % xmlns).find\
        ('{%s}applicationDescription' % xmlns).text != None
        sys.stdout.write('\napplicationDescription     =   %s' % xml.find\
            ('.//{%s}postProcessingStep' % xmlns).find\
            ('{%s}processingSoftware' % xmlns).find\
            ('{%s}applicationDescription' % xmlns).text)
    except AttributeError:
        sys.stdout.write(
            '\napplicationDescription     =   -- NOT_DEFINED --')  
    sys.stdout.write('\n')

def alto_query(alto, query):
    ''' Query ALTO xml file using XPath expressions '''
    xml, xmlns = alto_parse(alto)
    query = []
    # TODO

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
# |                   |  the beginning of the path, to indicate that it’s a  |
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

def write_output():
    ''' Write output to file(s) instead of stdout '''
    if len(output) == 0:
        sys.stdout.write()
    else:
        if args.text == True:
            output_filename = alto.name + '.txt'
            sys.stdout = open('output_filename', 'w')
        if args.metadata == True:
            output_filename = alto.name + '.md.txt'
            sys.stdout = open('output_filename', 'w')        
        if args.confidence == True:
            output_filename = alto.name + '.conf.txt'
            sys.stdout = open('output_filename', 'w')
        if args.transform == True:
            output_filename = alto.name
            sys.stdout = open('output_filename', 'w')

def web_app(alto):
    ''' Simple webapp '''
    import web
    xml, xmlns = alto_parse(alto)
    root = xml.getroot()
    # Create a webserver to serve up the requests
    urls = (
        '/', 'index',
        '/elements', 'list_elements',
        '/attributes/(.*)', 'get_attributes')
    app = web.application(urls, globals())
    # Bind to localhost port 8888
    app.run('0.0.0.0:8888')

    class list_elements:        
        def GET(self):
            output = 'elements:[';
            for child in root:
                print('child', child.tag, child.attrib)
                output += str(child.attrib) + ','
                output += ']';
                return output

    class get_attributes:
        def GET(self, elements):
            for child in root:
                if child.attrib['id'] == user:
                    return str(child.attrib)

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="ALTO Tools: simple methods to perform operations on ALTO \
        xml files",
        add_help=True,
        prog='alto_tools.py', 
        usage='python %(prog)s INPUT [options]')
    parser.add_argument('INPUT',
        help='path to ALTO file or directory containing ALTO file(s)')
    parser.add_argument('-o', '--output',
        default='',
        dest='output',
        help='path to output directory (if none specified, stdout is used)')
    parser.add_argument('-v', '--version', 
        action='version', 
        version=__version__,
        help='show version number and exit')
    parser.add_argument('-c', '--confidence',
        action ='store_true',
        default=False,
        dest='confidence',
        help='calculate page confidence of the ALTO document(s)')
    parser.add_argument('-t', '--text',
        action ='store_true',
        default=False,
        dest='text',
        help='extract text content of the ALTO document(s)')
    parser.add_argument('-m', '--metadata',
        action ='store_true',
        default=False,
        dest='metadata',
        help='extract metadata of the ALTO document(s)')
    parser.add_argument('-x', '--transform',
        dest='transform',
        help='transform ALTO document(s) to target format')
    parser.add_argument('-q', '--query',
        dest='query',
        help='query elements and attributes of the ALTO document(s)')
    parser.add_argument('-w', '--web',
        action='store_true',
        default=False,
        dest='web',
        help='start webapp')
    args=parser.parse_args()
    return(args)


def main():
    args = parse_arguments()
    for root, dirs, files in os.walk(sys.argv[1]):
        for filename in files:
            if filename.endswith('.xml') or filename.endswith('.alto'):
                altofiles = open(os.path.join(root, filename), 'r', encoding='UTF8')
                for alto in altofiles:
                    try:
                        alto_parse(alto)
                    except ET.ParseError as e:
                        sys.stdout.write('\nERROR: Failed parsing "%s" - ' % \
                            altofiles.name + str(e))
                        if args.confidence == True:
                            alto_confidence(alto)
                        elif args.text == True:
                            alto_text(alto)
                        elif args.metadata == True:
                            alto_metadata(alto)
                        elif args.transform == True:
                            alto_transform(alto, xsl)
                        elif args.query == True:
                            alto_query(alto, query)
                        elif args.web == True:
                            web_app()
                        else:
                            altofiles.close()
                            sys.stdout.write('\nNo operation specified, aborting.')


if __name__ == "__main__":
    main()
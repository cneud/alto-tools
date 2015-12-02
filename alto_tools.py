#!/usr/bin/env python
 
''' alto_tools.py: simple methods to perform operations on ALTO xml files'''

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


def alto_parse(f):
    ''' Convert ALTO xml file to element tree '''
    try:
        xml = ET.parse(f)
    except ET.ParseError as e:
        sys.stdout.write('\nERROR: Failed parsing "%s" - ' % fh.name + str(e))
    #Register known namespaces    
    namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO', 
                 'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
                 'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#'}
                 # TODO: Resolve use of xsi/xlink
    # Extract namespace from document root
    xmlns = xml.getroot().tag.split('}')[0].strip('{')
    if xmlns in namespace.values():
        return xml, xmlns
    else:
        sys.stdout.write('ERROR: File "%s" appears not to be a valid ALTO \
            file (namespace declaration missing or not registered)' % fh.name)

def alto_text(xml, xmlns):
    ''' Extract text content from ALTO xml file '''
    xml, xmlns = alto_parse(fh)
    if sys.stdout.encoding != 'UTF-8':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        # Find all TextLine elements
        for lines in xml.iterfind('.//{%s}TextLine' % xmlns):
            sys.stdout.write('\n')
            # Find all String elements
            for line in lines.findall('{%s}String' % xmlns):
                # Get value of attribute CONTENT of all String elements
                text = line.attrib.get('CONTENT') + ' '
                sys.stdout.write(text)

def alto_confidence(xml, xmlns):
    ''' Calculate word confidence score for ALTO xml file '''
    xml, xmlns = alto_parse(fh)
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
        sys.stdout.write('\nFile: %s, Confidence: %s' % (fh.name, result))

def alto_transform(xml, xmlns, xsl):
    ''' Transform ALTO xml with XSLT '''
    # Detect operating system
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

def alto_metadata(xml, xmlns):
    ''' Extract metadata from ALTO xml file '''
    xml, xmlns = alto_parse(fh)
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
    sys.stdout.write('\n\n<OCRProcessing>\n')
    try: 
        xml.find('.//{%s}OCRProcessing' % xmlns).text != None
        sys.stdout.write('\nID                         =   %s' % xml.find\
            ('.//{%s}OCRProcessing' % xmlns).attrib.get('ID'))
    except AttributeError:
        sys.stdout.write(
            '\nID                         =   -- NOT_DEFINED --')
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

def parse_arguments():
    parser = argparse.ArgumentParser(
        description="ALTO Tools: simple methods to perform operations on ALTO \
        xml files",
        add_help=True,
        prog='alto_tools.py', 
        usage='python %(prog)s INPUT OUTPUT [options]')
    parser.add_argument('INPUT',
        help='path to ALTO file or directory containing ALTO file(s)')
    parser.add_argument('OUTPUT',
        help='path to output directory (will use stdout if none given)')
    parser.add_argument('-v', '--version', 
        action='version', 
        version=__version__,
        help='show version number and exit')
    subparsers = parser.add_subparsers(
        help='supported operations')
    parser_c = subparsers.add_parser('-c', 
        help='calculate page confidence of the ALTO document(s)')
    parser_t = subparsers.add_parser('-t', 
        help='extract text content of the ALTO document(s)')
    parser_m = subparsers.add_parser('-m', 
        help='extract metadata of the ALTO document(s)')
    parser_x = subparsers.add_parser('-x', 
        help='transform ALTO document(s) to target format')
    args=parser.parse_args()
    return(args)


def main():
    args = parse_arguments()
    for root, dirs, files in os.walk(sys.argv[1]):
        for filename in files:
            if filename.endswith('.xml') or filename.endswith('.alto'):
                fh = open(os.path.join(root, filename), 'r', encoding='UTF8')
                # TODO: implement optional arguments switch
                for f in fh:
                    try:
                        parse_alto(fh)
                    except ET.ParseError as e:
                        sys.stdout.write('\nERROR: Failed parsing "%s" - ' % \
                            fh.name + str(e))
                    alto_parse(f)
                    alto_text()
                    alto_confidence()
                    alto_metadata()
                    alto_transform()
                fh.close()


if __name__ == "__main__":
    main()
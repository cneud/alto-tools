#!/usr/bin/env python
# Usage: python alto_ocr_metadata.py <altofile>

import codecs
import os
import sys
import xml.etree.ElementTree as ET


namespace = {'alto-1': 'http://schema.ccs-gmbh.com/ALTO',
             'alto-2': 'http://www.loc.gov/standards/alto/ns-v2#',
             'alto-3': 'http://www.loc.gov/standards/alto/ns-v3#'}
tree = ET.parse(sys.argv[1])
xmlns = tree.getroot().tag.split('}')[0].strip('{')
if xmlns in namespace.values():
    # Description
    sys.stdout.write('\n<Description>\n')
    try:
        tree.find('.//{%s}Description' % xmlns).find('{%s}sourceImageInformation' % xmlns).find('{%s}fileName' % xmlns).text is not None
        sys.stdout.write('\nfileName                   =   %s' % tree.find('.//{%s}Description' % xmlns).find('{%s}sourceImageInformation' % xmlns).find('{%s}fileName' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nfileName                   =   -- NOT_DEFINED --')
    try:
        tree.find('.//{%s}Description' % xmlns).find('{%s}sourceImageInformation' % xmlns).find('{%s}fileIdentifier' % xmlns).text is not None
        sys.stdout.write('\nfileIdentifier             =   %s' % tree.find('.//{%s}Description' % xmlns).find('{%s}sourceImageInformation' % xmlns).find('{%s}fileIdentifier' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nfileIdentifier             =   -- NOT_DEFINED --')
    try:
        tree.find('.//{%s}Description' % xmlns).find('{%s}sourceImageInformation' % xmlns).find('{%s}documentIdentifier' % xmlns).text is not None
        sys.stdout.write('\ndocumentIdentifier         =   %s' % tree.find('.//{%s}Description' % xmlns).find('{%s}sourceImageInformation' % xmlns).find('{%s}documentIdentifier' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\ndocumentIdentifier         =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}Description' % xmlns).find('{%s}MeasurementUnit' % xmlns).text is not None
        sys.stdout.write('\nMeasurementUnit            =   %s' % tree.find('.//{%s}Description' % xmlns).find('{%s}MeasurementUnit' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nMeasurementUnit            =   -- NOT_DEFINED --')
    # OCRProcessing 
    sys.stdout.write('\n\n<OCRProcessing>\n')
    try: 
        tree.find('.//{%s}OCRProcessing' % xmlns).text is not None
        sys.stdout.write('\nID                         =   %s' % tree.find('.//{%s}OCRProcessing' % xmlns).attrib.get('ID'))
    except AttributeError:
        sys.stdout.write('\nID                         =   -- NOT_DEFINED --')
    # preProcessingStep
    sys.stdout.write('\n\n<preProcessingStep>\n')
    try: 
        tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingDateTime' % xmlns).text is not None
        sys.stdout.write('\nprocessingDateTime         =   %s' % tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingDateTime' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nprocessingDateTime         =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingAgency' % xmlns).text is not None
        sys.stdout.write('\nprocessingAgency           =   %s' % tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingAgency' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nprocessingAgency           =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingStepDescription' % xmlns).text is not None
        sys.stdout.write('\nprocessingStepDescription  =   %s' % tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingStepDescription' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nprocessingStepDescription  =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingStepSettings' % xmlns).text is not None
        sys.stdout.write('\nprocessingStepSettings     =   %s' % tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingStepSettings' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nprocessingStepSettings     =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareCreator' % xmlns).text is not None
        sys.stdout.write('\nsoftwareCreator            =   %s' % tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareCreator' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nsoftwareCreator            =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareName' % xmlns).text is not None
        sys.stdout.write('\nsoftwareName               =   %s' % tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareName' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nsoftwareName               =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareVersion' % xmlns).text is not None
        sys.stdout.write('\nsoftwareVersion            =   %s' % tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareVersion' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nsoftwareVersion            =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}applicationDescription' % xmlns).text is not None
        sys.stdout.write('\napplicationDescription     =   %s' % tree.find('.//{%s}preProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}applicationDescription' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\napplicationDescription     =   -- NOT_DEFINED --')
    # ocrProcessingStep
    sys.stdout.write('\n\n<ocrProcessingStep>\n')
    try: 
        tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingDateTime' % xmlns).text is not None
        sys.stdout.write('\nprocessingDateTime         =   %s' % tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingDateTime' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nprocessingDateTime         =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingAgency' % xmlns).text is not None
        sys.stdout.write('\nprocessingAgency           =   %s' % tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingAgency' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nprocessingAgency           =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingStepDescription' % xmlns).text is not None
        sys.stdout.write('\nprocessingStepDescription  =   %s' % tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingStepDescription' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nprocessingStepDescription  =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingStepSettings' % xmlns).text is not None
        sys.stdout.write('\nprocessingStepSettings     =   %s' % tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingStepSettings' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nprocessingStepSettings     =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareCreator' % xmlns).text is not None
        sys.stdout.write('\nsoftwareCreator            =   %s' % tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareCreator' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nsoftwareCreator            =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareName' % xmlns).text is not None
        sys.stdout.write('\nsoftwareName               =   %s' % tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareName' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nsoftwareName               =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareVersion' % xmlns).text is not None
        sys.stdout.write('\nsoftwareVersion            =   %s' % tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareVersion' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nsoftwareVersion            =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}applicationDescription' % xmlns).text is not None
        sys.stdout.write('\napplicationDescription     =   %s' % tree.find('.//{%s}ocrProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}applicationDescription' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\napplicationDescription     =   -- NOT_DEFINED --')  
    # postProcessingStep
    sys.stdout.write('\n\n<postProcessingStep>\n')
    try: 
        tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingDateTime' % xmlns).text is not None
        sys.stdout.write('\nprocessingDateTime         =   %s' % tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingDateTime' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nprocessingDateTime         =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingAgency' % xmlns).text is not None
        sys.stdout.write('\nprocessingAgency           =   %s' % tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingAgency' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nprocessingAgency           =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingStepDescription' % xmlns).text is not None
        sys.stdout.write('\nprocessingStepDescription  =   %s' % tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingStepDescription' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nprocessingStepDescription  =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingStepSettings' % xmlns).text is not None
        sys.stdout.write('\nprocessingStepSettings     =   %s' % tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingStepSettings' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nprocessingStepSettings     =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareCreator' % xmlns).text is not None
        sys.stdout.write('\nsoftwareCreator            =   %s' % tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareCreator' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nsoftwareCreator            =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareName' % xmlns).text is not None
        sys.stdout.write('\nsoftwareName               =   %s' % tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareName' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nsoftwareName               =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareVersion' % xmlns).text is not None
        sys.stdout.write('\nsoftwareVersion            =   %s' % tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}softwareVersion' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\nsoftwareVersion            =   -- NOT_DEFINED --')
    try: 
        tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}applicationDescription' % xmlns).text is not None
        sys.stdout.write('\napplicationDescription     =   %s' % tree.find('.//{%s}postProcessingStep' % xmlns).find('{%s}processingSoftware' % xmlns).find('{%s}applicationDescription' % xmlns).text)
    except AttributeError:
        sys.stdout.write('\napplicationDescription     =   -- NOT_DEFINED --')  
    sys.stdout.write('\n')
else:
    print('ERROR: Not a valid ALTO file (namespace declaration missing)')
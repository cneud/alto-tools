# alto-ocr-confidence
Calculates the OCR confidence score per page in [ALTO](http://www.loc.gov/standards/alto/) files. 

The method used is really simple:
* find all String elements
* get value of attribute "([WC](https://github.com/altoxml/schema/blob/master/v2/alto-2-0.xsd#L381))" (word confidence) for each String
* calculate sum of all "WC" values
* divide sum by the count of words per page

Use like:

    python alto_ocr_confidence.py <inputdir>

Example output:

    File: alto\AZ_1926_04_25_0001.xml, Confidence: 54.13

_Note that **OCR confidence** (which is a native output of the OCR engine) is NOT equal to the actual **OCR accuracy**, which can only be determined by evaluation against Ground Truth._

_Read more about OCR evaluation [here](https://sites.google.com/site/textdigitisation/qualitymeasures)._

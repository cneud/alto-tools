# alto-ocr-confidence
Calculates the OCR confidence score per page in [ALTO](http://www.loc.gov/standards/alto/) files.

Use like:

    python alto_ocr_confidence.py <inputdir>

Example output:

    File: alto\AZ_1926_04_25_0001.xml, Confidence: 54.13

_Note that **OCR confidence** (which is a native output of the OCR engine) is NOT equal to the actual **OCR accuracy**, which can only be determined by evaluation against Ground Truth._

_Read more about OCR evaluation [here](https://sites.google.com/site/textdigitisation/qualitymeasures)._

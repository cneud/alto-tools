# alto-tools

> [Python3](https://www.python.org/) script for performing various operations on [ALTO](http://www.loc.gov/standards/alto/) files.

## Usage

* extract UTF-8 text content from ALTO file

  `python3 alto_tools.py alto.xml -t`

* extract page OCR confidence score from ALTO file

  `python3 alto_tools.py alto.xml -c`

* extract bounding boxes of illustrations from ALTO file

  `python3 alto_tools.py alto.xml -l`

## Planned

* write output to file(s) - currently all output is sent to `stdout`

  `python3 alto-tools.py alto.xml [OPTION] -o`

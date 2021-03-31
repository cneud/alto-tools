# alto-tools

[![image](https://travis-ci.org/cneud/alto-tools.svg?branch=master)](https://travis-ci.org/cneud/alto-tools)

**Warning: not fully implemented - work in progress**

> [Python3](https://www.python.org/) script for performing various operations on [ALTO](http://www.loc.gov/standards/alto/) files.

## Usage

* extract **text** content from ALTO document(s)  

  `python3 alto-tools.py alto.xml -t`

* extract **confidence** score from ALTO document(s)  

  `python3 alto-tools.py alto.xml -c`

* extract **graphical elements** from ALTO document(s)  

  `python3 alto-tools.py alto.xml -g`

## Planned

* write **output** to file(s) - currently all output is sent to `stdout`   

  `python3 alto-tools.py alto.xml [OPTION] -o output`

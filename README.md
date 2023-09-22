# alto-tools
> simple, fast [Python3](https://www.python.org/) tools for performing various operations on [ALTO](http://www.loc.gov/standards/alto/) XML files

<!-- [![PyPI Version](https://img.shields.io/pypi/v/alto-tools.svg)](https://pypi.org/project/alto-tools/) -->
[![GH Actions Test](https://github.com/cneud/alto-tools/actions/workflows/tests.yml/badge.svg)](https://github.com/cneud/alto-tools/actions/workflows/tests.yml)
[![License: ASL](https://img.shields.io/github/license/cneud/alto-tools)](https://opensource.org/license/apache-2-0/)

## Installation

Clone the repository and run

```bash
pip install .
```

There are zero dependencies, so in principle this should work cross-platform.

## Usage

Extract text content from ALTO file

```bash
alto-tools alto.xml -t
```

Extract OCR confidence score from ALTO file

```bash
alto-tools alto.xml -c
```

Extract bounding boxes of image regions from ALTO file

```bash
alto-tools alto.xml -l
```

All output is sent to `stdout`.

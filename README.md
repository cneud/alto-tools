# alto-tools

> [Python3](https://www.python.org/) tools for performing various operations on [ALTO](http://www.loc.gov/standards/alto/) XML files

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

Extract bounding boxes of illustrations from ALTO file

```bash
alto-tools alto.xml -l
```

All output is sent to `stdout`.

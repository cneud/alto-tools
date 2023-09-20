# alto-tools

> [Python](https://www.python.org/) (v3) script for performing various operations on [ALTO](http://www.loc.gov/standards/alto/) files.

## Usage

Extract text content from ALTO file

```bash
python alto_tools.py alto.xml -t
```

Extract OCR confidence score from ALTO file

```bash
python alto_tools.py alto.xml -c
```

Extract bounding boxes of illustrations from ALTO file

```bash
python alto_tools.py alto.xml -l
```

All output is sent to `stdout`.

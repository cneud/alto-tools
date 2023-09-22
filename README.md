<h3 align="center">alto-tools</h3>
<p align="center">
  <a href="https://www.python.org/">:snake:</a> tools for performing various operations on <a href="http://www.loc.gov/standards/alto/">ALTO</a> XML files
</p>
<p align="center">
  <!--<a href="pypi.org/project/alto-tools/"><img src="https://img.shields.io/pypi/v/alto-tools.svg" title="PyPI Version"></a>-->
  <a href="https://github.com/cneud/alto-tools/actions/workflows/tests.yml"><img src="https://github.com/cneud/alto-tools/actions/workflows/tests.yml/badge.svg" title="GitHub Actions Tests Status"></a>
  <a href="https://opensource.org/license/apache-2-0/"><img src="https://img.shields.io/github/license/cneud/alto-tools" title="Apache Software License 2.0"></a>
</p>

---

## Installation

Clone the repository and run

```bash
pip install .
```

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

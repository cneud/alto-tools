<h3 align="center">ALTO Tools</h3>
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

Clone the repository, enter it and run

```bash
pip install .
```

## Usage

```bash
alto-tools <INPUT> [OPTION] 
```

`INPUT` should be the path to an ALTO file or directory containing ALTO files.

Output is sent to `stdout`.

| OPTION | Description |
|--------|:------------|
| `-t` `--text`  | Extract UTF-8 encoded text content |
| `-c` `--confidence`  | Extract mean OCR word confidence score |
| `-i` `--illustrations`  | Extract bounding box coordinates of `<Illustration>` elements |
| `-g` `--graphics`  | Extract bounding box coordinates of `<GraphicalElement>` elements |

#!/usr/bin/env python

""" ALTO Tools: simple tools for performing various operations on ALTO xml files """

from __future__ import annotations
import argparse
import codecs
import io
import os
import re
import sys
from typing import Callable, Iterable
import xml.etree.ElementTree as ET

__version__ = "0.1.0"


def alto_parse(alto, **kargs):
    """Convert ALTO xml file to element tree"""
    xml = None
    try:
        xml = ET.parse(alto, **kargs)
    except ET.ParseError as e:
        print(f"Parser Error in file '{alto}': {e}")
    # Register ALTO namespaces
    namespace = {
        "alto-1": "http://schema.ccs-gmbh.com/ALTO",
        "alto-1-xsd": "http://schema.ccs-gmbh.com/ALTO/alto-1-4.xsd",
        "alto-2": "http://www.loc.gov/standards/alto/ns-v2#",
        "alto-2-xsd": "https://www.loc.gov/standards/alto/alto.xsd",
        "alto-3": "http://www.loc.gov/standards/alto/ns-v3#",
        "alto-3-xsd": "http://www.loc.gov/standards/alto/v3/alto.xsd",
        "alto-4": "http://www.loc.gov/standards/alto/ns-v4#",
        "alto-4-xsd": "http://www.loc.gov/standards/alto/v4/alto.xsd",
        "alto-bnf": "http://bibnum.bnf.fr/ns/alto_prod",
        "alto-bnf-xsd": "http://bibnum.bnf.fr/ns/alto_prod.xsd",
    }
    # Extract namespace from document root
    if "http://" in str(xml.getroot().tag.split("}")[0].strip("{")):
        xmlns = xml.getroot().tag.split("}")[0].strip("{")
    else:
        try:
            ns = xml.getroot().attrib
            xmlns = str(ns).split(" ")[1].strip("}").strip("'")
        except IndexError:
            sys.stderr.write(
                f'\nERROR: File "{alto.name}": no namespace declaration found.'
            )
            xmlns = "no_namespace_found"
    if xmlns in namespace.values():
        return alto, xml, xmlns
    else:
        sys.stdout.write(
            f'\nERROR: File "{alto.name}": namespace {xmlns} is not registered.\n'
        )


def alto_text(xml, xmlns):
    """Extract text content from ALTO xml file"""
    text = None
    # Ensure use of UTF-8
    if isinstance(sys.stdout, io.TextIOWrapper) and sys.stdout.encoding != "UTF-8":
        sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, "strict")
    # Find all <TextLine> elements
    for lines in xml.iterfind(".//{%s}TextLine" % xmlns):
        # New line after every <TextLine> element
        sys.stdout.write("\n")
        # Find all <String> elements
        for line in lines.findall("{%s}String" % xmlns):
            # Check if there are no hyphenated words
            if "SUBS_CONTENT" not in line.attrib and "SUBS_TYPE" not in line.attrib:
                # Get value of attribute @CONTENT from all <String> elements
                text = line.attrib.get("CONTENT") + " "
            else:
                #  Handling of hyphenation to avoid duplicates, see
                #  https://github.com/cneud/alto-tools/issues/16
                if "HypPart1" in line.attrib.get("SUBS_TYPE"):
                    # Get the first part of the hyphenated word from @CONTENT
                    # (instead of using @SUBS_CONTENT)
                    if "HypPart1" in line.attrib.get("SUBS_TYPE"):
                        text = line.attrib.get("CONTENT")
                    # Concatenate second part of the hyphenated word from @CONTENT
                    if "HypPart2" in line.attrib.get("SUBS_TYPE"):
                        text = line.attrib.get("CONTENT") + " "
            sys.stdout.write(text)


def alto_illustrations(alto, xml, xmlns):
    """Extract bounding box coordinates of illustration regions from ALTO xml file"""
    # Find all <Illustration> elements
    for illustration in xml.iterfind(".//{%s}Illustration" % xmlns):
        # Get @ID of <Illustration> element
        illustration_id = illustration.attrib.get("ID")
        # Get coordinates of <Illustration> element
        illustration_coords = (
            illustration.attrib.get("HEIGHT")
            + ","
            + illustration.attrib.get("WIDTH")
            + ","
            + illustration.attrib.get("VPOS")
            + ","
            + illustration.attrib.get("HPOS")
        )
        illustrations = illustration_id + "=" + illustration_coords
        sys.stdout.write(f"\nFile: {alto.name}, Illustration: {illustrations}")


def alto_graphics(alto, xml, xmlns):
    """Extract bounding box coordinates of graphical elements from ALTO xml file"""
    # Find all <GraphicalElement> elements
    for graphic in xml.iterfind(".//{%s}GraphicalElement" % xmlns):
        # Get @ID of <GraphicalElement> element
        graphic_id = graphic.attrib.get("ID")
        # Get coordinates of <GraphicalElement> element
        graphic_coords = (
            graphic.attrib.get("HEIGHT")
            + ","
            + graphic.attrib.get("WIDTH")
            + ","
            + graphic.attrib.get("VPOS")
            + ","
            + graphic.attrib.get("HPOS")
        )
        graphics = graphic_id + "=" + graphic_coords
        sys.stdout.write(f"\nFile: {alto.name}, GraphicalElement: {graphics}")


def alto_confidence(alto, xml, xmlns):
    """Calculate mean word confidence score for ALTO xml file"""
    score = 0
    count = 0
    # Find all <String> elements
    for conf in xml.iterfind(".//{%s}String" % xmlns):
        # Get value of attribute @WC (Word Confidence) of all <String> elements
        wc = conf.attrib.get("WC")
        # Calculate sum of all @WC values as float
        if wc is not None:
            score += float(wc)
            # Increment counter for each word
            count += 1
    # Divide sum of @WC values by number of words
    if count > 0:
        confidence = score / count
        result = round(100 * confidence, 2)
        sys.stdout.write(f"\nFile: {alto.name}, Confidence: {result}")
        return result
    else:
        sys.stdout.write(f"\nFile: {alto.name}, Confidence: 00.00")
        return 0


def alto_statistics(alto, xml, xmlns):
    """Extract statistical information from ALTO xml file"""
    no_textlines = 0
    no_strings = 0
    no_glyphs = 0
    no_illustrations = 0
    no_graphics = 0
    for textlines in xml.iterfind(".//{%s}TextLine" % xmlns):
        no_textlines += 1
    for strings in xml.iterfind(".//{%s}String" % xmlns):
        no_strings += 1
    for glyphs in xml.iterfind(".//{%s}Glyph" % xmlns):
        no_glyphs += 1
    for illustrations in xml.iterfind(".//{%s}Illustration" % xmlns):
        no_illustrations += 1
    for graphics in xml.iterfind(".//{%s}GraphicalElement" % xmlns):
        no_graphics += 1
    sys.stdout.write(f"\nFile: {alto.name}, Statistics:")
    sys.stdout.write(f"\n# of <TextLine> elements: {no_textlines}")
    sys.stdout.write(f"\n# of <String> elements: {no_strings}")
    sys.stdout.write(f"\n# of <Glyph> elements: {no_glyphs}")
    sys.stdout.write(f"\n# of <Illustration> elements: {no_illustrations}")
    sys.stdout.write(f"\n# of <GraphicalElement> elements: {no_graphics}")
    return {
        'textlines': no_textlines,
        'strings': no_strings,
        'glyphs': no_glyphs,
        'illustrations': no_illustrations,
        'graphics': no_graphics
    }


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="ALTO Tools: simple tools for performing various operations on ALTO xml files",
        add_help=True,
        prog="alto_tools.py",
        usage="python %(prog)s INPUT [option]",
    )
    parser.add_argument(
        "INPUT", nargs="+", help="path to ALTO file or directory containing ALTO files"
    )
    g = parser.add_mutually_exclusive_group()
    g.add_argument(
        "-v",
        "--version",
        action="version",
        version=__version__,
        help="show version number and exit",
    )
    g.add_argument(
        "-c",
        "--confidence",
        action="store_true",
        default=False,
        dest="confidence",
        help="extract mean OCR word confidence score",
    )
    g.add_argument(
        "-t",
        "--text",
        action="store_true",
        default=False,
        dest="text",
        help="extract UTF8-encoded text content",
    )
    g.add_argument(
        "-i",
        "--illustrations",
        action="store_true",
        default=False,
        dest="illustrations",
        help="extract bounding boxes of illustrations",
    )
    g.add_argument(
        "-g",
        "--graphics",
        action="store_true",
        default=False,
        dest="graphics",
        help="extract bounding boxes of graphical elements",
    )
    g.add_argument(
        "-s",
        "--statistics",
        action="store_true",
        default=False,
        dest="statistics",
        help="extract statistical information",
    )
    parser.add_argument(
        "-x",
        "--xml-encoding",
        default=None,
        dest="xml_encoding",
        help="XML encoding",
    )
    parser.add_argument(
        "-e",
        "--file-encoding",
        default="UTF-8",
        dest="file_encoding",
        help="file encoding",
    )
    args = parser.parse_args()
    return args


def walker(
    inputs: Iterable[str],
    fnfilter: Callable[[str], bool] = lambda fn: True,
) -> Iterable[str]:
    """
    Returns all file names in inputs, and recursively for directories.

    If an input is
    - a file:      return as is
    - a directory: return all files in it, recursively, filtered by fnfilter.
    """
    for i in inputs:
        if os.path.isfile(i):
            yield i
        else:
            for root, _, files in os.walk(i):
                for f in filter(fnfilter, files):
                    yield os.path.join(root, f)


def open_input_file(
    filename: str,
    args: argparse.Namespace,
) -> tuple[io.TextIOWrapper | str, ET.ElementTree, dict[str, str] | str] | None:
    try:
        if args.xml_encoding:
            xml_encoding = args.xml_encoding
            if xml_encoding == "auto":
                with open(filename, "rb") as f:
                    m = re.search('encoding="(.*?)"', f.read(45).decode("utf-8"))
                    xml_encoding = m.group(1)
            xmlp = ET.XMLParser(encoding=xml_encoding)
            alto, xml, xmlns = alto_parse(filename, parser=xmlp)
        else:
            with open(filename, "r", encoding=args.file_encoding) as alto:
                alto, xml, xmlns = alto_parse(alto)
    except IndexError:
        return None
    except ET.ParseError as e:
        print("Error parsing %s" % filename, file=sys.stderr)
        raise e
    return alto, xml, xmlns


def _read_from_stdin() -> (
    Iterable[tuple[io.TextIOWrapper | str, ET.ElementTree, dict[str, str] | str]]
):
    if os.isatty(0):
        return
    assert isinstance(sys.stdin, io.TextIOWrapper)
    parsing_result = alto_parse(sys.stdin)
    if not parsing_result:
        return
    yield parsing_result


def open_input_files(
    args: argparse.Namespace,
) -> Iterable[tuple[io.TextIOWrapper | str, ET.ElementTree, dict[str, str] | str]]:
    if "-" in args.INPUT:
        yield from _read_from_stdin()
    fnfilter = lambda fn: fn.endswith(".xml") or fn.endswith(".alto")
    for filename in walker(args.INPUT, fnfilter):
        parsing_result = open_input_file(filename, args)
        if not parsing_result:
            continue
        alto, xml, xmlns = parsing_result
        yield (alto, xml, xmlns)
        if isinstance(alto, str):
            continue
        alto.close()


def main() -> None:
    if sys.version_info < (3, 0):
        sys.stdout.write("Python 3 is required.\n")
        sys.exit(-1)

    args = parse_arguments()
    if not len(sys.argv) > 2:
        sys.stdout.write("\nNo operation specified, ")
        os.system("python alto_tools.py -h")
        sys.exit(-1)
    else:
        confidence_sum = 0.
        number_of_files = 0
        for alto, xml, xmlns in open_input_files(args):
            number_of_files += 1
            if args.confidence:
                confidence_sum += alto_confidence(alto, xml, xmlns)
            if args.text:
                alto_text(xml, xmlns)
            if args.illustrations:
                alto_illustrations(alto, xml, xmlns)
            if args.graphics:
                alto_graphics(alto, xml, xmlns)
            if args.statistics:
                alto_statistics(alto, xml, xmlns)
        if number_of_files >= 2 and args.confidence:
            print(
                f"\n\nConfidence of folder: {round(confidence_sum / number_of_files, 2)}"
            )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import argparse
import re
import sys
import xml.etree.ElementTree

# Author: mail@HeikoBehrens.net, 2020-01-08
#
# Works around two bugs in the SVG export of FreeCAD 0.18.
#
# Bug 1) incorrect formats length attributes which
# separate a number and unit literal with a space, e.g. "0.35 px".
#
# According to https://www.w3.org/TR/SVG/coords.html#Units,
#   https://www.w3.org/TR/css-values/#absolute-lengths
#   https://developer.mozilla.org/en-US/docs/Web/CSS/length#syntax
# this is incorrect as
#   > there is no space between the unit literal and the number.
# Shaper Origin rejects the file with
#   > Unable to place design. Check that your file is formatted properly.
#
# Bug 2) invalid CSS style "fill-rule". This is not a CSS style property
# but an SVG attribute.
#   https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule
# For the time being, the property is simply removed.


# https://developer.mozilla.org/en-US/docs/Web/CSS/number
# https://developer.mozilla.org/en-US/docs/Web/CSS/length#syntax
RE_LENGTH_WITH_UNIT = re.compile(r'^\s*([+-]?)(\d*\.)?(\d+)([Ee][+-]?\d+)?\s*(cm|mm|Q|in|pc|pt|px)\s*$')


def length_value_without_spaces(value):
    m = RE_LENGTH_WITH_UNIT.match(value)
    if not m:
        return value

    return value.replace(" ", "")


def style_attribute_without_fill_rule(value):
    props = value.split(";")
    props_without_fill_rule = [p for p in props if not p.strip().startswith("fill-rule") and p.strip()]
    return ";".join(props_without_fill_rule) + (";" if len(props_without_fill_rule) > 0 else "")


def fixup_element(element):
    for k, v in element.attrib.items():
        if k == "style":
            new_value = style_attribute_without_fill_rule(v)
        else:
            new_value = length_value_without_spaces(v)

        if new_value != v:
            element.attrib[k] = new_value


def fixup_svg(infile, outfile):
    xml.etree.ElementTree.register_namespace("", "http://www.w3.org/2000/svg")
    svg = xml.etree.ElementTree.parse(infile)
    for elem in svg.iter():
        fixup_element(elem)
    svg.write(outfile, encoding='unicode', xml_declaration=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    args = parser.parse_args()

    fixup_svg(infile=args.infile, outfile=args.outfile)

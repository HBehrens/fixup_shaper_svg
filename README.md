[![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/hbehrens/fixup_shaper_svg/python_tests.yml?label=tests&link=https%3A%2F%2Fgithub.com%2FHBehrens%2Ffixup_shaper_svg%2Factions%2Fworkflows%2Fpython_tests.yml)](https://github.com/HBehrens/fixup_shaper_svg/actions/workflows/python_tests.yml)
![Static Badge](https://img.shields.io/badge/platform-macos_%7C_linux_%7C_windows-blue)
![Static Badge](https://img.shields.io/badge/python-3.8_%7C_3.11-blue?logo=python&logoColor=white)

Works around two bugs in the SVG export of [FreeCAD (0.18)](https://freecadweb.org) as
[Shaper Origin (Humboldt)](https://www.shapertools.com) rejects the file with

  > Unable to place design. Check that your file is formatted properly.

Probably related to [this discussion at the FreeCAD forum](https://forum.freecadweb.org/viewtopic.php?style=10&f=3&t=45416).

# Usage

Call the script from the terminal

```
python3 fixup_shaper_svg.py freecad_export.svg compatible_with_shaper.svg
```

To process an SVG and patch elements that cause Shaper Origin to reject the file.
The following incorrect SVG constructs are corrected by the script: 

## Patched Bug 1
incorrect formats length attributes which
separate a number and unit literal with a space, e.g. "0.35 px".

According to https://www.w3.org/TR/SVG/coords.html#Units,
  https://www.w3.org/TR/css-values/#absolute-lengths
  https://developer.mozilla.org/en-US/docs/Web/CSS/length#syntax
this is incorrect as
  > there is no space between the unit literal and the number.

## Patched Bug 2 
invalid CSS style "fill-rule". This is not a CSS style property
but an SVG attribute.
  https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/fill-rule
For the time being, the property is simply removed.

# Running Tests

Run the unit-tests via

```
python3 fixup_shaper_svg_tests.py
```

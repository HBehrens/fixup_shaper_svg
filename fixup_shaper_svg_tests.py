import unittest

from fixup_shaper_svg import length_value_without_spaces, style_attribute_without_fill_rule


class LengthWithUnit(unittest.TestCase):
    def test_number_formats(self):
        self.assertEqual("12cm", length_value_without_spaces("12 cm"))
        self.assertEqual("4.01mm", length_value_without_spaces("4.01 mm"))
        self.assertEqual("-456.8Q", length_value_without_spaces("-456.8 Q"))
        self.assertEqual("0.0in", length_value_without_spaces("0.0 in"))
        self.assertEqual("+0.0pc", length_value_without_spaces("+0.0 pc"))
        self.assertEqual("-0.0pt", length_value_without_spaces("-0.0 pt"))
        self.assertEqual(".60px", length_value_without_spaces(".60 px"))
        self.assertEqual("10e3px", length_value_without_spaces("10e3 px"))
        self.assertEqual("-3.4e-2px", length_value_without_spaces("-3.4e-2 px"))

    def test_spacing(self):
        self.assertEqual("0.35px", length_value_without_spaces("0.35px"))
        self.assertEqual("0.35px", length_value_without_spaces("0.35  px"))
        self.assertEqual("0.35px", length_value_without_spaces("  0.35px"))
        self.assertEqual("0.35px", length_value_without_spaces("0.35px  "))
        self.assertEqual("0.35px", length_value_without_spaces("  0.35  px  "))

    def test_ignore_invalid_numbers(self):
        self.assertEqual("12. px", length_value_without_spaces("12. px"))
        self.assertEqual("+-12.2 px", length_value_without_spaces("+-12.2 px"))
        self.assertEqual("12.1.1 px", length_value_without_spaces("12.1.1 px"))

    def test_ignores_complex_attributes(self):
        self.assertEqual("stroke-width:0.35 px;stroke-miterlimit:4 pt;",
                         length_value_without_spaces("stroke-width:0.35 px;stroke-miterlimit:4 pt;"))


class StyleWithUnsupportedAttributes(unittest.TestCase):
    def test_removes_fill_rule(self):
        self.assertEqual("stroke-width:0.35;",
                         style_attribute_without_fill_rule("stroke-width:0.35;fill-rule: evenodd"))
        self.assertEqual("fill:  none  ;",
                         style_attribute_without_fill_rule("  fill-rule: evenodd;fill:  none  ;  "))
        self.assertEqual("",
                         style_attribute_without_fill_rule(" fill-rule: evenodd; "))


if __name__ == '__main__':
    unittest.main()

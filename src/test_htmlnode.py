import unittest

from htmlnode import HTMLNode

prop_dict1 = {
    "href": "https://www.google.com",
    "target": "_blank",
}

prop_dict2 = {
    "href": "https://www.boot.dev",
    "target": "_blank",
}

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("p", "text inside paragraph", None, prop_dict1)
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html2(self):
        node = HTMLNode("p", "text inside paragraph", None, prop_dict2)
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev" target="_blank"')

    def test_props_to_html3(self):
        node = HTMLNode(None, None, None, prop_dict2)
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), None)
    


if __name__ == "__main__":
    unittest.main()
import unittest

from htmlnode import *
from textnode import *

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
        self.assertEqual(node.props_to_html(), "")
    
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_grandchildren_links(self):
        grandchild_node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            '<div><span><a href="https://www.google.com">Click me!</a></span></div>',
        )
    
    #The below HTML doesn't make sense, but for testing purposes...
    def test_to_html_with_parent_props(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node], {"href": "https://www.google.com"})
        self.assertEqual(
            parent_node.to_html(),
            '<div href="https://www.google.com"><span><b>grandchild</b></span></div>',
        )

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold_to_html_node(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node).to_html()
        self.assertEqual(html_node, "<b>This is a bold node</b>")

    def test_link_text_to_html_node(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.google.com")
        html_node = text_node_to_html_node(node).to_html()
        self.assertEqual(html_node, '<a href="https://www.google.com">This is a link node</a>')

    def test_img_text_to_html_node(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.google.com")
        html_node = text_node_to_html_node(node).to_html()
        self.assertEqual(html_node, '<img src="https://www.google.com" alt="This is an image node" />')


if __name__ == "__main__":
    unittest.main()
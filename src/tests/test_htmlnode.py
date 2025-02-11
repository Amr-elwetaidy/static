import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("div", "Hello, world!")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_props_to_html(self):
        node = HTMLNode("div", "Hello, world!", props={"class": "test"})
        self.assertEqual(node.props_to_html(), "class='test'")

    def test_repr(self):
        node = HTMLNode("div", "Hello, world!", props={"class": "test"})
        self.assertEqual(
            repr(node),
            "HTMLNode(tag=div, value=Hello, world!, children=None, props={'class': 'test'})",
        )

    def test_leaf_node_no_children(self):
        node = LeafNode("div", "Hello, world!")
        self.assertEqual(node.children, None)

    def test_leaf_node_to_html(self):
        node = LeafNode("div", "Hello, world!")
        self.assertEqual(node.to_html(), "<div>Hello, world!</div>")

    def test_leaf_node_repr(self):
        node = LeafNode("div", "Hello, world!")
        self.assertEqual(
            repr(node), "HTMLNode(tag=div, value=Hello, world!, children=None, props=None)"
        )

    def test_parent_node_no_children(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_no_tag(self):
        node = ParentNode(None, [LeafNode("span", "Hello, world!")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_node_to_html(self):
        node = ParentNode("div", [LeafNode("span", "Hello, world!")])
        self.assertEqual(node.to_html(), "<div><span>Hello, world!</span></div>")

    def test_parent_node_to_html_many_children(self):
        node = ParentNode("div", [LeafNode("span", "Hello, world!"), LeafNode("span", "Hello, world!")])
        self.assertEqual(node.to_html(), "<div><span>Hello, world!</span><span>Hello, world!</span></div>")

    def test_parent_node_nested(self):
        node = ParentNode("div", [ParentNode("span", [LeafNode("span", "Hello, world!")])])
        self.assertEqual(node.to_html(), "<div><span><span>Hello, world!</span></span></div>")


if __name__ == "__main__":
    unittest.main()

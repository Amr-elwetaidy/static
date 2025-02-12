import unittest

from src import main
from src.textnode import TextNode, TextType


class TestMain(unittest.TestCase):
    def test_text_node_to_html_node(self):
        text_node = TextNode("Hello, world!", TextType.TEXT)
        html_node = main.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.to_html(), "Hello, world!")

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("Hello, world!", TextType.BOLD)
        html_node = main.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.to_html(), "<b>Hello, world!</b>")

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("Hello, world!", TextType.ITALIC)
        html_node = main.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.to_html(), "<i>Hello, world!</i>")

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("Hello, world!", TextType.CODE)
        html_node = main.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.to_html(), "<code>Hello, world!</code>")

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("Hello, world!", TextType.LINK, "https://example.com")
        html_node = main.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Hello, world!")
        self.assertEqual(html_node.props, {"href": "https://example.com"})
        self.assertEqual(html_node.to_html(), "<a href='https://example.com'>Hello, world!</a>")

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("Hello, world!", TextType.IMAGE, "https://example.com")
        html_node = main.text_node_to_html_node(text_node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://example.com", "alt": "Hello, world!"})
        self.assertEqual(html_node.to_html(), "<img src='https://example.com' alt='Hello, world!'></img>")

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = main.text_to_textnodes(text)
        self.assertEqual(len(nodes), 10)


if __name__ == "__main__":
    unittest.main()

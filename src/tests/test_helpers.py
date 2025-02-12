import unittest

from src import helpers
from src.textnode import TextNode, TextType


class TestHelpers(unittest.TestCase):
    def test_split_nodes_delimiter(self):
        text_node = TextNode("This is text with a `code block` word", TextType.TEXT)
        nodes = helpers.split_nodes_delimiter([text_node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 3)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.CODE)

    def test_split_nodes_delimiter_multiple(self):
        text_node = TextNode("This is text with a `code block` word and a `code block 2` word", TextType.TEXT)
        nodes = helpers.split_nodes_delimiter([text_node], "`", TextType.CODE)
        self.assertEqual(len(nodes), 5)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.CODE)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)
        self.assertEqual(nodes[3].text_type, TextType.CODE)
        self.assertEqual(nodes[4].text_type, TextType.TEXT)

    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        images = helpers.extract_markdown_images(text)
        self.assertEqual(len(images), 2)
        self.assertEqual(images[0], ("rick roll", "https://i.imgur.com/aKaOqIh.gif"))
        self.assertEqual(images[1], ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"))

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = helpers.extract_markdown_links(text)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0], ("to boot dev", "https://www.boot.dev"))
        self.assertEqual(links[1], ("to youtube", "https://www.youtube.com/@bootdotdev"))

    def test_split_nodes_image(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        nodes = helpers.split_nodes_image([TextNode(text, TextType.TEXT)])
        self.assertEqual(len(nodes), 4)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.IMAGE)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_split_nodes_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        nodes = helpers.split_nodes_link([TextNode(text, TextType.TEXT)])
        self.assertEqual(len(nodes), 4)
        self.assertEqual(nodes[0].text_type, TextType.TEXT)
        self.assertEqual(nodes[1].text_type, TextType.LINK)
        self.assertEqual(nodes[2].text_type, TextType.TEXT)

    def test_block_to_block_type(self):
        self.assertEqual(helpers.block_to_block_type("# This is a heading"), "heading")
        self.assertEqual(helpers.block_to_block_type("```python\nprint('Hello, world!')```"), "code")
        self.assertEqual(helpers.block_to_block_type("> This is a quote"), "quote")
        self.assertEqual(helpers.block_to_block_type("* This is a list item"), "unordered_list")
        self.assertEqual(helpers.block_to_block_type("1. This is a list item"), "ordered_list")


if __name__ == "__main__":
    unittest.main()

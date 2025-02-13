import re
from typing import Any

from htmlnode import LeafNode, ParentNode
from textnode import TextNode, TextType


def validate_node(node: TextNode | Any, nodes: list[TextNode]):
    if not isinstance(node, TextNode):
        return False
    if node.text_type != TextType.TEXT:
        nodes.append(node)
        return False
    return True


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if not validate_node(node, new_nodes):
            continue

        parts = re.split(delimiter, node.text)
        for i, part in enumerate(parts):
            if not part:
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                new_nodes.append(TextNode(part, text_type))

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if not validate_node(node, new_nodes):
            continue

        parts = re.split(r"(\!\[.*?\]\(.*?\))", node.text)
        for i, part in enumerate(parts):
            if not part:
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                alt, url = extract_markdown_images(part)[0]
                new_nodes.append(TextNode(alt, TextType.IMAGE, url))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if not validate_node(node, new_nodes):
            continue

        parts = re.split(r"(\[.*?\]\(.*?\))", node.text)
        for i, part in enumerate(parts):
            if not part:
                continue

            if i % 2 == 0:
                new_nodes.append(TextNode(part, TextType.TEXT))
            else:
                alt, url = extract_markdown_links(part)[0]
                new_nodes.append(TextNode(alt, TextType.LINK, url))

    return new_nodes


def markdown_to_blocks(markdown: str) -> list[TextNode]:
    blocks = []
    for block in markdown.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        blocks.append(block)
    return blocks


def block_to_block_type(block: str) -> str:
    heading_match = re.match(r"^#+\s+", block)
    if heading_match:
        return "heading"

    if block.startswith("```") and block.endswith("```"):
        return "code"

    lines = block.split("\n")
    for line in lines:
        if not line.startswith(">"):
            break
    else:
        return "quote"

    for line in lines:
        if not line[:2] in ["* ", "- ", "+ "]:
            break
    else:
        return "unordered_list"

    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            break
    else:
        return "ordered_list"

    return "paragraph"


def extract_title(markdown: str) -> str:
    try:
        return re.match(r"^#\s+(.*)", markdown).group(1)
    except AttributeError:
        raise ValueError("No title found")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"Unknown text type: {text_node.text_type}")


def text_to_textnodes(text: str) -> list[TextNode]:
    delimiters = [
        (r"\*\*", TextType.BOLD),
        (r"\*", TextType.ITALIC),
        (r"`", TextType.CODE),
    ]
    nodes = [TextNode(text, TextType.TEXT)]
    for delimiter, text_type in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    children = text_to_children(text)
    code = ParentNode("code", children)
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

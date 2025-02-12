import re
from typing import Any

from src.textnode import TextNode, TextType


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
        if not line[0] in ["*", "-", "+"]:
            break
    else:
        return "unordered_list"

    for i, line in enumerate(lines, start=1):
        if not line.startswith(f"{i}. "):
            break
    else:
        return "ordered_list"

    return "paragraph"

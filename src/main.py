import glob
import os
import re
import shutil

from src import helpers
from src.htmlnode import ParentNode


def markdown_to_html_node(markdown: str) -> ParentNode:
    children = []
    blocks = helpers.markdown_to_blocks(markdown)
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)

    return ParentNode("div", children)


def block_to_html_node(block):
    block_type = helpers.block_to_block_type(block)
    if block_type == "paragraph":
        return helpers.paragraph_to_html_node(block)
    if block_type == "heading":
        return helpers.heading_to_html_node(block)
    if block_type == "code":
        return helpers.code_to_html_node(block)
    if block_type == "ordered_list":
        return helpers.olist_to_html_node(block)
    if block_type == "unordered_list":
        return helpers.ulist_to_html_node(block)
    if block_type == "quote":
        return helpers.quote_to_html_node(block)
    raise ValueError("invalid block type")


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        markdown = f.read()

    title = helpers.extract_title(markdown)
    html_node = markdown_to_html_node(markdown)

    with open(template_path, "r") as f:
        template = f.read()

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(template.replace("{{ Title }}", title).replace("{{ Content }}", html_node.to_html()))


def generate_pages_recursive(dir_path: str, template_path: str, dest_dir_path: str):
    files = glob.glob(os.path.join(dir_path, "**/*.md"), recursive=True)
    for file in files:
        dest_path = file.replace(dir_path, dest_dir_path).replace(".md", ".html")
        generate_page(file, template_path, dest_path)


def main():
    try:
        shutil.rmtree("public")
    except FileNotFoundError:
        pass
    shutil.copytree("static", "public")

    generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()

from enum import Enum


class TextType(Enum):
    TEXT = "TEXT"
    PARAGRAPH = "PARAGRAPH"
    HEADING = "HEADING"
    QUOTE = "QUOTE"
    CODE = "CODE"
    UNORDERED_LIST = "UNORDERED_LIST"
    ORDERED_LIST = "ORDERED_LIST"
    BOLD = "BOLD"
    ITALIC = "ITALIC"
    LINK = "LINK"
    IMAGE = "IMAGE"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

from enum import Enum
import re

from textnode import TextType, TextNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        extracted_images = extract_markdown_images(old_node.text)
        if old_node.text_type != TextType.TEXT or len(extracted_images) == 0:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = re.split(r"(\!\[.*?\]\(.*?\))",old_node.text)
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                image_extract = extract_markdown_images(sections[i])
                split_nodes.append(TextNode(image_extract[0][0], TextType.IMAGE, image_extract[0][1]))
        new_nodes.extend(split_nodes)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        extracted_links = extract_markdown_links(old_node.text)
        if old_node.text_type != TextType.TEXT or len(extracted_links) == 0:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = re.split(r"(\[.*?\]\(.*?\))",old_node.text)
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                image_extract = extract_markdown_links(sections[i])
                split_nodes.append(TextNode(image_extract[0][0], TextType.LINK, image_extract[0][1]))
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"\!\[(.*?)\]\((.*?)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[(.*?)\]\((.*?)\)",text)
    return matches

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    stripped_blocks = []
    for block in blocks:
        stripped_block = block.strip()
        if block != "":
            stripped_blocks.append(stripped_block)
    return stripped_blocks

def block_to_block_type(block):
    if len(re.findall(r"^#{1,6} .*",block)) > 0:
        return BlockType.HEADING
    elif len(re.findall(r"^`{3}.*`{3}$",block)) > 0:
        return BlockType.CODE
    elif len(re.findall(r"^>.*",block, flags = re.MULTILINE)) == len(block.splitlines()):
        return BlockType.QUOTE
    elif len(re.findall(r"^- .*",block, flags = re.MULTILINE)) == len(block.splitlines()):
        return BlockType.UNORDERED_LIST
    elif len(re.findall(r"^\d*\. .*",block, flags = re.MULTILINE)) == len(block.splitlines()):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

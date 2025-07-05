from re import findall
from textnode import TextType, TextNode


def split_nodes_delimiter(
    old_nodes: list[TextNode],
    delimiter: str,
    text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
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

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        full_node_text = old_node.text
        images = extract_markdown_images(full_node_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue

        for image in images:
            sections = full_node_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            full_node_text = sections[1]

        if full_node_text != "":
            new_nodes.append(TextNode(full_node_text, TextType.TEXT))

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            new_nodes.append(old_node)
            continue

        full_node_text = old_node.text
        links = extract_markdown_links(full_node_text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue

        for link in links:
            sections = full_node_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            full_node_text = sections[1]

        if full_node_text != "":
            new_nodes.append(TextNode(full_node_text, TextType.TEXT))

    return new_nodes

def extract_markdown_images(text: str) -> list[tuple[str, ...]]:
    image_pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = findall(image_pattern, text)
    return matches

def extract_markdown_links(text: str) -> list[tuple[str, ...]]:
    link_pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = findall(link_pattern, text)
    return matches

def text_to_textnodes(text: str) -> list[TextNode]:
    nodes = [ TextNode(text, TextType.TEXT)]
    text_type_delimiter = {"**": TextType.BOLD, "_": TextType.ITALIC, "`": TextType.CODE}
    for delimiter in text_type_delimiter:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type_delimiter[delimiter])
    return split_nodes_link(split_nodes_image(nodes))

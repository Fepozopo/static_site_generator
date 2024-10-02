from textnode import TextNode
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    '''
    This function takes a list of "old nodes", a delimiter, and a text type. It should return a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax.
    '''

    # Create a new list to store the new TextNodes
    new_nodes = []

    for node in old_nodes:
        # Only process nodes that are of the "text" type
        if node.text_type != "text":
            new_nodes.append(node)
            continue

        # Split the text by the delimiter
        parts = node.text.split(delimiter)

        # If there's an unmatched delimiter, we raise an error
        if len(parts) % 2 == 0:
            raise ValueError(f"Unmatched delimiter '{delimiter}' found in text: {node.text}")

        # Alternate between regular text and the delimited text
        for i, part in enumerate(parts):
            if i % 2 == 0:
                # Even indices are regular text (non-delimited)
                if part:
                    new_nodes.append(TextNode(part, "text", node.url))
            else:
                # Odd indices are delimited text (like code, bold, italic, etc.)
                new_nodes.append(TextNode(part, text_type, node.url))

    return new_nodes


def extract_markdown_images(text):
    '''
    This function takes raw markdown text and returns a list of tuples. Each tuple contains the alt text of the image and the image URL.
    '''

    # Create a list to store the image URLs
    image_urls = []

    # Find all image URLs in the text using regex
    image_url = re.findall(r"!\[(.*?)\]\((.*?)\)", text)
    if image_url:
        for alt_text, image_url in image_url:
            image_urls.append((alt_text, image_url))

    return image_urls


def extract_markdown_links(text):
    '''
    This function takes raw markdown text and returns a list of tuples. Each tuple contains the anchor text and the link URL.
    '''

    # Create a list to store the link URLs
    link_urls = []

    # Find all link URLs in the text using regex
    link_url = re.findall(r"\[(.*?)\]\((.*?)\)", text)
    if link_url:
        for anchor_text, link_url in link_url:
            link_urls.append((anchor_text, link_url))

    return link_urls


def split_nodes_image(old_nodes):
    '''
    This function takes a list of "old nodes" and returns a new list of nodes, where any "image" type nodes in the input list are (potentially) split into multiple nodes based on the syntax.
    '''

    # Create a new list to store the new TextNodes
    new_nodes = []
    
    # Regex pattern to find Markdown images
    image_pattern = r"!\[(.*?)\]\((.*?)\)"
    
    for node in old_nodes:
        # If it's not a "text" node, just append it to new_nodes
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        
        # Find all image matches in the node's text
        parts = re.split(image_pattern, node.text)
        
        # Iterate over the split parts using enumerate
        for i, part in enumerate(parts):
            if i % 3 == 0:  # Regular text before or between images
                if part:
                    new_nodes.append(TextNode(part, "text", node.url))
            elif i % 3 == 1:  # Alt text (captured by the first group)
                alt_text = part
                image_url = parts[i + 1] if i + 1 < len(parts) else None
                if image_url:
                    new_nodes.append(TextNode(alt_text, "image", image_url))
                    
    return new_nodes


def split_nodes_link(old_nodes):
    '''
    This function takes a list of "old nodes" and returns a new list of nodes, where any "link" type nodes in the input list are (potentially) split into multiple nodes based on the syntax.
    '''

    # Create a new list to store the new TextNodes
    new_nodes = []

    # Regex pattern to find Markdown links
    link_pattern = r"\[(.*?)\]\((.*?)\)"
    
    for node in old_nodes:
        # If it's not a "text" node, just append it to new_nodes
        if node.text_type != "text":
            new_nodes.append(node)
            continue
        
        # Find all link matches in the node's text
        parts = re.split(link_pattern, node.text)
        
        # Iterate over the split parts using enumerate
        for i, part in enumerate(parts):
            if i % 3 == 0:  # Regular text before or between links
                if part:
                    new_nodes.append(TextNode(part, "text", node.url))
            elif i % 3 == 1:  # Anchor text (captured by the first group)
                anchor_text = part
                link_url = parts[i + 1] if i + 1 < len(parts) else None
                if link_url:
                    new_nodes.append(TextNode(anchor_text, "link", link_url))
                    
    return new_nodes


def text_to_textnodes(text):
    '''
    This function converts a raw string of markdown text into a list of TextNodes using other functions.
    '''

    # Create an initial TextNode for the entire text
    nodes = [TextNode(text, "text")]

    # Process the Markdown syntax for each type: images, links, code blocks, bold, and finally italic text in that order
    nodes = split_nodes_image(nodes) # Process images
    nodes = split_nodes_link(nodes) # Process links
    nodes = split_nodes_delimiter(nodes, "`", "code") # Process code blocks
    nodes = split_nodes_delimiter(nodes, "**", "bold") # Process bold text
    nodes = split_nodes_delimiter(nodes, "*", "italic") # Process italic text

    return nodes

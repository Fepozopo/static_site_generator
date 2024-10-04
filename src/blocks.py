import re
from htmlnode import ParentNode, LeafNode, text_node_to_html_node
from inline import text_to_textnodes



def markdown_to_blocks(markdown):
    '''
    This function takes a raw markdown string (representing a full document) and returns a list of "block" strings.
    '''

    # Strip any leading or trailing whitespace from the entire document
    markdown = markdown.strip()

    # Normalize the markdown by removing leading spaces from each line
    markdown = '\n'.join(line.lstrip() for line in markdown.splitlines())

    # Remove any "empty" blocks due to excessive newlines
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    # Split the markdown into blocks based on double newlines
    blocks = re.split(r"\n{2,}", markdown)

    # Strip leading/trailing whitespace from each block individually
    blocks = [block.strip() for block in blocks]

    return blocks

def block_to_block_type(block):
    '''
    This function takes a single block of markdown text as input and returns a string representing the type of block it is.
    '''

    # Check for headings (1-6 # followed by a space)
    if re.match(r"^#{1,6} .+", block):
        return "heading"

    # Split the block into lines for further processing
    lines = block.splitlines()

    # Check if the block is an unordered list. Every line in an unordered list block must start with a * or - character, followed by a space.
    if all(re.match(r"^(\*|\-|\+)\s", line) for line in lines):
        return "unordered_list"

    # Check if the block is an ordered list. Every line in an ordered list block must start with a number followed by a . character and a space.
    # The numbers must start at 1 and increment by 1 for each line.
    ordered_list = True
    for i, line in enumerate(lines):
        match = re.match(r"^(\d+)\.\s", line)
        if not match or int(match.group(1)) != i + 1:
            ordered_list = False
            break
    if ordered_list:
        return "ordered_list"

    # Check if the block is a code block. Code blocks must start with 3 backticks and end with 3 backticks.
    if block.startswith("```") and block.endswith("```"):
        return "code_block"
    
    # Check if the block is a quote. Every line in a quote block must start with a > character.
    if all(line.startswith("> ") for line in lines):
        return "quote"
    
    # If none of the above, the block is a paragraph
    return "paragraph"


def text_to_children(text):
    '''
    This function takes a string of text and converts it into a list of HTMLNode objects 
    that represent the inline elements (bold, italic, links, etc.) using the text_to_textnodes and text_node_to_html_node functions.
    '''
    text_nodes = text_to_textnodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]
    return html_nodes


def block_to_html_node(block):
    '''
    This function takes a block of markdown and converts it into an appropriate HTMLNode.
    '''
    block_type = block_to_block_type(block)

    # If the block is a heading
    if block_type == "heading":
        level = len(re.match(r"^(#+)", block).group(1))  # Count the number of # symbols
        text_content = block[level + 1:].strip()  # Remove the heading symbols
        return ParentNode(f"h{level}", text_to_children(text_content))

    # If the block is an unordered list
    elif block_type == "unordered_list":
        items = [ParentNode("li", text_to_children(line[2:])) for line in block.splitlines()]
        return ParentNode("ul", items)

    # If the block is an ordered list
    elif block_type == "ordered_list":
        items = [ParentNode("li", text_to_children(line[3:])) for line in block.splitlines()]
        return ParentNode("ol", items)

    # If the block is a code block
    elif block_type == "code_block":
        code_content = block[3:-3].strip()  # Remove the backticks
        return ParentNode("pre", [LeafNode("code", code_content, None)])

    # If the block is a quote
    elif block_type == "quote":
        quote_content = "\n".join([line[2:] for line in block.splitlines()])
        return ParentNode("blockquote", text_to_children(quote_content))

    # Default: treat it as a paragraph
    else:
        return ParentNode("p", text_to_children(block))


def markdown_to_html_node(markdown):
    '''
    This function converts a full markdown document into a single HTMLNode. 
    The document will be represented as a parent div element containing child elements.
    '''
    # Split markdown into blocks
    blocks = markdown_to_blocks(markdown)
    
    # Create a parent div node
    parent_node = ParentNode("div", [])

    # Loop over each block
    for block in blocks:
        # Convert the block to an HTML node
        block_html_node = block_to_html_node(block)
        # Add the block node as a child of the parent div
        parent_node.children.append(block_html_node)

    return parent_node

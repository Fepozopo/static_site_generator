from textnode import TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    '''
    This function takes a list of "old nodes", a delimiter, and a text type. It should return a new list of nodes, where any "text" type nodes in the input list are (potentially) split into multiple nodes based on the syntax
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

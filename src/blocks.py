import re


def markdown_to_blocks(markdown):
    '''
    This function takes a raw markdown string (representing a full document) and returns a list of "block" strings.
    '''

    # Create a list to store the blocks
    blocks = []

    # Strip any leading or trailing whitespace from each block
    markdown = markdown.strip()

    # Remove any "empty" blocks due to excessive newlines
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)

    # Split the markdown into blocks
    blocks = re.split(r"\n{2,}", markdown)


    return blocks
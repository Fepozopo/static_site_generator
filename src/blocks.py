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


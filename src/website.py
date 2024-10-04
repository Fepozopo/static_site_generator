import os
from blocks import markdown_to_blocks, markdown_to_html_node



def copy_static_to_public():
    '''
    This function copies all the contents of the static directory to the public directory recursively.
    '''

    # Create variables for the paths to the static and public directories
    static_path = "static"
    public_path = "public"

    # First, delete all the contents of the public directory to ensure that the copy is clean
    if os.path.exists(public_path):
        os.system(f"rm -rf {public_path}/*")

    # Create the public directory if it doesn't exist
    if not os.path.exists(public_path):
        os.mkdir(public_path)

    # Then, copy the contents of the static directory to the public directory
    os.system(f"cp -r {static_path}/* {public_path}")


def extract_title(markdown):
    '''
    This function pulls the h1 header from the markdown and returns it as a string. If there is no h1 header, it raises an exception.
    '''

    # Split the markdown into blocks
    blocks = markdown_to_blocks(markdown)

    # Find the h1 header and strip the "# " prefix
    for block in blocks:
        if block.startswith("# "):
            return block[2:]

    # If no h1 header is found, raise an exception
    raise ValueError("No h1 header found")


def generate_page(from_path, template_path, dest_path):
    '''
    This function generates a new HTML page from a template file and saves it to a destination file.
    '''

    # Print a message to indicate that the page is being generated
    print(f"Generating page: {from_path} -> {dest_path} using template: {template_path}")

    # Read the markdown file at from_path and store the contents in a variable
    with open(from_path, "r", encoding="utf-8") as f:
        markdown = f.read()

    # Read the template file and store the contents in a variable
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Use the markdown_to_html_node function and .to_html() method to convert the markdown to an HTML string
    html = markdown_to_html_node(markdown).to_html()

    # Use the extract_title function to extract the title from the markdown
    title = extract_title(markdown)

    # Replace the placeholders in the template with the extracted title and HTML string
    result = template.replace("{{ Title }}", title).replace("{{ Content }}", html)

    # Write the result to the destination file, creating it if it doesn't exist
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(result)
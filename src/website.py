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


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    '''
    This function crawls every entry in the content directory and generates a new HTML page for each markdown file it finds using the same template.
    The generated pages are stored in the dest_dir_path directory.
    '''

    # Create the destination directory if it doesn't exist
    if not os.path.exists(dest_dir_path):
        os.makedirs(dest_dir_path)  # Use makedirs to ensure subdirectories are created

    # Loop over every entry in the content directory
    for entry in os.listdir(dir_path_content):
        full_entry_path = os.path.join(dir_path_content, entry)  # Get full path of the entry

        # If the entry is a directory, recursively call the function to generate pages in that directory
        if os.path.isdir(full_entry_path):
            # Create the corresponding subdirectory in the destination path
            new_dest_dir = os.path.join(dest_dir_path, entry)
            generate_pages_recursive(full_entry_path, template_path, new_dest_dir)

        # If the entry is a markdown file, generate a page for that file
        elif entry.endswith(".md"):
            # Generate the page and save it to the destination directory
            output_file = os.path.join(dest_dir_path, os.path.splitext(entry)[0] + ".html")
            generate_page(full_entry_path, template_path, output_file)

    # Print a message to indicate that all pages have been generated
    print(f"All pages have been generated in {dest_dir_path}")
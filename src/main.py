import os
from blocks import markdown_to_blocks


# Define the main function
def main():

    copy_static_to_public()


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
    h1_headers = []

    for block in blocks:
        if block.startswith("# "):
            h1_headers.append(block[2:])  # Strip the "# " from the header

    if not h1_headers:
        raise ValueError("No h1 header found")

    if len(h1_headers) > 1:
        raise ValueError("Multiple h1 headers found")

    # Return the single h1 header
    return h1_headers[0]




# Call the main function
if __name__ == "__main__":
    main()

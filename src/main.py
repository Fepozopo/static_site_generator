from textnode import TextNode
import os


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



# Call the main function
if __name__ == "__main__":
    main()

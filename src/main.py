from website import copy_static_to_public, generate_pages_recursive



# Define the main function
def main():

    copy_static_to_public()
    generate_pages_recursive("content", "template.html", "public")




# Call the main function
if __name__ == "__main__":
    main()

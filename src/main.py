from website import copy_static_to_public, generate_page



# Define the main function
def main():

    copy_static_to_public()
    generate_page("content/index.md", "template.html", "public/index.html")




# Call the main function
if __name__ == "__main__":
    main()

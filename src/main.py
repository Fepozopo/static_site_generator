from textnode import TextNode


# Create a new TextNode object
def main():
    text = "This is a text node"
    text_type = "bold"
    url = "https://www.boot.dev"
    text_node = TextNode(text, text_type, url)
    print(text_node)


# Call the main function
if __name__ == "__main__":
    main()

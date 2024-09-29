class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    # Returns True if all of the properties of the TextNode are equal
    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return False
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url
    
    # Returns a string representation of the TextNode
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children # A list of HTMLNode objects representing the children of this node
        self.props = props # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError
    
    # Return a string that represents the HTML attributes of the node
    def props_to_html(self):
        if self.props is None:
            return ""
        return " ".join([f"{key}=\"{value}\"" for key, value in self.props.items()])
    
    # Return an HTMLNode object that represents the children of the node
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("The value of a leaf node cannot be None")
        if self.tag is None:
            return self.value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        else: 
            return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"
import unittest
from main import extract_title



class TestExtractTitle(unittest.TestCase):
    def test_extract_title_with_h1_header(self):
        markdown = """
        # This is the title
        """

        result = extract_title(markdown)

        expected = "This is the title"

        self.assertEqual(result, expected)

    def test_extract_title_with_no_h1_header(self):
        markdown = """
        This is the title
        """

        try:
            result = extract_title(markdown)
        except ValueError as e:
            result = str(e) # Convert the exception to a string to compare with the expected value

        expected = "No h1 header found"

        self.assertEqual(result, expected)

    def test_extract_title_with_whitespace(self):
        markdown = """
            # This is a heading
         
            This is a paragraph of text. It has some **bold** and *italic* words inside of it.
            
            * This is the first list item in a list block
            * This is a list item
            * This is another list item
        """

        result = extract_title(markdown)

        expected = "This is a heading"

        self.assertEqual(result, expected)
        
import unittest

from markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self) -> None:
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("This is text with a ", TextType.TEXT), TextNode("bolded", TextType.BOLD), TextNode(" word", TextType.TEXT)]
        self.assertListEqual(actual, expected)

    def test_delim_bold_double(self) -> None:
        node = TextNode("This is text with a **bolded** word and **another**", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("This is text with a ", TextType.TEXT), TextNode("bolded", TextType.BOLD), TextNode(" word and ", TextType.TEXT), TextNode("another", TextType.BOLD)]
        self.assertListEqual(actual, expected)

    def test_delim_bold_multiword(self) -> None:
        node = TextNode("This is text with a **bolded word** and **another**", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("This is text with a ", TextType.TEXT), TextNode("bolded word", TextType.BOLD), TextNode(" and ", TextType.TEXT), TextNode("another", TextType.BOLD)]
        self.assertListEqual(actual, expected)

    def test_delim_italic(self) -> None:
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "_", TextType.ITALIC)
        expected = [TextNode("This is text with an ", TextType.TEXT), TextNode("italic", TextType.ITALIC), TextNode(" word", TextType.TEXT)]
        self.assertListEqual(actual, expected)

    def test_delim_bold_and_italic(self) -> None:
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        actual = split_nodes_delimiter([node], "**", TextType.BOLD)
        actual = split_nodes_delimiter(actual, "_", TextType.ITALIC)
        expected = [TextNode("bold", TextType.BOLD), TextNode(" and ", TextType.TEXT), TextNode("italic", TextType.ITALIC)]
        self.assertListEqual(actual, expected)

    def test_delim_code(self) -> None:
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        actual = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [TextNode("This is text with a ", TextType.TEXT), TextNode("code block", TextType.CODE), TextNode(" word", TextType.TEXT)]
        self.assertListEqual(actual, expected)

    def test_delim_error(self) -> None:
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_extract_markdown_images(self) -> None:
        actual, expected = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"), [("image", "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(actual, expected)

    def test_extract_markdown_links(self) -> None:
        actual = extract_markdown_links("This is text with a [link](https://boot.dev) and [another link](https://www.freecodecamp.org)")
        expected = [("link", "https://boot.dev"), ("another link", "https://www.freecodecamp.org")]
        self.assertListEqual(actual, expected)

    def test_split_image(self) -> None:
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        actual, expected = split_nodes_image([node]), [TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png")]
        self.assertListEqual(actual, expected)

    def test_split_image_single(self) -> None:
        node = TextNode("![image](https://www.example.COM/IMAGE.PNG)", TextType.TEXT)
        actual, expected = split_nodes_image([node]), [TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG")]
        self.assertListEqual(actual, expected)

    def test_split_images(self) -> None:
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT)
        actual = split_nodes_image([node])
        expected = [TextNode("This is text with an ", TextType.TEXT), TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"), TextNode(" and another ", TextType.TEXT), TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png")]
        self.assertListEqual(actual, expected)

    def test_split_links(self) -> None:
        node = TextNode("This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows", TextType.TEXT)
        actual = split_nodes_link([node])
        expected = [TextNode("This is text with a ", TextType.TEXT), TextNode("link", TextType.LINK, "https://boot.dev"), TextNode(" and ", TextType.TEXT), TextNode("another link", TextType.LINK, "https://blog.boot.dev"), TextNode(" with text that follows", TextType.TEXT)]
        self.assertListEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()

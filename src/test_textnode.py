import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_none_eq(self) -> None:
        node = TextNode("This is text", TextType.BOLD, None)
        node2 = TextNode("This is text", TextType.BOLD, None)
        self.assertEqual(node, node2)

    def test_url_none_not_eq(self) -> None:
        node = TextNode("This is text", TextType.BOLD, None)
        node2 = TextNode("This is text", TextType.BOLD, "https://boot.dev")
        self.assertNotEqual(node, node2)

    def test_text_not_eq(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_texttype_not_eq(self) -> None:
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_repr(self) -> None:
            node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
            self.assertEqual("TextNode(This is a text node, text, https://www.boot.dev)", repr(node))


class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self) -> None:
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self) -> None:
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_italic(self) -> None:
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_code(self) -> None:
        node = TextNode("This is a code block", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code block")

    def test_link(self) -> None:
        node = TextNode("This is a link", TextType.LINK, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href": "https://boot.dev"})

    def test_image(self) -> None:
        node = TextNode("This is an image", TextType.IMAGE, "https://boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://boot.dev", "alt": "This is an image"})

    def test_Error(self) -> None:
        node = TextNode("This is an invalid text node", "blockquote", "some_url") # type: ignore[reportArgumentType]
        node2 = TextNode("This is an invalid text node", None, None) # type: ignore[reportArgumentType]
        with self.assertRaises(ValueError):
            text_node_to_html_node(node)
            text_node_to_html_node(node2)


if __name__ == "__main__":
    unittest.main()

from htmlnode import HTMLNode


def main() -> None:
    dummy2 = HTMLNode("a", "this is a link.", None, {"href": "https://boot.dev", "target": "_blank"})
    dummy3 = HTMLNode("p", "this is a paragraph.", [dummy2], None)
    print(dummy3)


main()

def load_template_html(template_file):
    """
    Loads the HTML template from the specified file.

    Args:
        template_file (str): The path to the HTML template file.

    Returns:
        str: The content of the HTML template file.
    """
    with open(template_file, mode="r", encoding="utf-8") as file:
        return file.read()


def write_output_html(content, output_file):
    """
    Writes the generated HTML content to the output file and prints a success message.

    Args:
        content (str): The HTML content to write to the file.
        output_file (str): The path to the output HTML file.
    """
    with open(output_file, mode="w", encoding="utf-8") as file:
        file.write(content)

    print(f"Website was successfully generated to the file {output_file}.")


def merge_html_template(template, content, placeholder):
    """
    Merges the generated HTML content into the template, replacing the placeholder.

    Args:
        template (str): The HTML template string.
        content (str): The generated HTML content to insert.
        placeholder (str): The placeholder string to replace in the template.

    Returns:
        str: The merged HTML string.
    """
    return template.replace(placeholder, content)


def html_node(node, *, children=None, css_class=None, self_closing=False, **html_attrs):
    """
    Creates a new HTML node string.

    Args:
        node (str): The HTML tag name (e.g., "div", "p", "span").
        children (list[str] or str): A list of child HTML strings. Defaults to None.
        css_class (str): A CSS class to add to the opening tag. Defaults to None.
        self_closing (bool): Whether the tag is self-closing (e.g., <br />). Defaults to False.
        **html_attrs (dict): Additional HTML attributes as keyword arguments.

    Returns:
        str: The generated HTML node string.
    """
    opening_tag = f"<{node}>"
    closing_tag = [f"</{node}>"]

    if css_class:
        opening_tag = f"{opening_tag[:-1]} class='{css_class}'>"

    for attr, value in html_attrs.items():
        opening_tag = f"{opening_tag[:-1]} {attr}='{value}'>"

    if self_closing:
        opening_tag = f"{opening_tag[:-1]} />"
        closing_tag = []

    if not children or self_closing:
        return "".join([opening_tag, *closing_tag])

    return "".join([opening_tag, *children, *closing_tag])

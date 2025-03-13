from .html_generator import load_template_html, write_output_html, merge_html_template, html_node
from src.definitions import HTML_TEMPLATE_PATH, HTML_DESTINATION_PATH

PLACEHOLDER = "__TEMPLATE_MOVIE_GRID__"


def generate_html(movies):
    if not movies:
        return html_node("h2", children="No movies exist in database")

    list_items = []
    for title, movie in movies.items():
        img_node = html_node("img",
                             css_class="movie-poster",
                             src=movie.get("poster_url", "placeholder_poster.jpg"),
                             alt=f"{title}-Poster",
                             self_closing=True)
        imdb_link_node = html_node("a", href=f"https://www.imdb.com/title/{movie.get('imdb_id')}",
                                   target="_blank", children=img_node)
        title_node = html_node("div", css_class="movie-title", children=title)
        year_node = html_node("div", css_class="movie-year", children=str(movie.get("year")))
        containter = html_node("div", css_class="movie",
                               children=[imdb_link_node, title_node, year_node])
        list_item = html_node("li", children=containter)
        list_items.append(list_item)

    return "\n".join(list_items)


def generate_website(movies):
    html_content = generate_html(movies)
    template = load_template_html(HTML_TEMPLATE_PATH)
    merged_template = merge_html_template(template, html_content, PLACEHOLDER)
    write_output_html(merged_template, HTML_DESTINATION_PATH)

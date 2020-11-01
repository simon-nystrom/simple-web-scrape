# scrape.py

import requests
from bs4 import BeautifulSoup


def search(search_term):
    # Make the search request to IMDB
    response = requests.get(f"https://www.imdb.com/find?q={search_term}")
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    # Find the table with the class findList
    table = soup.find("table", {"class": "findList"})
    rows = table.select("tr td.result_text")
    # Construct a list with the search results, store the title and the href
    return [{"title": row.get_text().strip(), "href": row.a['href']} for row in rows]


def get_rating(href):
    response = requests.get(f"https://www.imdb.com{href}")
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    # Select by CSS selector for .ratingValue class and get the first result, we only expect there to be one
    rating = soup.select(".ratingValue")[0].span.get_text()
    return rating


def run():
    # Main interaction
    search_term = input("Search IMDB: ")
    results = search(search_term)
    num_results = len(results)

    print(f"Found {num_results} results:")
    for i, result in enumerate(results):
        print(f"({i+1}) {result['title']}")

    # Convert to int and subtract one to undo the addition to the index in the above loop
    selection = int(
        input(f"Select by entering a number (1-{num_results}): ")) - 1
    selected_result = results[selection]
    # Pass in the URL to the title we want to get the rating for
    rating = get_rating(selected_result["href"])

    print(f"{selected_result['title']} has a rating of {rating}!")


run()

import json
import requests
from bs4 import BeautifulSoup


def scrape_quotes():
    quotes_list = []
    page = 1
    while True:
        response = requests.get(f"http://quotes.toscrape.com/page/{page}/")
        if response.status_code != 200:
            break
        soup = BeautifulSoup(response.text, 'lxml')
        quotes = soup.find_all('div', class_='quote')
        for quote in quotes:
            text = quote.find('span', class_='text').text
            author = quote.find('small', class_='author').text
            tags = [tag.text for tag in quote.find_all('a', class_='tag')]
            quotes_list.append({'text': text, 'author': author, 'tags': tags})
        page += 1
    return quotes_list


def scrape_authors():
    authors_list = []
    response = requests.get("http://quotes.toscrape.com/")
    soup = BeautifulSoup(response.text, 'lxml')
    authors = soup.find_all('div', class_='author-details')
    for author in authors:
        name = author.find('h3', class_='author-title').text
        born_date = author.find('span', class_='author-born-date').text
        born_location = author.find('span', class_='author-born-location').text
        description = author.find('div', class_='author-description').text
        authors_list.append({'name': name, 'born_date': born_date, 'born_location': born_location, 'description': description})
    return authors_list


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


quotes_data = scrape_quotes()
authors_data = scrape_authors()
save_to_json(quotes_data, 'quotes.json')
save_to_json(authors_data, 'authors.json')

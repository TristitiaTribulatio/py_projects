import requests
import string
import os
from bs4 import BeautifulSoup


def main():
    # request_movie()
    # response_to_file()
    parsing_news()


def request_movie():
    try:
        url = input("Input the URL: ")
        request = requests.get(url).content
        page = BeautifulSoup(request, "html.parser")
        title = page.find("div", {"class": "originalTitle"}).find(text=True, recursive=False)
        description = page.find("div", {"class": "summary_text"}).find(text=True).strip()
        print({"title": title, "description": description})
    except AttributeError:
        print("Invalid movie page!")


def response_to_file():
    url = input("Input the URL: ")
    request = requests.get(url)
    if request.status_code == 200:
        file = open("source.html", "wb")
        file.write(request.content)
        file.close()
        print("Content saved.")
    else:
        print(f"The URL returned {request.status_code}!")


def parsing_news():
    articles, num_pages, type_articles = list(), int(input()), input()
    for i in range(1, num_pages+1):
        request = requests.get(f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={i}").content
        page = BeautifulSoup(request, "html.parser")
        articles.append(list(map(lambda x: x.get_text().strip("\n"), page.find_all("span", {"data-test": "article.type"}))))
        articles.append(list(map(lambda x: x.get("href"), page.find_all("a", {"data-track-action": "view article"}))))
        articles.append(list(map(lambda x: x.get_text(), page.find_all("a", {"data-track-action": "view article"}))))
        for x in range(len(articles[0])):
            if not os.access(f"Page_{i}", os.F_OK):
                os.mkdir(f"Page_{i}")
            if articles[0][x] == type_articles:
                title = articles[2][x].translate(articles[2][x].maketrans(' ', '_', string.punctuation))
                page_news = requests.get(f"https://www.nature.com{articles[1][x]}").content
                page_news_body = BeautifulSoup(page_news, "html.parser").find("div", {"class": "article__body"})
                if page_news_body is None:
                    page_news_body = BeautifulSoup(page_news, "html.parser").find("div", {"class": "article-item__body"})
                file = open(f"Page_{i}/{title}.txt", "wb")
                file.write(bytes(f"{page_news_body.get_text()}", "utf-8"))
                file.close()
        articles = list()
    print(f"Saved all articles")


if __name__ == "__main__":
    main()
from django.shortcuts import render, redirect
from django.conf import settings
from json import load, dumps
from datetime import datetime
from random import randint


def index(request):
    return redirect("/news/")


def news(request, num):
    with open(settings.NEWS_JSON_PATH) as file:
        for obj in load(file):
            if obj['link'] == num:
                title, created, text = obj['title'], obj['created'], obj['text']
                return render(request, 'news.html', {'title': title, 'created': created, 'text': text})


def main(request):
    with open(settings.NEWS_JSON_PATH) as file:
        sorted_news = sorted(load(file), key=lambda x: x["created"], reverse=True)
    data, q = dict(), request.GET.get("q")
    if q is None:
        q = ""
    for n in sorted_news:
        if q in n['title']:
            n['created'] = datetime.strptime(n['created'], "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d")
            if data.get(n['created']):
                data[n['created']].append([n['title'], n['link']])
            elif not data.get(n['created']):
                data[n['created']] = [[n['title'], n['link']]]
    return render(request, "main.html", {"data": data})


def create(request):
    title, text, time = request.POST.get("title"), request.POST.get("text"), datetime.now().replace(microsecond=0)
    links, link = list(), 1
    with open(settings.NEWS_JSON_PATH) as file:
        data = load(file)
        for obj in data:
            links.append(obj['link'])
            while link in links:
                link = randint(1, 100)
        news = {'created': str(time), 'text': text, 'title': title, 'link': link}
        if news['title'] is not None:
            data.append(news)
    with open(settings.NEWS_JSON_PATH, "w") as file:
        file.write(dumps(data))
    if title is None:
        return render(request, 'create.html')
    elif title is not None:
        return redirect("/news/")


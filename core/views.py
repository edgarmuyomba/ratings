from django.shortcuts import render
from dotenv import load_dotenv
import os
import requests
import time
import json
from bs4 import BeautifulSoup
from requests import Session
from django.http import JsonResponse

load_dotenv()
omdbKey = os.getenv('OMDB_APIKEY')


def search(request):
    title = request.GET.get('name')
    query = title.replace(' ', '%20')
    data = requests.get(
        f"https://www.omdbapi.com/?apiKey={omdbKey}&s={query}").json()
    results = data['Search']
    return render(request, "core/search.html", {"results": results, "title": title})


def details(request, imdbId, type):
    if type == "movie":
        # omdb request
        data = requests.get(
            f"https://www.omdbapi.com/?apiKey={omdbKey}&i={imdbId}")
        details = data.json()
        context = {
            "title": details['Title'],
            "rating": details['Ratings'][0]['Value'].split('/')[0],
            "plot": details['Plot'],
            "released": details['Released'],
            "poster": details['Poster'],
            "actors": details['Actors'],
            "year": details['Year']
        }
        return render(request, "core/movie_details.html", context)
    elif type == "series":
        # web scraping
        data = runScraper(imdbId)
        context = data
        data = requests.get(f"https://www.omdbapi.com/?apikey={omdbKey}&i={imdbId}").json()
        context['poster'] = data['Poster']
        context['year'] = data['Year']
        context['released'] = data['Released']
        context['actors'] = data['Actors']
        return render(request, "core/serie_details.html", context)


def runScraper(imdbID):
    session = Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
        'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
        'Accept': 'text/html,application/xhtml+xml,application/xml;'
        'q=0.9,image/webp,*/*;q=0.8'
    }
    res = session.get(f"https://www.imdb.com/title/{imdbID}/", headers=headers)
    bs = BeautifulSoup(res.text, "html.parser")
    title = bs.find("span", {"class": "sc-afe43def-1"}).text
    plot = bs.find("span", {"class": "sc-466bb6c-0 kJJttH"}).text
    rating = bs.find("span", {"class": "sc-bde20123-1 iZlgcd"}).text
    return {
        "title": title,
        "plot": plot,
        "rating": rating,
        "imdbId": imdbID
    }

def episode_ratings(request, imdbID):
    session = Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)'
        'AppleWebKit 537.36 (KHTML, like Gecko) Chrome',
        'Accept': 'text/html,application/xhtml+xml,application/xml;'
        'q=0.9,image/webp,*/*;q=0.8'
    }
    episode_ratings = {}
    res2 = session.get(f"https://www.imdb.com/title/{imdbID}/episodes/", headers=headers)
    bs2 = BeautifulSoup(res2.text, "html.parser")
    seasons = bs2.find_all("li", {"data-testid": "tab-season-entry"})
    for season in seasons:
        try:
            season = int(season.text)
        except ValueError:
            # value isnt an integer
            pass 
        else:
            episode_ratings[f'{season}'] = []
            time.sleep(1)
            episode_page = session.get(f"https://www.imdb.com/title/{imdbID}/episodes/?season={season}", headers=headers)
            bs3 = BeautifulSoup(episode_page.text, "html.parser")
            episodes = bs3.find_all("article", {"class": "sc-f1a948e3-1 bGxjcH episode-item-wrapper"})
            for episode in episodes:
                rate = episode.find("span", {"class": "ipc-rating-star ipc-rating-star--base ipc-rating-star--imdb ratingGroup--imdb-rating"})
                episode_ratings[f'{season}'].append(float(rate.text.split('/')[0]))
    return JsonResponse(episode_ratings)
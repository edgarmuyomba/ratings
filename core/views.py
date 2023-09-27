from django.shortcuts import render
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
from requests import Session

load_dotenv()
omdbKey = os.getenv('OMDB_APIKEY')


def search(request):
    title = request.GET.get('name')
    query = title.replace(' ', '%20')
    data = requests.get(
        f"https://www.omdbapi.com/?apiKey={omdbKey}&s={query}").json()
    results = data['Search']
    '''
        format is title, year, imdbid, type, poster
    '''
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
            "languages": details['Language'],
            "poster": details['Poster']
        }
        return render(request, "core/movie_details.html", context)
    elif type == "series":
        # web scraping
        data = runScraper(imdbId)
        context = data
        poster = requests.get(f"https://img.omdbapi.com/?apikey={omdbKey}&i={imdbId}")
        context['poster'] = poster
        return render(request, "core/serie_details.html", context)


'''
    for a movie, display all ratings from omdb, poster, box office
    for a serie, scrape imdb and display well formatted ratings per episode on top of above results
    https://www.imdb.com/title/{{ imdbId }}/episodes/ ,,, https://www.imdb.com/title/{{ imdbId }}/episodes/?season=2
'''


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
        "rating": rating
    }

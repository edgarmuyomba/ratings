from django.shortcuts import render
from dotenv import load_dotenv
import os, requests 

load_dotenv()
omdbKey = os.getenv('OMDB_APIKEY')

def search(request):
    title = request.GET.get('name')
    query = title.replace(' ', '%20')
    data = requests.get(f"https://www.omdbapi.com/?apiKey={omdbKey}&s={query}").json()
    results = data['Search']
    '''
        format is title, year, imdbid, type, poster
    '''
    return render(request, "core/search.html", { "results": results, "title": title })

def details(request, imdbId, type):
    if type == "movie":
        # omdb request
        data = requests.get(f"https://www.omdbapi.com/?apiKey={omdbKey}&i={imdbId}").json()
    elif type == "series":
        # web scraping
        data = runScraper(imdbId)
    # i think this is where we do the web scraping
    # url -> https://www.imdb.com/title/{imdbId}/
    return render(request, "core/details.html", {})


'''
    for a movie, display all ratings from omdb, poster, box office
    for a serie, scrape imdb and display well formatted ratings per episode on top of above results
    https://www.imdb.com/title/{{ imdbId }}/episodes/ ,,, https://www.imdb.com/title/{{ imdbId }}/episodes/?season=2
'''

def runScraper(imdbID):
    return {}
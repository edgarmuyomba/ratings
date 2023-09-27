from django.shortcuts import render
from dotenv import load_dotenv
import os, requests 

load_dotenv()
omdbKey = os.getenv('OMDB_APIKEY')

def search(request):
    query = request.GET.get('name')
    data = requests.get(f"https://www.omdbapi.com/?apiKey={omdbKey}&s={query}").json()
    results = data['Search']
    '''
        format is title, year, imdbid, type, poster
    '''
    return render(request, "core/search.html", { "results": results, "query": query })

def details(request, imdbId):
    movie_details = requests.get(f"https://www.omdbapi.com/?apiKey={omdbKey}&i={imdbId}").json()
    return render(request, "core/details.html", {})
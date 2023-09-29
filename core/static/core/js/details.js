const episodes = document.querySelector("div.episodes");

const id = document.querySelector("p.imdbId").textContent;

const endPoint = "http://localhost:8000"

async function get_ratings(imdbId) {
    const data = await fetch(`${endPoint}/details/episode_ratings/${imdbId}`);
    const results = await data.json();
    return results;
}

(async () => {
    const ratings = await get_ratings(id);
    console.log(ratings);
})();


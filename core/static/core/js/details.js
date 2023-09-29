const episodes = document.querySelector("div.episodes > table");

const id = document.querySelector("p.imdbId").textContent;

const endPoint = "http://localhost:8000"

async function get_ratings(imdbId) {
    const data = await fetch(`${endPoint}/details/episode_ratings/${imdbId}`);
    const results = await data.json();
    return results;
}

function displayRatings(ratings) {
    let last_ep = 1;
    let header = document.createElement('tr');
    let _ = document.createElement('td');
    header.appendChild(_);
    for (let season in ratings) {
        last_ep = Math.max(last_ep, ratings[season].length);
        let head = document.createElement('td');
        head.textContent = season;
        header.appendChild(head);
    }
    episodes.appendChild(header);
    
    for (let i = 1; i <= last_ep; i++) {
        let row = document.createElement('tr');
        let season = document.createElement('td');
        season.textContent = i;
        row.appendChild(season);

        for (let season in ratings) {
            let rate = document.createElement('td');
            rate.textContent = ratings[season][i-1] ? ratings[season][i-1] : '';
            row.appendChild(rate);
        }
        episodes.appendChild(row);
    }
}

(async () => {
    const ratings = await get_ratings(id);
    const rates = {
        1: [1, 2, 3, 4, 5],
        2: [1, 2, 3, 4, 5, 6],
        3: [1, 2, 3, 4],
        4: [1, 2, 3, 4, 5, 6, 7],
    }
    displayRatings(ratings);
})();


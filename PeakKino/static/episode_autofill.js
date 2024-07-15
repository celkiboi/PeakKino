document.addEventListener("DOMContentLoaded", () => {
    document.addEventListener("click", async (event) => {
        if (event.target.id === "autohelp-button") {
            const showName = document.getElementById("show-name").innerText;
            const results = await searchTVMaze(showName);
            showSearchResults(results);
        }
    });
});

async function searchTVMaze(query) {
    const response = await fetch(`https://api.tvmaze.com/search/shows?q=${query}`);
    if (!response.ok) {
        throw new Error('Network response was not ok.');
    }
    return await response.json();
}

function showSearchResults(results) {
    const resultsContainer = document.querySelector('.results');
    resultsContainer.innerHTML = results.map((result, index) => {
        const imageUrl = result.show.image ? result.show.image.medium : '';
        return `
            <div class="result-entry">
                <h2>${result.show.name}</h2>
                <img alt="${result.show.name}" src="${imageUrl}">
                <button class="select-button" data-id="${index}">Select</button>
            </div>
        `;
    }).join('');

    function handleResultClick(event) {
        if (event.target.classList.contains("select-button")) {
            const id = event.target.getAttribute("data-id");
            selectShow(results[id].show);
            
            resultsContainer.removeEventListener("click", handleResultClick);
        }
    }

    resultsContainer.addEventListener("click", handleResultClick);
}

async function selectShow(selectedShow) {
    const resultsContainer = document.querySelector('.results');
    resultsContainer.innerHTML = '';

    let seasonNumber = document.getElementById('season-name').innerText.split('. ')[0];

    const seasons = await getSeasons(selectedShow);
    const episodes = await getEpisodes(seasons, seasonNumber);
    fillEpisode(episodes);
}

async function getSeasons(selectedShow) {
    try {
        let response = await fetch(`https://api.tvmaze.com/shows/${selectedShow.id}/seasons`);
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        let data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching data:', error);
    }
}

async function getEpisodes(seasons, seasonNumber) {
    let target_season;
    for (let i = 0; i < seasons.length; i++) {
        if (seasons[i].number == seasonNumber) {
            target_season = seasons[i];
            break;
        }
    }

    const response = await fetch(`https://api.tvmaze.com/seasons/${target_season.id}/episodes`);
    if (!response.ok) {
        throw new Error('Network response was not ok.');
    }
    return await response.json();
}

function fillEpisode(episodes) {
    var episodeNumber = document.getElementById('id_number').value;

    if (episodeNumber=='') {
        displayEpisodeOptions(episodes);
    }
    else {
        selectEpisode(episodes[episodeNumber - 1]); // id of episode 1 is 0
    }
}

function displayEpisodeOptions(episodes) {
    const resultsContainer = document.querySelector('.results');
    resultsContainer.innerHTML = episodes.map((episode, index) => {
        return `
            <div class="episode-option">
                <h2>Episode ${episode.number}</h2>
                <h3>${episode.name}</h3>
                ${episode.summary}
                <button class="select-button-episode" data-id="${index}">Select</button>
            </div>
        `;
    }).join('');

    function handleEpisodeSelect(event) {
        if (event.target.classList.contains("select-button-episode")) {
            const id = event.target.getAttribute("data-id");
            selectEpisode(episodes[id]);
            
            resultsContainer.removeEventListener("click", handleEpisodeSelect);
        }
    }

    resultsContainer.addEventListener("click", handleEpisodeSelect);
}

function selectEpisode(episode) {
    const nameInput = document.getElementById('id_title');
    nameInput.value = episode.name;

    const numberInput = document.getElementById('id_number');
    numberInput.value = episode.number;

    const descirptionInput = document.getElementById('id_description');
    descirptionInput.value = episode.summary.replace(/<[^>]*>/g, '');

    const resultsContainer = document.querySelector('.results');
    resultsContainer.innerHTML = '';
}
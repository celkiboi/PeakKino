var isDisplayed = 0;

    document.getElementById("upload_shows").addEventListener("click", function() {
        if (isDisplayed == 0) {
            var showMenu = document.createElement("ul");
            showMenu.id = "upload_shows_submenu"

            var createShow = document.createElement("li");
            var createShowLink = document.createElement("a");
            createShowLink.textContent = "Create a Show";
            createShow.appendChild(createShowLink);

            var createSeason = document.createElement("li");
            var createSeasonLink = document.createElement("a");
            createSeasonLink.textContent = "Create a Season";
            createSeason.appendChild(createSeasonLink);

            var uploadEpisode = document.createElement("li");
            var uploadEpisodeLink = document.createElement("a");
            uploadEpisodeLink.textContent = "Upload an Episode";
            uploadEpisode.appendChild(uploadEpisodeLink);

            showMenu.appendChild(createShow);
            showMenu.appendChild(createSeason);
            showMenu.appendChild(uploadEpisode);

            var insertionPoint = document.getElementById("upload_shows_container");
            insertionPoint.appendChild(showMenu);
            isDisplayed = 1;
        }
        else {
            var showMenu = document.getElementById("upload_shows_submenu");
            showMenu.remove();
            isDisplayed = 0;
        }
    });
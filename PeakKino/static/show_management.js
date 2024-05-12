var isCreateMenuDisplayed = 0;
var isDeleteMenuDisplayed = 0;

function displayCreateShowMenu() {
    var showCreateMenu = document.createElement("ul");
    showCreateMenu.id = "upload_shows_submenu"

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

    showCreateMenu.appendChild(createShow);
    showCreateMenu.appendChild(createSeason);
    showCreateMenu.appendChild(uploadEpisode);

    var insertionPoint = document.getElementById("upload_shows_container");
    insertionPoint.appendChild(showCreateMenu);
    isCreateMenuDisplayed = 1;
}

function hideCreateShowMenu(){
    var showCreateMenu = document.getElementById("upload_shows_submenu");
    showCreateMenu.remove();
    isCreateMenuDisplayed = 0;
}

function displayDeleteShowMenu() {
    var showDeleteMenu = document.createElement("ul");
    showDeleteMenu.id = "delete_shows_submenu"

    var deleteShow = document.createElement("li");
    var deleteShowLink = document.createElement("a");
    deleteShowLink.textContent = "Delete a Show";
    deleteShow.appendChild(deleteShowLink);

    var deleteSeason = document.createElement("li");
    var deleteSeasonLink = document.createElement("a");
    deleteSeasonLink.textContent = "Delete a Season";
    deleteSeason.appendChild(deleteSeasonLink);

    var deleteEpisode = document.createElement("li");
    var deleteEpisodeLink = document.createElement("a");
    deleteEpisodeLink.textContent = "Delete an Episode";
    deleteEpisode.appendChild(deleteEpisodeLink);

    showDeleteMenu.appendChild(deleteShow);
    showDeleteMenu.appendChild(deleteSeason);
    showDeleteMenu.appendChild(deleteEpisode);

    var insertionPoint = document.getElementById("delete_shows_container");
    insertionPoint.appendChild(showDeleteMenu);
    isDeleteMenuDisplayed = 1;
}

function hideDeleteShowMenu() {
    var showDeleteMenu = document.getElementById("delete_shows_submenu");
    showDeleteMenu.remove();
    isDeleteMenuDisplayed = 0;
}

document.getElementById("upload_shows").addEventListener("click", function() {
    if (isCreateMenuDisplayed == 0) {
        displayCreateShowMenu();
        if (isDeleteMenuDisplayed == 1) {
            hideDeleteShowMenu();
        }
    }
    else {
        hideCreateShowMenu();
    }
});

document.getElementById("delete_shows").addEventListener("click", function() {
    if (isDeleteMenuDisplayed == 0) {
        displayDeleteShowMenu();
        if (isCreateMenuDisplayed == 1) {
            hideCreateShowMenu();
        }
    }
    else {
        hideDeleteShowMenu();
    }
});
var isCreateMenuDisplayed = 0;
var isDeleteMenuDisplayed = 0;

function displayCreateShowMenu() {
    var showCreateMenu = document.getElementById("upload_shows_submenu");
    showCreateMenu.classList.remove("hidden");
    isCreateMenuDisplayed = 1;
}

function hideCreateShowMenu(){
    var showCreateMenu = document.getElementById("upload_shows_submenu");
    showCreateMenu.classList.add("hidden");
    isCreateMenuDisplayed = 0;
}

function displayDeleteShowMenu() {
    var showDeleteMenu = document.getElementById("delete_shows_submenu");
    showDeleteMenu.classList.remove("hidden");
    isDeleteMenuDisplayed = 1;
}

function hideDeleteShowMenu() {
    var showDeleteMenu = document.getElementById("delete_shows_submenu");
    showDeleteMenu.classList.add("hidden");
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

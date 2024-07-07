document.addEventListener("DOMContentLoaded", function () {
    document.addEventListener("click", function(event) {
        if (event.target.id == "autohelp-button") {
            var query = document.getElementById('id_name').value;
            searchTVMaze(query)
            .then(results => {
                results = results;
                showSearchResults(results);
            })
            .catch(error => {
                console.error('Error;', error);
            })
        }
    })
})

function searchTVMaze(query) {
    return fetch(`https://api.tvmaze.com/search/shows?q=${query}`)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.json();
    })
    .then(data => {
        return data;
    })
    .catch(error => {
        console.error('Error fetching data:', error);
    });
}

function showSearchResults(results) {
    var resultsMenuHTML = ''

    for (i = 0; i < results.length; i++) {
        if (results[i].show.image === null) {
            results[i].show.image = {medium: ''};
        }
        resultsMenuHTML += `
            <div class="result-entry">
                <h2>${results[i].show.name}</h2>
                <img alt="${results[i].show.name}" src="${results[i].show.image.medium}">
                <button class="select-button" id="${i}">Select</button>
            </div>
        `;
    }

    var resultsContainer = document.querySelector('.results');
    resultsContainer.innerHTML = resultsMenuHTML;

    resultsContainer.addEventListener("click", function(event) {
        if (event.target.classList.contains("select-button")) {
            const id = event.target.id;
            selectAutofill(results[id].show);
        }
    });
}

function selectAutofill(selectedShow) {
    document.getElementById('id_name').value = selectedShow.name;
    downloadImageFromURI(selectedShow.image.original)
    .then(file => {
        var imageInput = document.getElementById('id_image_upload');
        var fileList = new DataTransfer();
        fileList.items.add(file);
        imageInput.files = fileList.files;
        Object.defineProperty(imageInput, 'files', {
            value: fileList,
            writable: true
        });
        imageInput.dispatchEvent(new Event('change'));

        alert("WARNING: Age rating is not autofilled");

        var resultsContainer = document.querySelector('.results');
        resultsContainer.innerHTML = '';
    })
    .catch(error => {
        console.error('Error in downloadImageFromURI:', error);
    });
}

function downloadImageFromURI(uri) {
    return fetch(uri)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.blob();
    })
    .then(blob => {
        return new File([blob], 'autofilled_image.jpg', { type: 'image/jpeg' });
    })
    .catch(error => {
        console.error('Error downloading image:', error);
        throw error;
    });
}

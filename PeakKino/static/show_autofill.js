document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("autohelp-button").addEventListener("click", async function(event) {
        const query = document.getElementById('id_name').value;
        const results = await searchTVMaze(query);
        showSearchResults(results);
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

    const resultsMenuHTML = results.map((result, index) => {
        const imageUrl = result.show.image ? result.show.image.medium : '';
        return `
            <div class="result-entry">
                <h2>${result.show.name}</h2>
                <img alt="${result.show.name}" src="${imageUrl}">
                <button class="select-button" id="${index}">Select</button>
            </div>
        `;
    }).join('');

    resultsContainer.innerHTML = resultsMenuHTML;

    function handleShowSelect(event) {
        if (event.target.classList.contains("select-button")) {
            const id = event.target.id;
            selectAutofill(results[id].show);
        }

        resultsContainer.removeEventListener("click", handleShowSelect);
    }

    resultsContainer.addEventListener("click", handleShowSelect);
}

function selectAutofill(selectedShow) {
    document.getElementById('id_name').value = selectedShow.name;
    clearImageInput();
    downloadImageFromURI(selectedShow.image.original)
    .then(file => {
        var imageInput = document.getElementById('id_image_upload');
        var fileList = new DataTransfer();
        fileList.items.add(new File([file], 'autofilled_image.jpg', { type: 'image/jpeg' }));
        imageInput.files = fileList.files;

        imageInput.dispatchEvent(new Event('change'));

        alert("WARNING: Age rating is not autofilled");

        var resultsContainer = document.querySelector('.results');
        resultsContainer.innerHTML = '';
    })
    .catch(error => {
        console.error('Error in downloadImageFromURI:', error);
    });
}

function clearImageInput() {
    const imageInput = document.getElementById('id_image_upload');
    imageInput.value = '';
    imageInput.files = null;
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
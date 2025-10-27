/*global Image */
function loadImage(url) {
    return new Promise(function (resolve, reject) {
        const img = new Image();
        img.src = url;
        img.onload = function () {
            resolve(img);
        };
        img.onerror = function () {
            reject(new Error("Nie można załadować " + url));
        };
    });
}

function loadGallery() {
    const imagePaths = [
        "images/IMG_9921.jpg",
        "images/IMG_civ.jpg"
    ];

    const galleryContainer = document.getElementById("gallery-container");
    galleryContainer.innerHTML = "<p>Ładowanie zdjęć...</p>";

    Promise.all(imagePaths.map(loadImage))
        .then(function (images) {
            galleryContainer.innerHTML = "";
            images.forEach(function (img) {
                galleryContainer.appendChild(img);
            });
        })
        .catch(function (error) {
            galleryContainer.innerHTML =
                "<p>Błąd ładowania zdjęć: " + error.message + "</p>";
        });
}

window.addEventListener("DOMContentLoaded", loadGallery);

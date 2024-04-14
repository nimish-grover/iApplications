

function displayTextAfterDelay(textId, delay, removeOtherTextId) {
    setTimeout(function () {
        document.getElementById(textId).style.display = 'block';
        if (removeOtherTextId) {
            document.getElementById(removeOtherTextId).style.display = 'none';
        }
    }, delay);
}

// Display text after 30 seconds
displayTextAfterDelay('textAfter30Secs', 15000); // 30 seconds in milliseconds

// Display text after 1 minute and remove 30-second text
displayTextAfterDelay('textAfter1Minute', 40000, 'textAfter30Secs'); // 1 minute in milliseconds

window.addEventListener('load', function () {
    var loader = document.querySelector('.loader');
    setTimeout(function () {
        loader.classList.add('loader-hidden');
    }, 500); // 1000 milliseconds = 1 second
});

function showLoader() {
    var loader = document.querySelector('.loader');
    loader.classList.remove('loader-hidden');
}

// Add .init-loader class to clickable elements (buttons and anchor tags) if they themselves do not have .no-loader class
var clickableElements = document.querySelectorAll('button, a');
clickableElements.forEach(function (element) {
    if (!element.classList.contains('no-loader')) {
        element.classList.add('init-loader');
    }
});

// Add event listener to elements with class "init-loader"
var initLoaderElements = document.querySelectorAll('.init-loader');
initLoaderElements.forEach(function (element) {
    element.addEventListener('click', function () {
        showLoader();
    });
});

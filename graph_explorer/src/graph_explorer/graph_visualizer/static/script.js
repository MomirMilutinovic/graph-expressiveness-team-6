function changeVisualizer() {
    changeView("main")
    changeView("bird")
}

function changeView(type) {
    let selectedVisualizerId = document.getElementById("visualizer-select").value;
    for (let mainView of document.getElementsByClassName(type + "-view")) {
        mainView.classList.add("is-hidden");
    }
    document.getElementById(type + "-view-" + selectedVisualizerId).classList.remove("is-hidden");
}

function selectVisualizer(name) {
    const request = new XMLHttpRequest();
    request.onreadystatechange = function () {
      if (request.readyState === 4 && request.status === 200) {
        location.reload();
      }
    };
    request.open("GET", "/select-visualizer/" + encodeURIComponent(name), true);
    request.send();
    changeView("main");
}

function deleteFilter(filter) {
    const request = new XMLHttpRequest();
    request.open("DELETE", "/delete-filter", true);
    request.send(JSON.stringify(filter));
    request.onload = function () {
        if (request.status === 200) {
            location.reload();
        }
    };
}

document.addEventListener("DOMContentLoaded", function() {
    if (!document.getElementById("filter-form")) {
        return;
    }
    document.getElementById("filter-form").addEventListener("submit", function(e) {
        e.preventDefault();
        request = new XMLHttpRequest();
        request.open("POST", "/add-filter", true);
        request.send(new FormData(this));
        request.onload = function () {
            if (request.status === 200) {
                location.reload();
            }
            else {
                showErrorMessage("Invalid filter", "Error while adding filter (most likely due to type mismatch). <br/> Message: " + request.responseText);
            }
        };
    }, true);
}, true);

function showErrorMessage(title, message) {
    let errorToast = document.getElementById("error");
    let errorMessage = document.getElementById("error-message");
    let errorTitle = document.getElementById("error-title");
    errorTitle.innerHTML = title;
    errorMessage.innerHTML = message;
    errorToast.classList.remove("is-hidden");
    setTimeout(function() {
        errorToast.classList.add("is-hidden");
    }, 5000);
}

function dispatchNodeFocusEvent(nodeId) {
    let event = new CustomEvent("node-focus", {detail: nodeId});
    document.dispatchEvent(event);
}
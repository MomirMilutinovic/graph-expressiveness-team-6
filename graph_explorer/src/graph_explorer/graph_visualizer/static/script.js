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
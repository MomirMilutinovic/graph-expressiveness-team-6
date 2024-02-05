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
    alert("Selected: " + name);
    const request = new XMLHttpRequest();
    request.open("GET", "/select-visualizer/" + encodeURIComponent(name), true);
    request.send();
}

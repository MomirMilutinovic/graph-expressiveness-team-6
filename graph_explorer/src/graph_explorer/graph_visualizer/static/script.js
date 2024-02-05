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
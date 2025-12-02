let allGames = [];
let selected = [];


// Load game list
fetch("/games")
    .then(r => r.json())
    .then(list => allGames = list);


// Autocomplete
document.getElementById("game-search").addEventListener("input", function () {
    let q = this.value.toLowerCase();
    let out = document.getElementById("autocomplete");

    out.innerHTML = "";

    if (!q) return;

    let matches = allGames.filter(g => g.toLowerCase().includes(q)).slice(0, 10);

    matches.forEach(game => {
        let div = document.createElement("div");
        div.className = "option";
        div.textContent = game;
        div.onclick = () => addGame(game);
        out.appendChild(div);
    });
});

function addGame(game) {
    if (!selected.includes(game)) {
        selected.push(game);
        renderSelected();
    }
}

function renderSelected() {
    let container = document.getElementById("selected-games");
    container.innerHTML = "";
    selected.forEach(g => {
        let tag = document.createElement("div");
        tag.className = "tag";
        tag.textContent = g;
        container.appendChild(tag);
    });
}


// Submit
document.getElementById("submit-btn").onclick = () => {
    fetch("/recommend", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({owned_games: selected})
    })
    .then(r => r.json())
    .then(showResults);
};


function showResults(data) {
    renderGrid("combined-results", data.combined);
    renderGrid("bundle-results", data.bundle);
    renderGrid("copurchase-results", data.copurchase);
}

function renderGrid(id, list) {
    let grid = document.getElementById(id);
    grid.innerHTML = "";

    list.forEach(item => {
        let card = document.createElement("div");
        card.className = "game-card";

        card.innerHTML = `
            <img src="${item.image}">
            <div>${item.game_id}</div>
        `;
        grid.appendChild(card);
    });
}

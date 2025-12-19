

function showCelebration() {
    const celebrationText = document.createElement("div");
    celebrationText.className = "celebration-text";
    celebrationText.textContent = "LET'S GO! 5 IN FOLGE!";
    document.body.appendChild(celebrationText);
    setTimeout(() => celebrationText.remove(), 3000);
}

function showCelebration10() {
    const celebrationText = document.createElement("div");
    celebrationText.className = "celebration-text10";
    celebrationText.textContent = "WEITER SO! DAMN!";
    document.body.appendChild(celebrationText);

    const flashDiv = document.createElement("div");
    flashDiv.className = "rainbow-background";
    document.body.appendChild(flashDiv);

    setTimeout(() => { celebrationText.remove(); flashDiv.remove(); }, 3000);
}

function showCelebration20() {
    const celebrationText = document.createElement("div");
    celebrationText.className = "celebration-text";
    celebrationText.textContent = "20 AM STÜCK! DU BIST ES!";
    document.body.appendChild(celebrationText);

    const flameDiv = document.createElement("div");
    flameDiv.className = "flame-border";
    document.body.appendChild(flameDiv);

    setTimeout(() => { celebrationText.remove(); flameDiv.remove(); }, 3000);
}

export { showCelebration, showCelebration10, showCelebration20 };
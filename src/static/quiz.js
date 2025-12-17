
let currentModule = null;
let moduleButtons = document.querySelectorAll('.modulePickerBtn');


moduleButtons.forEach(moduleButton => {
moduleButton.addEventListener("click", async function() {
    await fetch("/reset_questions", {method: "POST"});
    let modul = moduleButton.dataset.modul;
    currentModule = modul;
    document.querySelector('.module-container').style.display = 'none';
    document.querySelector('.score-box').style.display = "";
    buttons.forEach(btn => btn.style.display = "");

    fetch(`/get_question/${modul}`)
        .then(response => response.json())
        .then(data => {
            document.querySelector('.question-container').style.display = 'block';
            document.getElementById("question-text").textContent = data.text;
            let answerButtons = document.querySelectorAll(".answer-btn");
            answerButtons[0].textContent = data.answer_a;
            answerButtons[1].textContent = data.answer_b;
            answerButtons[2].textContent = data.answer_c;
            
            answerButtons.forEach(btn => {
                btn.dataset.questionId = data.id;
            })
        });
    });
});  

let buttons = document.querySelectorAll(".answer-btn");

buttons.forEach(button => {
    button.addEventListener("click", async () => {
        buttons.forEach(b => b.disabled = true);
        const selectedAnswer = button.dataset.answer;

        const response = await fetch("/check_answer", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                question_id: button.dataset.questionId,
                selected_answer: selectedAnswer
            })
        });

        const result = await response.json();
        buttons.forEach(b => {
        if (b.dataset.answer === result.correct_answer) {
            b.classList.add("correct");
    }
        });
        document.getElementById("score").textContent = result.score;
        console.log("Streak:", result.streak, "Celebrate:", result.celebrate);
        if (result.celebrate) {
            if (result.streak === 5) {
                showCelebration();
            } else if (result.streak === 10) {
                showCelebration10();
            } else if (result.streak === 20) {
                showCelebration20();
            }
        }

        if (!result.correct) {
            button.textContent = "FALSCH";
        } 
        showNextButton();
    });
});

function showNextButton() {
    if (document.querySelector(".next-btn")) return;
    
    const nextBtn = document.createElement("button");
    nextBtn.textContent = "Nächste Frage";
    nextBtn.className = "next-btn";
    nextBtn.onclick = loadNewQuestion;
    document.querySelector('.answers-container').appendChild(nextBtn);
}

async function loadNewQuestion() {
    buttons.forEach(b => {
    b.disabled = false;  
    b.classList.remove("correct"); 
});
    const nextBtn = document.querySelector(".next-btn");
    if (nextBtn) nextBtn.remove();
    
    buttons.forEach(btn => btn.style.backgroundColor = "");
    
    const response = await fetch(`/get_question/${currentModule}`);
    const question = await response.json();

    if (question.error) {
        document.querySelector("h1").textContent = "Modul abgeschlossen! Wähle ein neues oder mach 'ne Pause.";
        buttons.forEach(btn => btn.style.display = "none");
        moduleButtons.forEach(btn => btn.style.display = "inline-block");
        document.querySelector('.module-container').style.display = '';
        return;
    }

    document.querySelector("h1").textContent = question.text;

    buttons[0].textContent = question.answer_a;
    buttons[0].dataset.questionId = question.id;

    buttons[1].textContent = question.answer_b;
    buttons[1].dataset.questionId = question.id;

    buttons[2].textContent = question.answer_c;
    buttons[2].dataset.questionId = question.id;
}

function chooseModule() {
    modulePicker = document.querySelectorAll("modulePickerBtn");
}

function showCelebration() {
    const celebrationText = document.createElement("div");
    celebrationText.className = "celebration-text";
    celebrationText.textContent = "LET'S GO! 5 IN FOLGE!";
    document.body.appendChild(celebrationText);

    setTimeout(() => {
        celebrationText.remove();
    }, 3000);
} 

function showCelebration10() {
    const celebrationText = document.createElement("div");
    celebrationText.className = "celebration-text10";
    celebrationText.textContent = "WEITER SO! DAMN!";
    document.body.appendChild(celebrationText);

    const flashDiv = document.createElement("div");
    flashDiv.className = "rainbow-background";
    document.body.appendChild(flashDiv);

    setTimeout(() => {
        celebrationText.remove();
        flashDiv.remove();
    }, 3000);
}

function showCelebration20() {
    const celebrationText = document.createElement("div");
    celebrationText.className = "celebration-text";
    celebrationText.textContent = "20 AM STÜCK! DU BIST ES!";
    document.body.appendChild(celebrationText);

    const flameDiv = document.createElement("div");
    flameDiv.className = "flame-border";
    document.body.appendChild(flameDiv);

    setTimeout(() => {
        celebrationText.remove();
        flameDiv.remove();
    }, 3000);
}
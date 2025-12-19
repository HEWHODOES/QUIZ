

let currentModule = null;
let asked_questions = [];

async function loadNewQuestion(buttons, currentModule) {
    buttons.forEach(b => { b.disabled = false; b.classList.remove("correct"); });
    const nextBtn = document.querySelector(".next-btn");
    if (nextBtn) nextBtn.remove();
    
    buttons.forEach(btn => btn.style.backgroundColor = "");

    const response = await fetch(`/get_question/${currentModule}`);
    const question = await response.json();

    if (question.error) {
        document.querySelector("h1").textContent = "Modul abgeschlossen! Wähle ein neues oder mach 'ne Pause.";
        buttons.forEach(btn => btn.style.display = "none");
        document.querySelectorAll('.modulePickerBtn').forEach(btn => btn.style.display = "inline-block");
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

export { currentModule, loadNewQuestion, asked_questions };


let currentModule = null;
let asked_questions = [];

async function loadNewQuestion(buttons, currentModule) {
    buttons.forEach(b => { b.disabled = false; b.classList.remove("correct"); });
    const nextBtn = document.querySelector(".next-btn");
    if (nextBtn) nextBtn.remove();
    
    buttons.forEach(btn => btn.style.backgroundColor = "");

    const response = await fetch(`/get_question/${currentModule}`);
    const question = await response.json();

    console.log('Received question:', question);

    if (!question.id) {

            const moduleContainer = document.querySelector('.module-container');
            const categoryName = moduleContainer.dataset.categoryName;

            document.getElementById('module-name').textContent = categoryName;

            document.querySelector('.question-container').style.display = 'none';
            document.querySelector('.score-box').style.display = 'none';
            buttons.forEach(btn => btn.style.display = "none");
            document.querySelectorAll('.modulePickerBtn').forEach(btn => btn.style.display = ""); 
            document.querySelector('.module-container').style.display = "grid"; 
            return;
}

    document.getElementById("question-text").textContent = question.text;
    buttons[0].textContent = question.answer_a;
    buttons[0].dataset.questionId = question.id;
    buttons[1].textContent = question.answer_b;
    buttons[1].dataset.questionId = question.id;
    buttons[2].textContent = question.answer_c;
    buttons[2].dataset.questionId = question.id;
}

export { currentModule, loadNewQuestion, asked_questions };
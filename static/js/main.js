
import { currentModule, loadNewQuestion, asked_questions } from "./quiz.js";
import { showCelebration, showCelebration10, showCelebration20 } from "./celebration.js";

document.addEventListener("DOMContentLoaded", () => {
    const moduleButtons = document.querySelectorAll('.modulePickerBtn');
    const buttons = document.querySelectorAll(".answer-btn");

    let currentModuleLocal = null; // lokale Referenz

    moduleButtons.forEach(moduleButton => {
        moduleButton.addEventListener("click", async function() {
            await fetch("/reset_questions", { method: "POST" });
            currentModuleLocal = moduleButton.dataset.modul;
            document.querySelector('.module-container').style.display = 'none';
            document.querySelector('.score-box').style.display = "";
            buttons.forEach(btn => btn.style.display = "");

            const response = await fetch(`/get_question/${currentModuleLocal}`);
            const data = await response.json();

            document.querySelector('.question-container').style.display = 'block';
            document.getElementById("question-text").textContent = data.text;

            buttons[0].textContent = data.answer_a;
            buttons[1].textContent = data.answer_b;
            buttons[2].textContent = data.answer_c;

            buttons.forEach(btn => { btn.dataset.questionId = data.id; });
        });
    });

    buttons.forEach(button => {
        button.addEventListener("click", async () => {
            buttons.forEach(b => b.disabled = true);
            const selectedAnswer = button.dataset.answer;

            const response = await fetch("/check_answer", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    question_id: button.dataset.questionId,
                    selected_answer: selectedAnswer
                })
            });

            const result = await response.json();
            buttons.forEach(b => { if (b.dataset.answer === result.correct_answer) b.classList.add("correct"); });

            document.getElementById("score").textContent = result.score;

            if (result.celebrate) {
                if (result.streak === 5) showCelebration();
                if (result.streak === 10) showCelebration10();
                if (result.streak === 20) showCelebration20();
            }

            if (!result.correct) button.textContent = "FALSCH"; 
            showNextButton();
        });
    });

    function showNextButton() {
        if (document.querySelector(".next-btn")) return;
        const nextBtn = document.createElement("button");
        nextBtn.textContent = "Nächste Frage";
        nextBtn.className = "next-btn";
        nextBtn.onclick = () => loadNewQuestion(buttons, currentModuleLocal);
        document.querySelector('.answers-container').appendChild(nextBtn);
    }
});
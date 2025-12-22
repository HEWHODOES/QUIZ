import { loadNewQuestion } from "./quiz.js";
import { showCelebration, showCelebration10, showCelebration20 } from "./celebration.js";

document.addEventListener("DOMContentLoaded", async () => {

    const sessionResponse = await fetch('/check_session');
    const sessionData = await sessionResponse.json();

    if (sessionData.logged_in) {
        document.getElementById('username-display').textContent = sessionData.username;
        document.getElementById('username-display').style.display = 'inline';
        document.getElementById('login-btn').style.display = 'none';
        document.getElementById('logout-btn').style.display = 'inline';
    }

    const categoryContainer = document.querySelector('.category-container');
    const moduleContainer = document.querySelector('.module-container');
    const buttons = document.querySelectorAll(".answer-btn");
    
    let currentModuleId = null;

    // === STEP 1: Categories laden ===
    const categoriesResponse = await fetch('/get_categories');
    const categories = await categoriesResponse.json();
    
    categories.forEach(category => {
        const btn = document.createElement('button');
        btn.textContent = category.name;
        btn.className = 'categoryPickerBtn';
        btn.dataset.categoryId = category.id;
        categoryContainer.appendChild(btn);
        
        // === STEP 2: Category Click → Module laden ===
        btn.addEventListener('click', async () => {
            categoryContainer.style.display = 'none';
            moduleContainer.style.display = 'block';
            moduleContainer.innerHTML = '';  // Leeren
            
            const modulesResponse = await fetch(`/get_modules/${category.id}`);
            const modules = await modulesResponse.json();
            
            modules.forEach(module => {
                const moduleBtn = document.createElement('button');
                moduleBtn.textContent = module.name;
                moduleBtn.className = 'modulePickerBtn';
                moduleBtn.dataset.moduleId = module.id;
                moduleContainer.appendChild(moduleBtn);
                
                // === STEP 3: Modul Click → Quiz starten ===
                moduleBtn.addEventListener('click', async () => {
                    await fetch("/reset_questions", { method: "POST" });
                    currentModuleId = module.id;
                    
                    moduleContainer.style.display = 'none';
                    document.querySelector('.score-box').style.display = "";
                    buttons.forEach(btn => btn.style.display = "");

                    const response = await fetch(`/get_question/${currentModuleId}`);
                    const data = await response.json();

                    console.log("Daten:", data); 

                    document.querySelector('.question-container').style.display = 'block';
                    document.getElementById("question-text").textContent = data.text;

                    buttons[0].textContent = data.answer_a;
                    buttons[1].textContent = data.answer_b;
                    buttons[2].textContent = data.answer_c;

                    buttons.forEach(btn => { btn.dataset.questionId = data.id; });
                });
            });
        });
    });

    // === Antwort-Buttons ===
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
            buttons.forEach(b => { 
                if (b.dataset.answer === result.correct_answer) 
                    b.classList.add("correct"); 
            });

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
        nextBtn.onclick = () => loadNewQuestion(buttons, currentModuleId);
        document.querySelector('.answers-container').appendChild(nextBtn);
    }
});
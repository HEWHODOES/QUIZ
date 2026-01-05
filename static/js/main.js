import { loadNewQuestion } from "./quiz.js";
import { showCelebration, showCelebration10, showCelebration20 } from "./celebration.js";

document.addEventListener("DOMContentLoaded", async () => {

    document.getElementById('back_to_gategories').addEventListener('click', () => {
        currentModuleId = null;
        const nextBtn = document.querySelector(".next-btn");
        if (nextBtn) nextBtn.remove();

        document.querySelectorAll('.answer-btn').forEach(btn => {
            btn.style.display = "none";
            btn.classList.remove("correct");
            btn.disabled = false;
            btn.style.backgroundColor = "";
        })
        
        document.getElementById('module-banner').style.display = 'none';
        document.querySelector('.section-title').style.display = 'block';
        document.querySelector('.module-container').style.display = 'none';
        document.querySelector('.category-container').style.display = 'grid';
        document.querySelector('.question-container').style.display = 'none';
        document.querySelector('.score-box').style.display = 'none';
        document.querySelectorAll('.answer-btn').forEach(btn => btn.style.display = 'none');
    });

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

    // === STEP 1: Load categories ===
    const categoriesResponse = await fetch('/get_categories');
    const categories = await categoriesResponse.json();
    
    categories.forEach(category => {
        
        const btn = document.createElement('button');
        btn.textContent = category.name;
        btn.className = 'categoryPickerBtn';
        btn.dataset.categoryId = category.id;
        categoryContainer.appendChild(btn);
        
        // === STEP 2: Category Click → Load modules ===
        btn.addEventListener('click', async () => {
            document.getElementById('module-banner').style.display = 'block';
            document.getElementById('module-name').textContent = category.name;

            // IMPORTANT: store both name and id so we can refresh later
            moduleContainer.dataset.categoryName = category.name;
            moduleContainer.dataset.categoryId = category.id;  // <-- store id

            document.querySelector('.section-title').style.display = 'none';
            categoryContainer.style.display = 'none';
            moduleContainer.style.display = 'grid';
            moduleContainer.innerHTML = '';  // clear
            
            // fetch modules and populate (same as refreshModulesUI logic)
            const modulesResponse = await fetch(`/get_modules/${category.id}`);
            const modules = await modulesResponse.json();
            
            modules.forEach(module => {
                const moduleBtn = document.createElement('button');
                moduleBtn.className = 'modulePickerBtn';

                if (module.perfect) {
                    moduleBtn.classList.add("moduleBtnPerfect");
                }

                if (module.completed) {
                    moduleBtn.textContent = module.name + ' ✓';
                } else {
                    moduleBtn.textContent = module.name;
                }
                
                moduleBtn.dataset.moduleId = module.id;
                moduleContainer.appendChild(moduleBtn);
                
                // === STEP 3: Module Click → Start quiz ===
                moduleBtn.addEventListener('click', async () => {
                    document.getElementById('module-banner').style.display = 'block';
                    document.getElementById('module-name').textContent = module.name;
                    document.querySelector('.section-title').style.display = 'none';
                    await fetch("/reset_questions", { method: "POST" });
                    currentModuleId = module.id;
                            
                    moduleContainer.style.display = 'none';
                    document.querySelector('.score-box').style.display = "";
                    buttons.forEach(btn => btn.style.display = "");

                    const response = await fetch(`/get_question/${currentModuleId}`);
                    const data = await response.json();

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

    // === Answer buttons behaviour ===
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

            // Choose label only after server confirmed whether this was the last question
            const lastLabel = "Zurück zu Modulen"; // final button text
            const nextLabel = result.module_finished ? lastLabel : "Nächste Frage";

            // Pass module_finished so showNextButton can change behavior on the final question
            showNextButton(nextLabel, !!result.module_finished);
        });
    });

    function showNextButton(label = "Nächste Frage", moduleFinished = false) {
        if (document.querySelector(".next-btn")) return;
        const nextBtn = document.createElement("button");
        nextBtn.textContent = label;
        nextBtn.className = "next-btn";

        if (moduleFinished) {
            // Final question: reload the page so the module list is refreshed from the server
            nextBtn.onclick = () => window.location.reload();
        } else {
            // Normal behaviour: load the next question
            nextBtn.onclick = () => loadNewQuestion(buttons, currentModuleId);
        }

        document.querySelector('.answers-container').appendChild(nextBtn);
    }

    // end of DOMContentLoaded
});
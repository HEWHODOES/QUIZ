

function showCelebration() {
    const gifBox = document.querySelector('.gif-box');
    gifBox.style.backgroundImage = "url('/static/gifs/streak5.gif')";

    setTimeout(() => {
        gifBox.style.backgroundImage = "url('/static/gifs/neutral.gif')";
    }, 6500); 
}

function showCelebration10() {
    const gifBox = document.querySelector('.gif-box');
    gifBox.style.backgroundImage = "url('/static/gifs/streak10.gif')"; 
    
    setTimeout(() => {
        gifBox.style.backgroundImage = "url('/static/gifs/neutral.gif')";
    }, 7600); 
}

function showCelebration20() {
    const gifBox = document.querySelector('.gif-box');
    gifBox.style.backgroundImage = "url('/static/gifs/streak20.gif')"; 

    setTimeout(() => {
        gifBox.style.backgroundImage = "url('/static/gifs/neutral.gif')";
    }, 9000); 
}

export { showCelebration, showCelebration10, showCelebration20 };
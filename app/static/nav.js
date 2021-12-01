// nav.js handles responsive menu
var burger = document.querySelector('.burger');
var nav = document.querySelector('.nav-mobile');
var main = document.getElementById('main');
var footer = document.getElementById('footer');
var screenWidth = window.innerWidth;

var toggleNav = () => {
    burger.addEventListener('click', () => {
        nav.classList.toggle('nav-active');
        burger.classList.toggle('toggle');
        
        if (main.style.display === "none") {
            main.style.display = "";
        } else {
            main.style.display = "none";
        }

        if (footer.style.display === "none") {
            footer.style.display = "";
        } else {
            footer.style.display = "none";
        }
    });
}

toggleNav();

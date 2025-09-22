import htmx from 'htmx.org'
import Mustache from 'mustache'
import { swapTheme } from "./utils/swapTheme";
import { checkAllTable } from "./utils/checkboxAllTable";

// Config HTMX
htmx.config.selfRequestsOnly = false;

const elements = {
    themeSwap: document.querySelector('#themeSwap input[type="checkbox"]'),
    // calledFunctions: {
    //     checkAllTable: checkAllTable(document.querySelector('.table')),
    // }
};

// Aplica el tema guardado al cargar la página
document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        if (elements.themeSwap) {
            elements.themeSwap.checked = savedTheme === 'dark';
        }
    }
});

// Cambia el tema y lo guarda en localStorage
if (elements.themeSwap) {
    elements.themeSwap.addEventListener('change', () => {
        swapTheme();
        const newTheme = document.documentElement.getAttribute('data-theme');
        localStorage.setItem('theme', newTheme);
    });
}



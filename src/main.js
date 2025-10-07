import htmx from 'htmx.org'
import 'htmx-ext-response-targets'
import { swapTheme } from "./utils/swapTheme";
import { checkAllTable } from "./utils/checkboxAllTable";
import { config } from './config';

window.htmx = htmx;

htmx.config.selfRequestsOnly = false;
htmx.config.withCredentials = true;
document.body.addEventListener('htmx:configRequest', (e) => {
    const path = e.detail.path;
        if(path.startsWith('/api/')) {
        const API_BASE_URL = config().url.api;
        e.detail.path = API_BASE_URL + e.detail.path;
    }
});

document.body.addEventListener('htmx:afterRequest', (evt) => {
    const redirectUrl = evt.detail.xhr.getResponseHeader('HX-Redirect');

    if (redirectUrl) {
        window.location.href = redirectUrl;
        return;
    }

    if(evt.detail.failed && evt.detail.xhr.status === 401) {
        showToast('Sesión expirada. Por favor ingresa nuevamente.', 'error');

        // Redirigir si es una petición importante
        setTimeout(() => {
            window.location.href = '/login.html'
        }, 1500)
    }
});



const elements = {
    themeSwap: document.querySelector('#themeSwap input[type="checkbox"]'),
    table: document.querySelector('.table'),
};



/* if(elements.table) {
    checkAllTable(elements.table);
} */

// Aplica el tema guardado al cargar la página
document.addEventListener('DOMContentLoaded', async () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
        document.documentElement.setAttribute('data-theme', savedTheme);
        if (elements.themeSwap) {
            elements.themeSwap.checked = savedTheme === 'dark';
        }
    }


        try {
        const API_BASE_URL = config().url.api;
        const res = await fetch(`${API_BASE_URL}/api/me`, { credentials: 'include' });
        if (res.ok) {
            const data = await res.json();
            console.log(data);
            if (data.rol !== 1) {
                // Oculta el link de usuarios si no es admin
                const adminLink = document.getElementById('admin-link');
                if (adminLink) adminLink.style.display = 'none';
            }
        }
    } catch (e) {
        // Si hay error, mejor ocultar el link por seguridad
        const adminLink = document.getElementById('admin-link');
        if (adminLink) adminLink.style.display = 'none';
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

function showToast(message, type = 'success') {
    const toast = document.getElementById('toast-notification');
    toast.innerHTML = `
        <div class="alert alert-${type}">
            ${message}
        </div>
    `;
    setTimeout(() => toast.innerHTML = '', 3000);
}

import { closeAllModals } from "../utils/closeAllModals";

const elements = {
    modals: document.querySelectorAll('dialog'),
    forms: {
        crear: document.querySelector('#crearSoporteForm')
    },
    errorContainer: document.querySelector('#response'),
    table: document.querySelector('#soportes-table')
}

elements.forms.crear.addEventListener('htmx:afterRequest', (e) => {
    const modal = document.querySelector('dialog#crearSoporte');
    const errorContainer = modal.querySelector('#response');
    const toastContainer = modal.querySelector('[data-soporte-toast]');
    const request = e.detail.xhr;

    if (request.status === 201) {
        errorContainer.innerHTML = '';

        htmx.trigger(modal, 'soporteCreated');

        setTimeout(() => {
            toastContainer.innerHTML = '';
            modal.close();
        }, 1000);

        e.target.reset();
    } else if (request.status === 422) {
        toastContainer.innerHTML = '';
    }
});

closeAllModals(elements.modals);

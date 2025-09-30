import { closeAllModals } from "../utils/closeAllModals";

const elements = {
    modals: document.querySelectorAll('dialog'),
    forms: {
        crear: document.querySelector('#crearAlertaForm')
    },
    errorContainer: document.querySelector('#response'),
    table: document.querySelector('#alertas-table')
}

elements.forms.crear.addEventListener('htmx:afterRequest', (e) => {
    const modal = document.querySelector('dialog#crearAlerta');
    const errorContainer = modal.querySelector('#response');
    const toastContainer = modal.querySelector('[data-alerta-toast]');
    const request = e.detail.xhr;

    if (request.status === 201) {
        errorContainer.innerHTML = '';

        htmx.trigger(modal, 'alertaCreated');

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

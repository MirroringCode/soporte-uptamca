import { closeAllModals } from "../utils/closeAllModals";

const elements = {
    modals: document.querySelectorAll('dialog'),
    forms: {
        crear: document.getElementById('crearEmpleadoForm')
    },
    table: document.querySelector('#table-personal')
}


elements.forms.crear.addEventListener('htmx:afterRequest', (e) => {
    const modal = document.querySelector('dialog#crearEmpleado');
    const errorContainer = modal.querySelector('[data-response]');
    const toastContainer = modal.querySelector('[data-empleado-toast]');
    const request = e.detail.xhr;

    if (request.status === 201) {
        errorContainer.innerHTML = '';

        htmx.trigger(modal, 'empleadoCreated');

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
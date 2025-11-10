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
        if (errorContainer) {
            errorContainer.innerHTML = '';
        }

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

// Disparar evento después de crear/actualizar/eliminar
document.addEventListener('htmx:afterRequest', (e) => {
    if (['POST', 'PUT', 'DELETE']
        .includes(e.detail.requestConfig.verb.toUpperCase()) && 
        e.detail.requestConfig.path.includes('/api/soportes')) {
        
        // Disparar actualización de filtros
        htmx.trigger('body', 'filterChanged');
    }
});


document.addEventListener('htmx:afterRequest', (evt) => {
    if (evt.detail.requestConfig.path.includes('/api/soportes/report')) {
        const btn = document.getElementById('downloadSoportesPdf');

        if (!evt.detail.successful) {
            // Mostrar mensaje de error si la generación falla
            const error = JSON.parse(evt.detail.xhr.response).message;
            const toast = document.querySelector('[data-toast]');
            toast.innerHTML = `
                <div class="alert alert-error">
                    ${error}
                </div>
            `;
            setTimeout(() => toast.innerHTML = '', 5000);
        }
    }
});



closeAllModals(elements.modals);

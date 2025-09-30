import { closeAllModals } from "../utils/closeAllModals";

const elements = {
    modals: document.querySelectorAll('dialog'),
    forms: {
        crear: document.getElementById('crearUsuarioForm'),
        editar: document.getElementById('editarUsuarioForm')
    },
    table: document.querySelector('#users-table')
}



elements.forms.crear.addEventListener('htmx:afterRequest', (e) => {
    const modal = document.querySelector('dialog#crearUsuario');
    const errorContainer = modal.querySelector('[data-response]');
    const toastContainer = modal.querySelector('[data-user-toast]');
    const request = e.detail.xhr;

    if (request.status === 201) {
        errorContainer.innerHTML = '';
        
        htmx.trigger(modal, 'userCreated');

        setTimeout(() => {
            toastContainer.innerHTML = ''; // Limpiar el toast
            modal.close();
        }, 1000);

        e.target.reset();
    } else if(request.status === 422) {
        toastContainer.innerHTML = '';
    }
})

// elements.forms.editar.addEventListener('htmx:afterRequest', (e) => {
//     const modal = document.querySelector('dialog#editarUsuario');
//     const errorContainer = modal.querySelector('[data-response]');
//     const toastContainer = modal.querySelector('[data-user-toast]');
//     const request = e.detail.xhr;

//     if (request.status === 201) {
//         errorContainer.innerHTML = '';
        
//         htmx.trigger(modal, 'userUpdated');

//         setTimeout(() => {
//             toastContainer.innerHTML = ''; // Limpiar el toast
//             modal.close();
//         }, 1000);

//         e.target.reset();
//     } else if(request.status === 422) {
//         toastContainer.innerHTML = '';
//     }
// })

closeAllModals(elements.modals)

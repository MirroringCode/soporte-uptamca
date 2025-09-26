const elements = {
    modals: document.querySelectorAll('dialog'),
    forms: {
        crear: document.getElementById('crearUsuarioForm')
    },
    errorContainer: document.getElementById('response'),
    table: document.querySelector('#users-table')
}



elements.forms.crear.addEventListener('htmx:afterRequest', (e) => {
    const modal = document.querySelector('dialog#crearUsuario');
    const errorContainer = modal.querySelector('#response');
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


elements.modals.forEach((modal) => {
    modal.addEventListener('close', (e) => {
        const form = modal.querySelector('form');
        modal.querySelector('#response').innerHTML = '';
        modal.querySelector('[data-user-toast').innerHTML = '';
        if (form) form.reset();
    });
});
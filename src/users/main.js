import htmx from 'htmx.org'

document.addEventListener('htmx:afterRequest', (e) => {
    const createModal = document.querySelector('dialog#crearUsuario');
    const usersTable = document.querySelector('#users-table')
    if(e.detail.requestConfig.path === '/api/users') {

        if(e.detail.xhr.status === 201) {
            createModalmodal.close();
            htmx.trigger('#users-table', 'refresh');
            const form = createModal.querySelector('form');
            form.reset();
        }

        
        
    }
});
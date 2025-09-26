import htmx from 'htmx.org'

const elements = {
    modals: document.querySelectorAll('dialog'),
    forms: {
        crear: document.getElementById('crearUsuarioForm')
    }
}

elements.forms.crear.addEventListener('htmx:afterRequest', (e) => {
    const form = e.target;
    const toast = document.querySelector('[data-message]');
    const request = {
        verb: e.detail.requestConfig.verb,
        path: e.detail.requestConfig.path
    }
    if(request.verb === 'post' && request.path.endsWith('/users')) {  
        if(e.detail.successful) {
            form.reset();
            if(toast.classList.contains('hidden')) {
                toast.classList.remove('hidden');
            }
            if(!toast.classList.contains('hidden')) {
                setTimeout(() => {
                    toast.classList.add('hidden')
                }, 1800);
            }
        }

    }
});

elements.modals.forEach((modal) => {
    modal.addEventListener('close', (e) => {
        const form = modal.querySelector('form');
        modal.querySelector('#response').innerHTML = '';
        if (form) form.reset();

    });
});
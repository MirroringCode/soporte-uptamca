export function closeAllModals(modals) {
modals.forEach((modal) => {
    modal.addEventListener('close', (e) => {
        const form = modal.querySelector('form');
        const responseDiv = modal.querySelector('[data-response]');
        const toast = modal.querySelector('[data-toast]');
        if (form) form.reset();
        if(responseDiv) {
            responseDiv.innerHTML = '';
        }
        if(toast) {
            toast.innerHTML = '';
        }
    });
});
} 
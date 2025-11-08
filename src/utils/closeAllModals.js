export function closeAllModals(modals) {
modals.forEach((modal) => {
    modal.addEventListener('close', (e) => {
        const form = modal.querySelector('form');
        modal.querySelector('[data-response]').innerHTML = '';
        if (form) form.reset();
        modal.querySelector(['data-toast']).innerHTML = '';
    });
});
} 
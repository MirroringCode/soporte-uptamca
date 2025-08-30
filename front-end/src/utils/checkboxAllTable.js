export const checkAllTable = (table) => {
    const firstCheckbox = table.querySelector('thead input[type="checkbox"]');
    const checkboxes = table.querySelectorAll('tbody input[type="checkbox"]');

    firstCheckbox.addEventListener('change', (e) => {
        const isChecked = e.target.checked;
        
        checkboxes.forEach(checkbox => {
            checkbox.checked = isChecked;
        });

    });

    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', (e) => {
            firstCheckbox.checked = false;
        });
    })

}

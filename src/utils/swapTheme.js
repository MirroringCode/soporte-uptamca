export const swapTheme = () => {
    const currentTheme = document.documentElement.getAttribute('data-theme');
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    document.documentElement.setAttribute('data-theme', newTheme);
    


    localStorage.setItem('theme', newTheme);

    // Optionally, you can save the theme preference in localStorage
    
    // Dispatch a custom event to notify other parts of the application
    // document.dispatchEvent(new CustomEvent('themeChanged', { detail: { theme: newTheme } }));
}
export function config() {
    const url = {
        api: import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:5000/',
        base: import.meta.env.BASE_URL
    } 
    
    return {
        url: url
    }
}



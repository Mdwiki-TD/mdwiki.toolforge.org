
class RealMwApi {
    async get(params) {
        // const end_point = 'https://commons.wikimedia.org/w/api.php';
        const end_point = 'https://ar.wikipedia.org/w/api.php';
        const url = new URL(end_point);
        for (const [key, value] of Object.entries(params)) {
            url.searchParams.append(key, value);
        }
        url.searchParams.append('origin', '*'); // required for CORS in browser

        const res = await fetch(url);
        if (!res.ok) {
            throw new Error(`HTTP error ${res.status}`);
        }
        return res.json();
    }
}

// Replace mw.Api with the real fetch-based implementation
const mw = {
    Api: RealMwApi,
    loader: {
        using(modules) {
            console.log('Loaded modules:', modules);
            return Promise.resolve();
        }
    }
};

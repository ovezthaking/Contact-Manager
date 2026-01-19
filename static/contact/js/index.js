function changeSorting() {
    const sortBy = document.getElementById('sort-select').value;
    const currentOrder = new URLSearchParams(window.location.search).get('order') || 'asc';
    const query = new URLSearchParams(window.location.search).get('q') || '';
    let url = `?sort_by=${sortBy}&order=${currentOrder}`;
    if (query) {
        url += `&q=${encodeURIComponent(query)}`;
    }
    window.location.href = url;
}

const getCityCoords = async (city) => {
    try {
        const res = await fetch(`https://nominatim.openstreetmap.org/search?q=${city}&format=json&limit=1`)
        const data = await res.json()

        if (data && data.length > 0){
            const coords = {
                lat: data[0].lat,
                lon: data[0].lon
            }
        }

        return coords
    } catch (e) {
        console.error('Error getting lattitude and longitude: ', e)
    }
    return null
}

const getWeatherData = async (lat, lon) => {

    try {
        const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,is_day,weather_code,wind_speed_10m`)
        const data = await res.json()
    } catch (e) {
        console.error('Error getting Weather data: ', e)
    }
}

getCityCoords()
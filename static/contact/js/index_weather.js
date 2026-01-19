const getCityCoords = async (city) => {
    try {
        const res = await fetch(`https://nominatim.openstreetmap.org/search?q=${city}&format=json&limit=1`)
        const data = await res.json()

        if (data && data.length > 0){
            const coords = {
                lat: data[0].lat,
                lon: data[0].lon
            }
            console.log('coords: ', coords)
            return coords
        }

    } catch (e) {
        console.error('Error getting lattitude and longitude: ', e)
    }
    return null
}

const getWeatherData = async (lat, lon) => {

    try {
        const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,is_day,weather_code,wind_speed_10m`)
        const data = await res.json()
        
        const weatherData = {
            temperature: data.current.temperature_2m,
            humidity: data.current.relative_humidity_2m,
            wind_speed: data.current.wind_speed_10m
        }

        console.log('current: ', weatherData)
        return weatherData
    } catch (e) {
        console.error('Error getting Weather data: ', e)
    }
}

async function displayWeather(element, city) {
    try {
        const { lat, lon } = await getCityCoords(city)
    
        if (!lat && !lon){
            element.innerHTML = '<span>N/A</span>'
            return
        }
    
        const weatherData = await getWeatherData(lat, lon)
        const { temperature, humidity, wind_speed } = weatherData
    
        if (weatherData) {
            element.innerHTML = `
                <div> ${temperature}°C </div>
                <div> ${humidity}% </div>
                <div> ${wind_speed} km/h </div>
            `
        } 
        else {
            element.innerHTML = '<span>N/A</span>'
        }

    } catch (e) {
        console.error('Error displaying weather: ', e)
        element.innerHTML = '<span>Error</span>'
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const weatherElements = document.querySelectorAll('.weather-info')

    weatherElements.forEach(element => {
        const city = element.dataset.city
        if (city) {
            displayWeather(element, city)
        }
    })
})

const CACHE_DURATION = 60 * 60 * 1000


function setCache(key, data) {
    localStorage.setItem(key, JSON.stringify({
        data: data,
        timestamp: Date.now()
    }))
}


function getCache(key, duration=CACHE_DURATION) {
    const cached = localStorage.getItem(key)
    if (cached) {
        const { data, timestamp } = JSON.parse(cached)
        if (Date.now() - timestamp < duration) {
            return data
        }
    }
    return null
}


const getCityCoords = async (city) => {
    const cacheKey = `coords_${city}`
    const cached = getCache(cacheKey)
    console.log('coords cache: ', cached)

    if (cached) {
        return cached
    }

    try {
        const res = await fetch(`https://nominatim.openstreetmap.org/search?q=${city}&format=json&limit=1`)
        const data = await res.json()

        if (data && data.length > 0){
            const coords = {
                lat: data[0].lat,
                lon: data[0].lon
            }

            setCache(cacheKey, coords)
            return coords
        }

    } catch (e) {
        console.error('Error getting lattitude and longitude: ', e)
    }
    return null
}


const getWeatherData = async (lat, lon) => {
    const cacheKey = `weather_${lat}_${lon}`
    const cached = getCache(cacheKey)

    if (cached) {
        return cached
    }

    try {
        const res = await fetch(`https://api.open-meteo.com/v1/forecast?latitude=${lat}&longitude=${lon}&current=temperature_2m,relative_humidity_2m,is_day,weather_code,wind_speed_10m`)
        const data = await res.json()
        
        const weatherData = {
            temperature: data.current.temperature_2m,
            humidity: data.current.relative_humidity_2m,
            wind_speed: data.current.wind_speed_10m
        }

        setCache(cacheKey, weatherData)
        return weatherData
    } catch (e) {
        console.error('Error getting Weather data: ', e)
    }
}


const displayWeather = async(element, city) => {
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
        element.innerHTML = '<span>Weather error</span>'
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

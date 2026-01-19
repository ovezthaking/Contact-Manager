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
        console.error('Error getting latitude and longitude: ', e)
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
        console.error('Error getting weather data: ', e)
    }
}

const displayWeather = async(element, city) => {
    try {
        const coords = await getCityCoords(city)
        
        if (!coords || !coords.lat || !coords.lon){
            element.innerHTML = '<span class="text-xs text-gray-400">Weather unavailable</span>'
            return
        }
    
        const weatherData = await getWeatherData(coords.lat, coords.lon)
    
        if (weatherData) {
            element.innerHTML = `
                <div class="flex items-center gap-3 text-xs text-gray-600">
                    <div class="flex items-center gap-1">
                       <svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" 
                            fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" 
                            stroke-linejoin="round">
                       <path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0Z"></path>
                       </svg> 
                       <span class="font-medium">${weatherData.temperature}°C</span>
                    </div>
                    <div class="flex items-center gap-1">
                        <svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" 
                            fill="none" stroke="#000000" stroke-width="2" stroke-linecap="round" 
                            stroke-linejoin="round">
                        <path 
                            d="M12 22a7 7 0 0 0 7-7c0-2-1-3.9-3-5.5s-3.5-4-4-6.5c-.5 2.5-2 4.9-4 6.5C6 11.1 5 13 5 15a7 7 0 0 0 7 7z">
                        </path>
                        </svg>
                        <span>${weatherData.humidity}%</span>
                    </div>
                    <div class="flex items-center gap-1">
                        <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14 5l7 7m0 0l-7 7m7-7H3"/>
                        </svg>
                        <span>${weatherData.wind_speed} km/h</span>
                    </div>
                </div>
            `
        } else {
            element.innerHTML = '<span class="text-xs text-gray-400">Weather unavailable</span>'
        }

    } catch (e) {
        console.error('Error displaying weather: ', e)
        element.innerHTML = '<span class="text-xs text-gray-400">Weather error</span>'
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
console.log('test mail: ', validator.isEmail('test@gmail.com'))
document.querySelector('form').addEventListener('submit', (e) => {
    const alertList = []
    const email = document.getElementById('id_email').value.trim()
    const phone_number = document.getElementById('id_phone_number').value.replace(/\s+/g,'')

    if(!validator.isEmail(email)){
        e.preventDefault()
        let mailAlert = 'Invalid email address'
        alertList.push(mailAlert)
    }

    if(!validator.isMobilePhone(phone_number, 'any')){
        e.preventDefault()
        let phoneAlert = 'Invalid phone number'
        alertList.push(phoneAlert)
    }

    document.querySelector('ul').innerHTML = ''
    alertList.forEach(alert => {
        document.querySelector('ul').innerHTML += `
            <svg class="w-5 h-5 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
            <span>${alert}</span>
        `
    })
})

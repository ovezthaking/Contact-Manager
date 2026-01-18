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

    if(!validator.isMobilePhone(phone_number)){
        e.preventDefault()
        let phoneAlert = 'Invalid phone number'
        alertList.push(phoneAlert)
    }
    document.querySelector('ul').innerHTML = ''
    alertList.forEach(alert => {
        document.querySelector('ul').innerHTML += `
            <li>${alert}</li>
        `
    })
    

})
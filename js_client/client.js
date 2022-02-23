const loginForm = document.getElementById('login-form')
const baseEndpoint = "http://localhost:8000/api"
if (loginForm) {
    // handle this login form
    loginForm.addEventListener('submit', handleLogin)
}

function handleLogin(event) {
    console.log(event)
    event.preventDefault()
    const loginEndpoint = `${baseEndpoint}/token/`
    let loginFormData = new FormData(loginForm)
    let loginObjectData = Object.fromEntries(loginFormData)
    let bodyStr = JSON.stringify(loginObjectData)
    const options = {
        method: "POST",
        headers: {
            "ContentType": "application/json"
        },
        body: bodyStr
    }
    fetch(loginEndpoint, options) //  Promise
    .then(response=>{
        console.log(response)
        return response.json()
    })
    .then(x => {
        console.log(x)
    })
    .catch(err=> {
        console.log('err', err)
    })
}
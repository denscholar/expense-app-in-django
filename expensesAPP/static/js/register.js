const usernameField = document.getElementById('username')
const usernameFeedbackArea = document.querySelector('.invalid_feedback')
const emailField = document.querySelector('#emailField')
const emailFeedBack = document.querySelector('.emailFeedBack')
const showPassword = document.querySelector('.show-password')
const password = document.querySelector('#password')
const submitButton = document.querySelector('.btn-disable')

console.log(submitButton)

usernameField.addEventListener('keyup', (e)=>{
    e.preventDefault()
    const inputValue = e.target.value;

    usernameField.classList.remove("is_invalid")
    usernameFeedbackArea.style.display = 'none'
   
    if (inputValue.length > 0) {
        fetch("/authentication/validate-username", {
            body: JSON.stringify({username: inputValue}),
            method: "POST",
        })
        .then((res) =>res.json())
        .then((data)=>{
            console.log('data', data);
            if(data.username_error){
                submitButton.disabled = true
                usernameField.classList.add("is_invalid")
                usernameFeedbackArea.style.display = 'block'
                usernameFeedbackArea.innerHTML = `<p>${data.username_error}</p>`
            }else{
                submitButton.disabled = false
            }
        })
    }
});

emailField.addEventListener('keyup', (e)=>{
    e.preventDefault()
    const emailValue = e.target.value;

    emailField.classList.remove("is_invalid")
    emailFeedBack.style.display = 'none'
   
    if (emailValue.length > 0) {
        fetch("/authentication/validate-email", {
            body: JSON.stringify({email: emailValue}),
            method: "POST",
        })
        .then((res) =>res.json())
        .then((data)=>{
            console.log('data', data);
            if(data.email_error){
                submitButton.disabled = true
                emailField.classList.add("is_invalid")
                emailFeedBack.style.display = 'block'
                emailFeedBack.innerHTML = `<p>${data.email_error}</p>`
            }else{
                submitButton.disabled = false
            }
        })
    }
});

showPassword.addEventListener('click', ()=>{
    if (password.type === "password") {  
        password.type = "text";
        showPassword.innerHTML = 'HIDE'
      } else {  
        password.type = "password";
        showPassword.innerHTML = 'SHOW'
      } 
})
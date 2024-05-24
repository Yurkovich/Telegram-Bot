
const sendButton = document.getElementById("submitButton")
sendButton.addEventListener('click', async function(event) {
    event.preventDefault();
    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const username = usernameInput.value;
    const password = passwordInput.value;
    const data = {"username": username, "password": password};
    console.log(data);
    try {
        const response = await fetch('http://127.0.0.1:8000/register/', {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert('Вы успешно зарегистрировались!');
            usernameInput.value = '';
            passwordInput.value = '';
        } else {
            alert('Ошибка!');
        }
    } catch (error) {
        alert('Ошибка!');
        console.error(error);
    }
});

const noAccount = document.getElementById('noAccount')
noAccount.addEventListener('click', async function(event) {
    event.preventDefault();
    window.location.href = "/signup"
})

const sendButton = document.getElementById("submitButton")
sendButton.addEventListener('click', async function(event) {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const data = {"username": username, "password": password};
    console.log(data);
    try {
        const response = await fetch('http://127.0.0.1:8000/users/', {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert('User registered successfully!');
        } else {
            alert('Registration failed');
        }
    } catch (error) {
        alert('Registration failed');
        console.error(error);
    }
});
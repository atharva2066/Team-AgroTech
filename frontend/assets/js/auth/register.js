async function handleRegister() {
  const name = document.getElementById("name").value;
  const phone = document.getElementById("phone").value;
  const password = document.getElementById("password").value;
  const role = document.getElementById("role").value;

  const body = {
    name,
    phone,
    password,
    role
  };

  try {
    const response = await fetch("http://127.0.0.1:8000/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body)
    });

    const data = await response.json();

    if (response.ok) {
      alert("Registration successful!");
      window.location.href = "/login/login.html";
    } else {
      alert("Error: " + data.detail);
    }

  } catch (err) {
    alert("Network error. Please check your backend server.");
  }
}
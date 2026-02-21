async function handleLogin() {
  const phone = document.getElementById("phone").value;
  const password = document.getElementById("password").value;

  const body = { phone, password };

  try {
    const response = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });

    const data = await response.json();

    if (response.ok) {
      // Save user info
      localStorage.setItem("user", JSON.stringify(data));

      // Redirect based on role
      if (data.role === "farmer") {
        window.location.href = "farmer-dashboard.html";
      } else if (data.role === "company") {
        window.location.href = "buyer-dashboard.html";
      } else {
        alert("Unknown role. Cannot redirect.");
      }
    } else {
      alert("Error: " + data.detail);
    }

  } catch (err) {
    alert("Network error. Check backend.");
  }
}
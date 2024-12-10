const apiBaseURL = "http://127.0.0.1:8000"; // URL de tu API FastAPI

// Registrar Comprador
document.getElementById("customerForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const customerData = {
        FullName: document.getElementById("customerFullName").value,
        PhoneNumber: document.getElementById("customerPhoneNumber").value,
        CreditCardNumber: document.getElementById("customerCreditCardNumber").value,
        Username: document.getElementById("customerUsername").value,
        PasswordHash: document.getElementById("customerPassword").value,
        salt: "",
    };

    try {
        const response = await fetch(`${apiBaseURL}/customers/`, { // Cambiado a /customers/
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(customerData),
        });

        if (response.ok) {
            alert("Comprador registrado con éxito.");
            document.getElementById("customerForm").reset();
        } else {
            const error = await response.json();
            alert(`Error: ${error.detail}`);
        }
    } catch (err) {
        console.error(err);
        alert("Ocurrió un error al registrar el comprador.");
    }
});

// registrar empleado
document.getElementById("employeeForm").addEventListener("submit", async (e) => {
    e.preventDefault(); // Evitar el envío predeterminado del formulario

    const employeeData = {
        FullName: document.getElementById("employeeFullName").value,
        Username: document.getElementById("employeeUsername").value,
        PasswordHash: document.getElementById("employeePassword").value,
        PublicKeyECDSA: "", // Este campo será generado automáticamente
        salt: "",
    };

    try {
        const response = await fetch(`${apiBaseURL}/employees/`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(employeeData),
        });

        if (response.ok) {
            const result = await response.json();
            console.log("Respuesta del servidor:", result);

            // Redirigir a la página de éxito con la URL de la llave privada
            if (result.private_key_url) {
                // Redirigir a success.html con el parámetro private_key_url
                window.location.href = `success.html?private_key_url=${apiBaseURL}${result.private_key_url}`;
            } else {
                alert("No se pudo generar el enlace de descarga.");
            }            

            document.getElementById("employeeForm").reset();
        } else {
            const error = await response.json();
            alert(`Error: ${error.detail}`);
        }
    } catch (err) {
        console.error(err);
        alert("Ocurrió un error al registrar el empleado.");
    }
});

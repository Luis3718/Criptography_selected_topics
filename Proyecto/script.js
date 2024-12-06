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

// Registrar Empleado
document.getElementById("employeeForm").addEventListener("submit", async (e) => {
    e.preventDefault();

    const employeeData = {
        FullName: document.getElementById("employeeFullName").value,
        Username: document.getElementById("employeeUsername").value,
        PasswordHash: document.getElementById("employeePassword").value,
        PublicKeyECDSA: document.getElementById("employeePublicKey").value,
    };

    try {
        const response = await fetch(`${apiBaseURL}/employees/`, { // Cambiado a /employees/
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(employeeData),
        });

        if (response.ok) {
            alert("Empleado registrado con éxito.");
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

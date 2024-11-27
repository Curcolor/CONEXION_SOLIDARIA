document.getElementById("orgForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const nombre = document.querySelector("input[type='text']").value;
    const descripcion = document.querySelector("textarea").value;
    const categoria = document.querySelector("select").value;

    const data = {
        nombre: nombre,
        descripcion: descripcion,
        categoria: categoria
    };

    let mensajeElement = document.getElementById("mensaje-respuesta");
    if (!mensajeElement) {
        mensajeElement = document.createElement("div");
        mensajeElement.id = "mensaje-respuesta";
        document.getElementById("orgForm").insertAdjacentElement('afterend', mensajeElement);
    }

    fetch("/src/templates/pages/html/nuevaOR.html", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        mensajeElement.className = data.success ? 'alert alert-success' : 'alert alert-danger';
        mensajeElement.textContent = data.message;
        
        if (data.error) {
            console.error("Error detallado:", data.error);
            mensajeElement.textContent += ` (${data.error})`;
        }

        if (data.success) {
            setTimeout(() => {
                window.location.href = "/src/templates/pages/html/organizaciones.html";
            }, 2000);
        }
    })
    .catch(error => {
        console.error("Error:", error);
        mensajeElement.className = 'alert alert-danger';
        mensajeElement.textContent = "Hubo un error al enviar los datos.";
    });
});

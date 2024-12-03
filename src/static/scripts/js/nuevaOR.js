console.log('Script de nueva organización cargado');

const form = document.getElementById('orgForm');
if (form) {
    console.log('Formulario de organización encontrado');
    iniciarProcesoCreacionOrganizacion();
} else {
    console.error('Formulario de organización no encontrado');
}

function iniciarProcesoCreacionOrganizacion() {
    document.getElementById('orgForm').addEventListener('submit', async function(event) {
        event.preventDefault();
        console.log('Formulario de organización enviado');

        // Obtener los valores del formulario
        const nombreInput = document.querySelector("input[name='nombre']");
        const descripcionInput = document.querySelector("textarea[name='descripcion']");
        const categoriaInput = document.querySelector("select[name='categoria']");
        const imagenInput = document.querySelector("input[name='imagen']");

        // Crear objeto con los datos
        const data = {
            nombre: nombreInput ? nombreInput.value : '',
            descripcion: descripcionInput ? descripcionInput.value : '',
            categoria: categoriaInput ? categoriaInput.value : '',
            imagen_url: null
        };

        // Procesar imagen si existe
        if (imagenInput && imagenInput.files && imagenInput.files.length > 0) {
            try {
                const file = imagenInput.files[0];
                const base64Image = await convertirImagenABase64(file);
                data.imagen_url = base64Image;
            } catch (error) {
                console.error('Error al procesar la imagen:', error);
            }
        }

        console.log('Datos del formulario:', data);

        try {
            console.log('Enviando datos al servidor...');
            const response = await fetch('/src/templates/pages/nuevaOR.html', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            const result = await response.json();

            let mensajeElement = document.getElementById("mensaje-respuesta");
            if (!mensajeElement) {
                mensajeElement = document.createElement("div");
                mensajeElement.id = "mensaje-respuesta";
                form.insertAdjacentElement('afterend', mensajeElement);
            }

            if (response.ok && result.success) {
                console.log('Organización creada con éxito:', result.message);
                mensajeElement.className = 'alert alert-success';
                mensajeElement.textContent = result.message;
                
                setTimeout(() => {
                    //window.location.href = "/src/templates/pages/html/organizaciones.html";
                }, 2000);
            } else {
                console.error('Error al crear la organización:', result.error);
                mensajeElement.className = 'alert alert-danger';
                mensajeElement.textContent = result.message;
                if (result.error) {
                    mensajeElement.textContent += ` (${result.error})`;
                }
            }
        } catch (error) {
            console.error('Error:', error);
            let mensajeElement = document.getElementById("mensaje-respuesta");
            if (mensajeElement) {
                mensajeElement.className = 'alert alert-danger';
                mensajeElement.textContent = "Hubo un error al enviar los datos.";
            }
        }
    });
}

// Función auxiliar para convertir imagen a base64
function convertirImagenABase64(file) {
    return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onload = () => resolve(reader.result);
        reader.onerror = reject;
        reader.readAsDataURL(file);
    });
}

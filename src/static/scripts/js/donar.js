// Variables globales
let organizacionesPorTipo = {};
let proyectoSeleccionado = null;

// Cargar datos cuando se inicia la página
document.addEventListener('DOMContentLoaded', async () => {
    // Obtener el ID del proyecto de la URL si existe
    const urlParams = new URLSearchParams(window.location.search);
    proyectoSeleccionado = urlParams.get('proyecto');

    // Cargar las organizaciones
    const organizaciones = await obtenerOrganizaciones();
    await mostrarOrganizacionesEnSelect(organizaciones);
    
    // Configurar los event listeners
    configurarEventListeners();
});

// Función para cargar las organizaciones
async function obtenerOrganizaciones() {
    try {
        const respuesta = await fetch('/api/organizaciones', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (!respuesta.ok) {
            throw new Error('Error al obtener las organizaciones');
        }

        const datos = await respuesta.json();
        if (!datos.success) {
            throw new Error(datos.message || 'Error al obtener las organizaciones');
        }

        return datos.organizaciones;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Función para mostrar las organizaciones en el select
function mostrarOrganizacionesEnSelect(organizaciones) {
    const selectOrg = document.getElementById('organizacion');
    if (!selectOrg) return;

    // Opción por defecto
    selectOrg.innerHTML = '<option value="">Seleccione una organización</option>';

    // Añadir cada organización como una opción
    organizaciones.forEach(org => {
        selectOrg.innerHTML += `
            <option value="${org.id}">
                ${org.nombre} - ${org.categoria}
            </option>
        `;
    });
}

// Configurar event listeners
function configurarEventListeners() {
    const tipoAyudaSelect = document.getElementById('tipo_ayuda');
    const organizacionSelect = document.getElementById('organizacion');
    const formDonacion = document.getElementById('form_donacion');

    tipoAyudaSelect.addEventListener('change', actualizarOrganizaciones);
    formDonacion.addEventListener('submit', procesarDonacion);
}

// Actualizar lista de organizaciones según el tipo de ayuda
function actualizarOrganizaciones() {
    const tipoAyuda = document.getElementById('tipo_ayuda').value;
    const organizacionSelect = document.getElementById('organizacion');
    
    organizacionSelect.innerHTML = '<option value="">Seleccione una organización</option>';

    if (tipoAyuda && organizacionesPorTipo[tipoAyuda]) {
        organizacionesPorTipo[tipoAyuda].forEach(org => {
            const option = document.createElement('option');
            option.value = org.id;
            option.textContent = org.nombre;
            organizacionSelect.appendChild(option);
        });
    }
}


// Procesar la donación
async function procesarDonacion(event) {
    event.preventDefault();

    // Verificar si el usuario está logueado
    const sessionResponse = await fetch('/api/session-status');
    const sessionData = await sessionResponse.json();

    if (!sessionData.logged_in) {
        mostrarMensaje('Debe iniciar sesión para realizar una donación', 'error');
        setTimeout(() => {
            window.location.href = '/iniciarSesion';
        }, 2000);
        return;
    }

    const tipoAyuda = document.getElementById('tipo_ayuda').value;
    const organizacionId = document.getElementById('organizacion').value;
    const monto = document.getElementById('monto_personalizado').value;

    if (!tipoAyuda || !organizacionId || !monto) {
        mostrarMensaje('Por favor complete todos los campos', 'error');
        return;
    }

    try {
        const donacionData = {
            monto: parseFloat(monto),
            tipo_ayuda: tipoAyuda,
            usuarios_id_usuario: sessionData.usuario.id,
            proyectos_id_proyecto: proyectoSeleccionado || null,
            organizaciones_id_organizacion: parseInt(organizacionId)
        };

        const response = await fetch('/api/donaciones', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(donacionData)
        });

        const data = await response.json();

        if (data.success) {
            mostrarMensaje('¡Donación realizada con éxito!', 'success');
            setTimeout(() => {
                window.location.href = '/proyectos';
            }, 2000);
        } else {
            throw new Error(data.message || 'Error al procesar la donación');
        }

    } catch (error) {
        console.error('Error:', error);
        mostrarMensaje(error.message || 'Error al procesar la donación', 'error');
    }
}

// Función para mostrar mensajes
function mostrarMensaje(mensaje, tipo) {
    const container = document.querySelector('.container');
    const mensajeExistente = document.querySelector('.mensaje');
    
    if (mensajeExistente) {
        mensajeExistente.remove();
    }

    const mensajeElement = document.createElement('div');
    mensajeElement.className = `mensaje mensaje-${tipo}`;
    mensajeElement.innerHTML = `
        <i class="fas ${tipo === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'}"></i>
        ${mensaje}
    `;

    container.insertBefore(mensajeElement, container.firstChild);

    // Remover el mensaje después de 5 segundos
    setTimeout(() => {
        mensajeElement.remove();
    }, 5000);
}
// Estilos CSS para los mensajes (agregar al archivo CSS)
const estilos = `
.mensaje {
    padding: 15px;
    margin-bottom: 20px;
    border-radius: 5px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.mensaje-success {
    background-color: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
}

.mensaje-error {
    background-color: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
}

.mensaje i {
    font-size: 1.2em;
}
`;

// Agregar estilos dinámicamente
const styleSheet = document.createElement('style');
styleSheet.textContent = estilos;
document.head.appendChild(styleSheet);


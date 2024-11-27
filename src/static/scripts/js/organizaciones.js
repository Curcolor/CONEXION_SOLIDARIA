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

function mostrarOrganizaciones(organizaciones) {
    const tbody = document.querySelector('#organizacionesTable tbody');
    if (!tbody) return;

    tbody.innerHTML = organizaciones.map(org => `
        <tr class="organizacion-row">
            <td class="org-imagen">
                <img src="${org.imagen_url || '/static/img/default-org.png'}" alt="${org.nombre}">
            </td>
            <td class="org-nombre">${org.nombre}</td>
            <td class="org-descripcion">${org.descripcion}</td>
            <td class="org-categoria">${org.categoria}</td>
            <td class="org-creador">${org.creador}</td>
            <td class="org-fecha">${new Date(org.fecha_registro).toLocaleDateString()}</td>
            <td class="org-acciones">
                <button onclick="borrarOrganizacion(${org.id})" class="btn-eliminar">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

// Cargar organizaciones cuando la página se cargue
document.addEventListener('DOMContentLoaded', () => {
    obtenerOrganizaciones()
        .then(organizaciones => {
            mostrarOrganizaciones(organizaciones);
        })
        .catch(error => {
            console.error('Error al cargar organizaciones:', error);
            // Mostrar mensaje de error al usuario
            const contenedor = document.getElementById('organizaciones-container');
            if (contenedor) {
                contenedor.innerHTML = '<p class="error">Error al cargar las organizaciones. Por favor, intente más tarde.</p>';
            }
        });
});

// Borrar una organización específica
async function borrarOrganizacion(id) {
    try {
        const respuesta = await fetch(`/api/organizaciones/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const datos = await respuesta.json();
        if (!datos.success) {
            throw new Error(datos.message);
        }

        // Actualizar la vista después de borrar
        const organizaciones = await obtenerOrganizaciones();
        mostrarOrganizaciones(organizaciones);
        
        return datos;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// Borrar todas las organizaciones
async function borrarTodasOrganizaciones() {
    if (!confirm('¿Estás seguro de que deseas borrar todas las organizaciones? Esta acción no se puede deshacer.')) {
        return;
    }

    try {
        const respuesta = await fetch('/api/organizaciones/borrar-todo', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const datos = await respuesta.json();
        if (!datos.success) {
            throw new Error(datos.message);
        }

        // Limpiar el contenedor de organizaciones
        const contenedor = document.getElementById('organizaciones-container');
        if (contenedor) {
            contenedor.innerHTML = '<p>No hay organizaciones para mostrar.</p>';
        }
        
        return datos;
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}
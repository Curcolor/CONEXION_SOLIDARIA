// Objeto con las organizaciones disponibles por tipo de ayuda
const organizacionesPorTipo = {
    'salud': [
        { id: 'org1', nombre: 'Hospital San Juan' },
        { id: 'org2', nombre: 'Clínica Bienestar' }
        // Aquí se pueden agregar más organizaciones de salud
    ],
    'alimentaria': [
        { id: 'org3', nombre: 'Banco de Alimentos' },
        { id: 'org4', nombre: 'Comedores Solidarios' }
        // Aquí se pueden agregar más organizaciones alimentarias
    ],
    'educativa': [
        { id: 'org5', nombre: 'Fundación Educativa' },
        { id: 'org6', nombre: 'Escuelas Unidas' }
        // Aquí se pueden agregar más organizaciones educativas
    ],
    'vivienda': [
        { id: 'org7', nombre: 'Construyendo Hogares' },
        { id: 'org8', nombre: 'Techo para Todos' }
        // Aquí se pueden agregar más organizaciones de vivienda
    ]
};

// Función para actualizar las organizaciones según el tipo de ayuda seleccionado
function actualizarOrganizaciones() {
    const tipoAyudaSelect = document.getElementById('tipo_ayuda');
    const organizacionSelect = document.getElementById('organizacion');
    const tipoAyuda = tipoAyudaSelect.value;
    
    // Limpiar opciones actuales
    organizacionSelect.innerHTML = '<option value="">Seleccione una organización</option>';
    
    // Si hay un tipo de ayuda seleccionado, mostrar las organizaciones correspondientes
    if (tipoAyuda && organizacionesPorTipo[tipoAyuda]) {
        organizacionesPorTipo[tipoAyuda].forEach(org => {
            const option = document.createElement('option');
            option.value = org.id;
            option.textContent = org.nombre;
            organizacionSelect.appendChild(option);
        });
    }
}

// Agregar event listener cuando se carga el documento
document.addEventListener('DOMContentLoaded', async () => {
    // Obtener el ID del proyecto de la URL si existe
    const urlParams = new URLSearchParams(window.location.search);
    const proyectoId = urlParams.get('proyecto_id');

    if (proyectoId) {
        // Si hay un proyecto específico, mostrar ese formulario y ocultar el general
        document.getElementById('proyecto-especifico').style.display = 'block';
        document.getElementById('donacion-general').style.display = 'none';
        
        try {
            // Obtener información del proyecto
            const response = await fetch(`/api/proyectos/${proyectoId}`);
            const data = await response.json();
            
            if (data.success) {
                const proyecto = data.proyecto;
                document.getElementById('proyecto_id').value = proyecto.id;
                document.getElementById('proyecto-titulo').textContent = proyecto.titulo;
                document.getElementById('proyecto-organizacion').textContent = proyecto.organizacion_nombre;
                document.getElementById('proyecto-meta').textContent = proyecto.meta_financiera.toLocaleString();
                document.getElementById('proyecto-recaudado').textContent = proyecto.monto_recaudado.toLocaleString();
            } else {
                throw new Error('No se pudo cargar la información del proyecto');
            }
        } catch (error) {
            console.error('Error:', error);
            // Mostrar mensaje de error
            document.getElementById('proyecto-especifico').innerHTML = 
                '<p class="error">Error al cargar la información del proyecto</p>';
        }
    } else {
        // Si no hay proyecto específico, mostrar el formulario general
        document.getElementById('proyecto-especifico').style.display = 'none';
        document.getElementById('donacion-general').style.display = 'block';
    }

    // Manejar el envío del formulario de donación específica
    const formDonacionProyecto = document.getElementById('form_donacion_proyecto');
    if (formDonacionProyecto) {
        formDonacionProyecto.addEventListener('submit', async (e) => {
            e.preventDefault();
            const monto = document.getElementById('monto_donacion').value;
            const proyecto_id = document.getElementById('proyecto_id').value;

            try {
                const response = await fetch('/api/donaciones', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        proyecto_id,
                        monto: parseFloat(monto)
                    })
                });

                const data = await response.json();
                if (data.success) {
                    alert('¡Donación realizada con éxito!');
                    window.location.href = '/proyectos';
                } else {
                    throw new Error(data.message);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error al procesar la donación');
            }
        });
    }

    // ... resto del código existente para el formulario general ...
});

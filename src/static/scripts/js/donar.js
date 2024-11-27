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
document.addEventListener('DOMContentLoaded', function() {
    const tipoAyudaSelect = document.getElementById('tipo_ayuda');
    tipoAyudaSelect.addEventListener('change', actualizarOrganizaciones);
});

// Objeto con los tipos de ayuda disponibles por organización
const tiposAyuda = {
    'organizacion_salud': ['Medicamentos', 'Equipos médicos', 'Atención médica', 'Otros'],
    'organizacion_educativa': ['Útiles escolares', 'Becas', 'Material didáctico', 'Otros'],
    'organizacion_alimentaria': ['Alimentos no perecederos', 'Comedores comunitarios', 'Otros'],
    'organizacion_vivienda': ['Materiales de construcción', 'Mejoras de vivienda', 'Otros']
};

// Montos sugeridos por tipo de ayuda (en pesos mexicanos)
const montosSugeridos = {
    'Medicamentos': [100, 200, 500, 1000],
    'Equipos médicos': [1000, 2000, 5000, 10000],
    'Atención médica': [300, 500, 1000, 2000],
    'Útiles escolares': [200, 500, 1000, 2000],
    'Becas': [1000, 2000, 5000, 10000],
    'Material didáctico': [300, 500, 1000, 2000],
    'Alimentos no perecederos': [200, 500, 1000, 2000],
    'Comedores comunitarios': [500, 1000, 2000, 5000],
    'Materiales de construcción': [1000, 2000, 5000, 10000],
    'Mejoras de vivienda': [2000, 5000, 10000, 20000],
    'Otros': [100, 200, 500, 1000]
};

// Función para actualizar el select de tipos de ayuda
function actualizarTiposAyuda() {
    const organizacionSelect = document.getElementById('organizacion');
    const tipoAyudaSelect = document.getElementById('tipo_ayuda');
    const organizacion = organizacionSelect.value;
    
    // Limpiar opciones actuales
    tipoAyudaSelect.innerHTML = '<option value="">Seleccione el tipo de ayuda</option>';
    
    // Si hay una organización seleccionada, agregar sus tipos de ayuda
    if (organizacion && tiposAyuda[organizacion]) {
        tiposAyuda[organizacion].forEach(tipo => {
            const option = document.createElement('option');
            option.value = tipo;
            option.textContent = tipo;
            tipoAyudaSelect.appendChild(option);
        });
    }
}

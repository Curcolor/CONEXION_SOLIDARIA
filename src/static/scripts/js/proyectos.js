// Función para cargar las organizaciones y crear proyectos
async function cargarProyectos() {
    try {
        // Obtener el contenedor de proyectos
        const projectList = document.getElementById('projectList');
        
        // Limpiar el contenedor
        projectList.innerHTML = '';

        // Insertar el proyecto de prueba fijo
        const proyectoPrueba = `
            <div class="project-card">
                <img src="/src/static/images/helpp.jpg" alt="Proyecto de Educación">
                <div class="project-content">
                    <h3 class="project-title">Educación para Todos</h3>
                    <p class="organization-name"><i class="fas fa-building"></i> Fundación Educativa</p>
                    <p class="project-description">Ayudando a niños de bajos recursos a acceder a educación de calidad
                    </p>
                    <div class="project-meta">
                        <div class="meta-item">
                            <span>Meta: $10,000</span>
                            <span>Recaudado: $7,500</span>
                        </div>
                        <div class="progress-bar">
                            <div class="progress" style="width: 75%"></div>
                        </div>
                        <p class="progress-text">75% completado</p>
                    </div>
                    <div class="project-actions">
                        <button class="btn-donar"><i class="fas fa-hand-holding-heart"></i> Donar</button>
                    </div>
                </div>
            </div>
        `;
        
        projectList.innerHTML = proyectoPrueba;

        // Obtener las organizaciones registradas
        const response = await fetch('/api/organizaciones');
        const organizaciones = await response.json();

        // Crear una tarjeta de proyecto para cada organización
        organizaciones.forEach(org => {
            const projectCard = crearTarjetaProyecto(org);
            projectList.appendChild(projectCard);
        });

    } catch (error) {
        console.error('Error al cargar los proyectos:', error);
    }
}

// Función para crear una tarjeta de proyecto individual
function crearTarjetaProyecto(organizacion) {
    // Crear elemento div para la tarjeta
    const card = document.createElement('div');
    card.className = 'project-card';

    // Generar un valor aleatorio para el progreso (solo para demostración)
    const progreso = Math.floor(Math.random() * 100);
    const meta = 10000;
    const recaudado = (meta * progreso) / 100;

    card.innerHTML = `
        <img src="${organizacion.imagen || '/src/static/images/helpp.jpg'}" alt="Proyecto de ${organizacion.nombre}">
        <div class="project-content">
            <h3 class="project-title">Proyecto ${organizacion.nombre}</h3>
            <p class="organization-name">
                <i class="fas fa-building"></i> ${organizacion.nombre}
            </p>
            <p class="project-description">${organizacion.descripcion}</p>
            <div class="project-meta">
                <div class="meta-item">
                    <span>Meta: $${meta.toLocaleString()}</span>
                    <span>Recaudado: $${recaudado.toLocaleString()}</span>
                </div>
                <div class="progress-bar">
                    <div class="progress" style="width: ${progreso}%"></div>
                </div>
                <p class="progress-text">${progreso}% completado</p>
            </div>
            <div class="project-actions">
                <button class="btn-donar" onclick="donarProyecto('${organizacion.id}')">
                    <i class="fas fa-hand-holding-heart"></i> Donar
                </button>
            </div>
        </div>
    `;

    return card;
}

// Función para manejar la donación
function donarProyecto(organizacionId) {
    // Redirigir a la página de donación con el ID de la organización
    window.location.href = `/src/templates/pages/donar.html?org=${organizacionId}`;
}

// Cargar los proyectos cuando la página se cargue
document.addEventListener('DOMContentLoaded', cargarProyectos);

// Función para actualizar los proyectos periódicamente (opcional)
setInterval(cargarProyectos, 300000); // Actualizar cada 5 minutos



class DonationPlatform {
    constructor() {
        this.projects = [
            {
                id: 1,
                title: "Educación para Todos",
                description: "Ayuda a niños de zonas rurales a acceder a educación de calidad",
                goal: 10000,
                current: 5600,
                organization: "Fundación Educativa",
                category: "educacion",
                image: "https://via.placeholder.com/300x200"
            },
            {
                id: 2,
                title: "Agua Limpia",
                description: "Proyecto para proporcionar agua potable a comunidades necesitadas",
                goal: 15000,
                current: 7800,
                organization: "Agua para Todos",
                category: "social",
                image: "https://via.placeholder.com/300x200"
            }
        ];

        this.initializeDashboard();
        this.renderProjects();
        this.initializeEventListeners();
    }

    initializeDashboard() {
        document.getElementById('totalDonations').textContent = 
            `$${this.projects.reduce((sum, p) => sum + p.current, 0).toLocaleString()}`;
        document.getElementById('activeProjects').textContent = this.projects.length;
        document.getElementById('registeredOrgs').textContent = 
            new Set(this.projects.map(p => p.organization)).size;
    }

    renderProjects() {
        const projectList = document.getElementById('projectList');
        projectList.innerHTML = '';

        this.projects.forEach(project => {
            const progress = (project.current / project.goal) * 100;
            const card = document.createElement('div');
            card.className = 'project-card';
            card.innerHTML = `
                <img src="${project.image}" alt="${project.title}" class="project-img">
                <div class="project-info">
                    <h3>${project.title}</h3>
                    <p>${project.description}</p>
                    <p><strong>Organización:</strong> ${project.organization}</p>
                    <div class="progress-bar">
                        <div class="progress" style="width: ${progress}%"></div>
                    </div>
                    <p>$${project.current.toLocaleString()} de $${project.goal.toLocaleString()}</p>
                    <button class="btn" onclick="platform.donate(${project.id})">Donar</button>
                </div>
            `;
            projectList.appendChild(card);
        });
    }

    donate(projectId) {
        const amount = prompt('Ingrese el monto a donar:');
        if (amount && !isNaN(amount)) {
            const project = this.projects.find(p => p.id === projectId);
            if (project) {
                project.current += Number(amount);
                this.initializeDashboard();
                this.renderProjects();
                alert('¡Gracias por tu donación!');
            }
        }
    }

    initializeEventListeners() {
        document.getElementById('orgForm').addEventListener('submit', (e) => {
            e.preventDefault();
            alert('Organización registrada exitosamente');
            e.target.reset();
        });
    }
}

const platform = new DonationPlatform();

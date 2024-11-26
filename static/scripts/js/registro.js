function validarFormulario() {
    // Validar contraseña
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    
    if (password !== confirmPassword) {
        alert('Las contraseñas no coinciden');
        return false;
    }

    // Validar formato de contraseña
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
    if (!passwordRegex.test(password)) {
        alert('La contraseña debe tener al menos 8 caracteres, una mayúscula, una minúscula y un número');
        return false;
    }

    // Validar áreas de interés
    const intereses = document.querySelectorAll('input[name="intereses"]:checked');
    if (intereses.length === 0) {
        alert('Por favor seleccione al menos un área de interés');
        return false;
    }

    // Validar edad mínima (18 años)
    const fechaNacimiento = new Date(document.getElementById('fechaNacimiento').value);
    const hoy = new Date();
    const edad = hoy.getFullYear() - fechaNacimiento.getFullYear();
    if (edad < 18) {
        alert('Debes ser mayor de 18 años para registrarte');
        return false;
    }

    // Si todo está correcto, enviar el formulario
    alert('Registro exitoso! Serás redirigido al inicio de sesión');
    window.location.href = '/templates/pages/html/login.html';
    return false; // Prevenir el envío del formulario (en un caso real, aquí harías el envío a tu backend)
}

// Validación en tiempo real de la contraseña
document.getElementById('password').addEventListener('input', function() {
    const password = this.value;
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$/;
    
    if (passwordRegex.test(password)) {
        this.style.borderColor = 'green';
    } else {
        this.style.borderColor = 'red';
    }
});

// Validación en tiempo real de confirmación de contraseña
document.getElementById('confirmPassword').addEventListener('input', function() {
    const password = document.getElementById('password').value;
    if (this.value === password) {
        this.style.borderColor = 'green';
    } else {
        this.style.borderColor = 'red';
    }
});

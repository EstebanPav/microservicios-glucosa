const BASE_URL = "http://localhost:5000/pacientes";

// 📌 Crear paciente
async function registrarPaciente(event) {
    event.preventDefault();

    const paciente = {
        nombre: document.getElementById('nombre').value,
        edad: document.getElementById('edad').value,
        historial: document.getElementById('historial').value
    };

    try {
        const response = await fetch(BASE_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(paciente)
        });

        if (response.ok) {
            alert('✅ Paciente registrado correctamente');
            obtenerPacientes(); // Actualiza la lista
            limpiarFormulario();
        } else {
            throw new Error('❌ Error al registrar paciente');
        }
    } catch (error) {
        alert(error.message);
    }
}

// 📌 Obtener pacientes (Listar)
async function obtenerPacientes() {
    try {
        const response = await fetch(BASE_URL);
        const pacientes = await response.json();

        const container = document.getElementById('pacientes-container');
        container.innerHTML = '';

        pacientes.forEach(paciente => {
            container.innerHTML += `
                <tr>
                    <td>${paciente.id}</td>
                    <td>${paciente.nombre}</td>
                    <td>${paciente.edad}</td>
                    <td>${paciente.historial}</td>
                    <td>
                        <button onclick="editarPaciente(${paciente.id}, '${paciente.nombre}', ${paciente.edad}, '${paciente.historial}')">✏️ Editar</button>
                        <button onclick="eliminarPaciente(${paciente.id})">🗑️ Eliminar</button>
                    </td>
                </tr>
            `;
        });
    } catch (error) {
        console.error('❌ Error al obtener pacientes:', error);
    }
}

// 📌 Actualizar paciente
async function actualizarPaciente(event) {
    event.preventDefault();

    const id = document.getElementById('paciente-id').value;
    const paciente = {
        nombre: document.getElementById('edit-nombre').value,
        edad: document.getElementById('edit-edad').value,
        historial: document.getElementById('edit-historial').value
    };

    try {
        const response = await fetch(`${BASE_URL}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(paciente)
        });

        if (response.ok) {
            alert('✅ Paciente actualizado correctamente');
            obtenerPacientes(); // Actualiza la lista
            cerrarModal();
        } else {
            throw new Error('❌ Error al actualizar paciente');
        }
    } catch (error) {
        alert(error.message);
    }
}

// 📌 Eliminar paciente
async function eliminarPaciente(id) {
    if (!confirm('¿Estás seguro de eliminar este paciente?')) return;

    try {
        const response = await fetch(`${BASE_URL}/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('✅ Paciente eliminado correctamente');
            obtenerPacientes(); // Actualiza la lista
        } else {
            throw new Error('❌ Error al eliminar paciente');
        }
    } catch (error) {
        alert(error.message);
    }
}

// 📌 Cargar datos en el modal para editar
function editarPaciente(id, nombre, edad, historial) {
    document.getElementById('paciente-id').value = id;
    document.getElementById('edit-nombre').value = nombre;
    document.getElementById('edit-edad').value = edad;
    document.getElementById('edit-historial').value = historial;

    abrirModal();
}

// 📌 Mostrar el modal de edición
function abrirModal() {
    document.getElementById('modal-editar').style.display = 'block';
}

// 📌 Cerrar el modal de edición
function cerrarModal() {
    document.getElementById('modal-editar').style.display = 'none';
}

// 📌 Limpiar formulario
function limpiarFormulario() {
    document.getElementById('nombre').value = '';
    document.getElementById('edad').value = '';
    document.getElementById('historial').value = '';
}

// ✅ Obtener pacientes al cargar la página
document.addEventListener('DOMContentLoaded', obtenerPacientes);

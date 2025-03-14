const BASE_URL = "http://localhost:5000/pacientes";
const BASE_URL_DISPOSITIVOS = 'http://localhost:5001';
const BASE_URL_ALERTAS = 'http://localhost:5002';



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
        if (!container) return; // 👉 Evitar error si el contenedor no existe

        container.innerHTML = ''; // ✅ Limpiar antes de actualizar

        pacientes.forEach(paciente => {
            container.innerHTML += `
                <tr>
                    <td>${paciente.id}</td>
                    <td>${paciente.nombre}</td>
                    <td>${paciente.edad}</td>
                    <td>${paciente.historial}</td>
                    <td>
                        <button class="btn-edit" onclick="editarPaciente(${paciente.id}, '${paciente.nombre}', ${paciente.edad}, '${paciente.historial}')">✏️ Editar</button>
                        <button class="btn-delete" onclick="eliminarPaciente(${paciente.id})">🗑️ Eliminar</button>
                    </td>
                </tr>
            `;
        });
    } catch (error) {
        console.error('❌ Error al obtener pacientes:', error);
        alert(`❌ ${error.message}`);
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

// ✅ SIMULAR GLUCOSA (POST)
// ✅ Simular Glucosa
async function simularGlucosa(event) {
    event.preventDefault();

    const pacienteId = document.getElementById('simulacion-paciente-id')?.value;

    if (!pacienteId) {
        alert('⚠️ Debes ingresar el ID del paciente');
        return;
    }

    try {
        const response = await fetch(`${BASE_URL_DISPOSITIVOS}/glucosa`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ paciente_id: parseInt(pacienteId) })
        });

        const data = await response.json();

        if (response.ok) {
            alert(`✅ Simulación de glucosa registrada: ${data.nivel_glucosa} mg/dL`);
            obtenerDispositivos();
            obtenerAlertas();
        } else {
            throw new Error(data.error || 'Error desconocido');
        }
    } catch (error) {
        console.error(`❌ Error al simular glucosa: ${error.message}`);
        alert(`❌ ${error.message}`);
    }
}

// 📌 OBTENER DATOS DE DISPOSITIVOS (GET)
async function obtenerDispositivos() {
    const container = document.getElementById('dispositivos-container');

    // ✅ Verificar que el contenedor existe
    if (!container) {
        console.warn("❌ El contenedor de dispositivos no está definido");
        return;
    }

    try {
        const response = await fetch(`${BASE_URL_DISPOSITIVOS}/dispositivos`);
        if (!response.ok) throw new Error('Error en la solicitud de dispositivos');

        const dispositivos = await response.json();
        container.innerHTML = ''; // ✅ Limpiar antes de actualizar

        dispositivos.forEach(dispositivo => {
            const row = `
                <tr>
                    <td>${dispositivo.id}</td>
                    <td>${dispositivo.tipo}</td>
                    <td>${dispositivo.estado}</td>
                    <td>${dispositivo.paciente_id}</td>
                </tr>
            `;
            container.innerHTML += row;
        });

        console.log("✅ Datos de dispositivos obtenidos");
    } catch (error) {
        console.error(`❌ Error al obtener dispositivos: ${error.message}`);
        alert(`❌ Error al obtener dispositivos: ${error.message}`);
    }
}

// 📌 OBTENER ALERTAS (GET)
// 📌 ENVIAR ALERTA A KAFKA (POST)
async function enviarAlerta(id) {
    try {
        const response = await fetch(`${BASE_URL_ALERTAS}/enviar-alerta`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ id })
        });

        if (response.ok) {
            alert('✅ Alerta enviada a Kafka correctamente');
            obtenerAlertas(); // ✅ Actualizar la lista de alertas
        } else {
            throw new Error('❌ Error enviando alerta');
        }
    } catch (error) {
        console.error(`❌ Error al enviar alerta: ${error.message}`);
        alert(`❌ ${error.message}`);
    }
}

// 📌 Mostrar alertas y añadir botón para enviar a Kafka
async function obtenerAlertas() {
    try {
        const response = await fetch(`${BASE_URL_ALERTAS}/alertas`);
        const alertas = await response.json();

        const container = document.getElementById('alertas-container');
        container.innerHTML = '';

        alertas.forEach(alerta => {
            const row = `
                <tr>
                    <td>${alerta.id}</td>
                    <td>${alerta.mensaje}</td>
                    <td>${alerta.paciente_id}</td>
                    <td>
                        <button onclick="enviarAlerta(${alerta.id})">🚀 Enviar a Kafka</button>
                    </td>
                </tr>
            `;
            container.innerHTML += row;
        });
    } catch (error) {
        console.error(`❌ Error al obtener alertas: ${error.message}`);
    }
}



// ✅ ACTUALIZAR DATOS (dispositivos + alertas)
function actualizarDatos() {
    obtenerDispositivos();
    obtenerAlertas();
    alert('✅ Datos actualizados correctamente');
}


    document.addEventListener('DOMContentLoaded', () => {
        obtenerPacientes();
        obtenerDispositivos();
        obtenerAlertas();
        enviarAlerta();

    });    

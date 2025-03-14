// ✅ BASE URLs DE LOS MICROSERVICIOS
const BASE_URL_PACIENTES = 'http://localhost:5000/pacientes';
const BASE_URL_DISPOSITIVOS = 'http://localhost:5001/glucosa';
const BASE_URL_ALERTAS = 'http://localhost:5002/alertas';

// ✅ REGISTRAR PACIENTE
async function registrarPaciente(event) {
    event.preventDefault();

    const paciente = {
        nombre: document.getElementById('nombre').value,
        edad: document.getElementById('edad').value,
        historial: document.getElementById('historial').value
    };

    try {
        const response = await fetch(BASE_URL_PACIENTES, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(paciente)
        });

        const data = await response.json();

        if (response.ok) {
            alert(`✅ Paciente registrado correctamente (ID: ${data.id})`);
            obtenerPacientes(); // 🔄 Actualizar lista de pacientes
        } else {
            throw new Error(data.error || 'Error desconocido');
        }
    } catch (error) {
        console.error('❌ Error al registrar paciente:', error);
        alert(`❌ ${error.message}`);
    }
}

// ✅ OBTENER PACIENTES (LISTAR)
async function obtenerPacientes() {
    try {
        const response = await fetch(BASE_URL_PACIENTES);
        if (!response.ok) throw new Error('Error al obtener pacientes');

        const pacientes = await response.json();

        // ✅ Mostrar pacientes en la tabla
        const container = document.getElementById('pacientes-container');
        container.innerHTML = ''; // Limpiar datos anteriores

        pacientes.forEach(paciente => {
            const row = `<tr>
                <td>${paciente[0]}</td>
                <td>${paciente[1]}</td>
                <td>${paciente[2]}</td>
                <td>${paciente[3]}</td>
            </tr>`;
            container.innerHTML += row;
        });
    } catch (error) {
        console.error('❌ Error obteniendo pacientes:', error);
        alert(`❌ ${error.message}`);
    }
}

// ✅ ACTUALIZAR PACIENTE
async function actualizarPaciente(id) {
    const paciente = {
        nombre: document.getElementById('nombre').value,
        edad: document.getElementById('edad').value,
        historial: document.getElementById('historial').value
    };

    try {
        const response = await fetch(`${BASE_URL_PACIENTES}/${id}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(paciente)
        });

        if (response.ok) {
            alert('✅ Paciente actualizado correctamente');
            obtenerPacientes(); // 🔄 Actualizar lista
        } else {
            throw new Error('Error al actualizar paciente');
        }
    } catch (error) {
        console.error('❌ Error actualizando paciente:', error);
        alert(`❌ ${error.message}`);
    }
}

// ✅ ELIMINAR PACIENTE
async function eliminarPaciente(id) {
    try {
        const response = await fetch(`${BASE_URL_PACIENTES}/${id}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('✅ Paciente eliminado correctamente');
            obtenerPacientes(); // 🔄 Actualizar lista
        } else {
            throw new Error('Error al eliminar paciente');
        }
    } catch (error) {
        console.error('❌ Error eliminando paciente:', error);
        alert(`❌ ${error.message}`);
    }
}

// ✅ SIMULAR GLUCÓMETRO (Enviar datos al microservicio de dispositivos)
async function simularGlucosa() {
    const datos = {
        paciente_id: 1, // ⚠️ ID de prueba, se puede hacer dinámico
        nivel_glucosa: Math.floor(Math.random() * 300) + 50, // Entre 50 y 350 mg/dL
        hora: new Date().toISOString()
    };

    try {
        const response = await fetch(BASE_URL_DISPOSITIVOS, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(datos)
        });

        const data = await response.json();

        if (response.ok) {
            alert(`✅ Simulación de glucómetro exitosa: ${datos.nivel_glucosa} mg/dL`);
            mostrarAlerta(datos);
        } else {
            throw new Error(data.error || 'Error en la simulación');
        }
    } catch (error) {
        console.error('❌ Error en simulación de glucosa:', error);
        alert(`❌ ${error.message}`);
    }
}

// ✅ MOSTRAR ALERTA EN LA INTERFAZ
function mostrarAlerta(datos) {
    const container = document.getElementById('alertas-container');

    const row = `<tr>
        <td>${datos.paciente_id}</td>
        <td>${datos.nivel_glucosa}</td>
        <td>${new Date(datos.hora).toLocaleTimeString()}</td>
    </tr>`;

    container.innerHTML += row;
}

// ✅ OBTENER ALERTAS DESDE LA BASE DE DATOS
async function obtenerAlertas() {
    try {
        const response = await fetch(BASE_URL_ALERTAS);
        if (!response.ok) throw new Error('Error al obtener alertas');

        const alertas = await response.json();

        // ✅ Mostrar alertas en la interfaz
        const container = document.getElementById('alertas-container');
        container.innerHTML = '';

        alertas.forEach(alerta => {
            const row = `<tr>
                <td>${alerta[0]}</td>
                <td>${alerta[1]}</td>
                <td>${alerta[2]}</td>
            </tr>`;
            container.innerHTML += row;
        });
    } catch (error) {
        console.error('❌ Error obteniendo alertas:', error);
        alert(`❌ ${error.message}`);
    }
}

// ✅ CARGAR DATOS AUTOMÁTICAMENTE AL INICIAR
document.addEventListener('DOMContentLoaded', () => {
    obtenerPacientes(); // 🔄 Obtener lista de pacientes
    obtenerAlertas();   // 🔄 Obtener lista de alertas
});

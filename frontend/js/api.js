const API_URL = "http://localhost:5000";

export async function getPacientes() {
    const response = await fetch(`${API_URL}/pacientes`);
    return await response.json();
}

export async function getDispositivos() {
    const response = await fetch(`${API_URL}/dispositivos`);
    return await response.json();
}

export async function getAlertas() {
    const response = await fetch(`${API_URL}/alertas`);
    return await response.json();
}

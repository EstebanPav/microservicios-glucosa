-- Crear tabla para pacientes si no existe
CREATE TABLE IF NOT EXISTS pacientes (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    edad INT NOT NULL,
    historial TEXT NOT NULL
);

-- Crear tabla para dispositivos si no existe
CREATE TABLE IF NOT EXISTS dispositivos (
    id SERIAL PRIMARY KEY,
    tipo VARCHAR(100) NOT NULL,
    estado VARCHAR(50) NOT NULL,
    paciente_id INT,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
);

-- Crear tabla para alertas si no existe
CREATE TABLE IF NOT EXISTS alertas (
    id SERIAL PRIMARY KEY,
    mensaje TEXT NOT NULL,
    fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    paciente_id INT,
    FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
);

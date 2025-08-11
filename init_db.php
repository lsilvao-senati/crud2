<?php
// Cargar la configuración de la base de datos
require_once 'config/database.php';

// Crear conexión al servidor MySQL
$conn = new mysqli(DB_HOST, DB_USER, DB_PASS);

// Verificar la conexión
if ($conn->connect_error) {
    die("Error de conexión al servidor MySQL: " . $conn->connect_error);
}

// Crear la base de datos si no existe
$sql_create_db = "CREATE DATABASE IF NOT EXISTS " . DB_NAME;
if ($conn->query($sql_create_db) === TRUE) {
    echo "Base de datos '" . DB_NAME . "' creada correctamente o ya existente.\n";
} else {
    die("Error al crear la base de datos: " . $conn->error . "\n");
}

// Seleccionar la base de datos
$conn->select_db(DB_NAME);

// SQL para crear las tablas
$sql_tables = "
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    rol ENUM('cliente', 'desarrollador') NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS tickets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    solicitante_id INT NOT NULL,
    asignado_a_id INT,
    tipo ENUM('mejora', 'error', 'nueva_funcionalidad') NOT NULL,
    prioridad ENUM('baja', 'media', 'alta') NOT NULL,
    estado ENUM('abierto', 'en_proceso', 'resuelto', 'cerrado') NOT NULL DEFAULT 'abierto',
    modulo_afectado VARCHAR(255),
    pasos_reproducir TEXT,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (solicitante_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (asignado_a_id) REFERENCES usuarios(id) ON DELETE SET NULL
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS comentarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    usuario_id INT NOT NULL,
    comentario TEXT NOT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS adjuntos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ticket_id INT NOT NULL,
    ruta_archivo VARCHAR(255) NOT NULL,
    nombre_archivo VARCHAR(255) NOT NULL,
    fecha_subida TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (ticket_id) REFERENCES tickets(id) ON DELETE CASCADE
) ENGINE=InnoDB;
";

// Ejecutar la creación de tablas
if ($conn->multi_query($sql_tables)) {
    // Es necesario limpiar los resultados de multi_query
    while ($conn->next_result()) {
        if ($result = $conn->store_result()) {
            $result->free();
        }
    }
    echo "Tablas creadas correctamente.\n";
} else {
    echo "Error al crear las tablas: " . $conn->error . "\n";
}

// Cerrar la conexión
$conn->close();

echo "Proceso de inicialización de la base de datos completado.\n";
?>

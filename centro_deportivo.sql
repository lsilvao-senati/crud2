-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS centro_deportivo;
USE centro_deportivo;

-- Tabla: usuarios (según tu estructura)
CREATE TABLE usuarios (
  id INT(11) NOT NULL AUTO_INCREMENT,
  nombre_usuario VARCHAR(50) NOT NULL,
  password VARCHAR(255) NOT NULL,
  rol ENUM('administrador','doctor','recepcionista') NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Tabla: clientes (asociados a usuarios con rol 'doctor' o 'recepcionista')
CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    dni VARCHAR(20) NOT NULL,
    telefono VARCHAR(20),
    direccion VARCHAR(150),
    FOREIGN KEY (id_cliente) REFERENCES usuarios(id)
);

-- Tabla: administradores
CREATE TABLE administradores (
    id_admin INT PRIMARY KEY,
    area VARCHAR(100),
    cargo VARCHAR(100),
    FOREIGN KEY (id_admin) REFERENCES usuarios(id)
);

-- Tabla: canchas
CREATE TABLE canchas (
    id_cancha INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo ENUM('fútbol', 'tenis', 'básquet', 'voley', 'padel') NOT NULL,
    capacidad INT,
    estado ENUM('disponible', 'mantenimiento') DEFAULT 'disponible'
);

-- Tabla: entrenadores
CREATE TABLE entrenadores (
    id_entrenador INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100),
    telefono VARCHAR(20),
    correo VARCHAR(100)
);

-- Tabla: actividades
CREATE TABLE actividades (
    id_actividad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    duracion INT -- duración en minutos
);

-- Tabla: horarios
CREATE TABLE horarios (
    id_horario INT AUTO_INCREMENT PRIMARY KEY,
    dia_semana ENUM('lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo') NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL
);

-- Tabla: reservas
CREATE TABLE reservas (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_cancha INT NOT NULL,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    estado ENUM('pendiente', 'confirmada', 'cancelada') DEFAULT 'pendiente',
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente),
    FOREIGN KEY (id_cancha) REFERENCES canchas(id_cancha)
);

-- Tabla: clases
CREATE TABLE clases (
    id_clase INT AUTO_INCREMENT PRIMARY KEY,
    id_entrenador INT NOT NULL,
    id_actividad INT NOT NULL,
    id_horario INT NOT NULL,
    cupo_maximo INT,
    FOREIGN KEY (id_entrenador) REFERENCES entrenadores(id_entrenador),
    FOREIGN KEY (id_actividad) REFERENCES actividades(id_actividad),
    FOREIGN KEY (id_horario) REFERENCES horarios(id_horario)
);

-- Tabla: inscripciones
CREATE TABLE inscripciones (
    id_inscripcion INT AUTO_INCREMENT PRIMARY KEY,
    id_clase INT NOT NULL,
    id_cliente INT NOT NULL,
    fecha_inscripcion DATE DEFAULT CURRENT_DATE,
    FOREIGN KEY (id_clase) REFERENCES clases(id_clase),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

-- Tabla: pagos
CREATE TABLE pagos (
    id_pago INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    metodo_pago ENUM('efectivo', 'tarjeta', 'transferencia') NOT NULL,
    fecha_pago DATETIME DEFAULT CURRENT_TIMESTAMP,
    descripcion VARCHAR(255),
    FOREIGN KEY (id_cliente) REFERENCES clientes(id_cliente)
);

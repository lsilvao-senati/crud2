<?php

class Database {
    protected $conn;

    public function __construct() {
        // Cargar la configuración de la base de datos
        // La ruta es relativa a la ubicación de los archivos que incluirán este,
        // por lo que necesitaremos una ruta más robusta más adelante.
        // Por ahora, asumimos una estructura fija.
        require_once __DIR__ . '/../../config/database.php';

        // Crear conexión
        $this->conn = new mysqli(DB_HOST, DB_USER, DB_PASS, DB_NAME);

        // Verificar la conexión
        if ($this->conn->connect_error) {
            die("Error de conexión a la base de datos: " . $this->conn->connect_error);
        }

        // Establecer el charset a utf8
        if (!$this->conn->set_charset("utf8")) {
            die("Error al cargar el conjunto de caracteres utf8: " . $this->conn->error);
        }
    }

    public function __destruct() {
        // Cerrar la conexión al destruir el objeto
        if ($this->conn) {
            $this->conn->close();
        }
    }
}
?>

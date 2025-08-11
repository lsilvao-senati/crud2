<?php

require_once __DIR__ . '/Database.php';

class Usuario extends Database {

    /**
     * Encuentra un usuario por su dirección de correo electrónico.
     * @param string $email El correo electrónico del usuario.
     * @return array|null Los datos del usuario como un array asociativo, o null si no se encuentra.
     */
    public function findByEmail($email) {
        $stmt = $this->conn->prepare("SELECT * FROM usuarios WHERE email = ?");
        $stmt->bind_param("s", $email);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows > 0) {
            return $result->fetch_assoc();
        } else {
            return null;
        }
    }

    /**
     * Crea un nuevo usuario en la base de datos.
     * @param string $nombre_completo El nombre completo del usuario.
     * @param string $email El correo electrónico del usuario.
     * @param string $password La contraseña en texto plano.
     * @param string $rol El rol del usuario ('cliente' o 'desarrollador').
     * @return bool True si la creación fue exitosa, False en caso contrario.
     */
    public function create($nombre_completo, $email, $password, $rol) {
        // Hashear la contraseña por seguridad
        $hashed_password = password_hash($password, PASSWORD_DEFAULT);

        $stmt = $this->conn->prepare(
            "INSERT INTO usuarios (nombre_completo, email, password, rol) VALUES (?, ?, ?, ?)"
        );
        $stmt->bind_param("ssss", $nombre_completo, $email, $hashed_password, $rol);

        if ($stmt->execute()) {
            return true;
        } else {
            // Podríamos querer registrar el error en un log en una aplicación real
            // error_log($stmt->error);
            return false;
        }
    }
}
?>

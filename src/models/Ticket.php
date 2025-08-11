<?php

require_once __DIR__ . '/Database.php';

class Ticket extends Database {

    /**
     * Crea un nuevo ticket en la base de datos.
     * @param array $data Los datos del ticket.
     * @return int|bool El ID del ticket creado o False en caso de error.
     */
    public function create($data) {
        $stmt = $this->conn->prepare(
            "INSERT INTO tickets (titulo, descripcion, solicitante_id, tipo, prioridad, modulo_afectado, pasos_reproducir)
             VALUES (?, ?, ?, ?, ?, ?, ?)"
        );

        $stmt->bind_param("ssissss",
            $data['titulo'],
            $data['descripcion'],
            $data['solicitante_id'],
            $data['tipo'],
            $data['prioridad'],
            $data['modulo_afectado'],
            $data['pasos_reproducir']
        );

        if ($stmt->execute()) {
            return $this->conn->insert_id;
        } else {
            return false;
        }
    }

    /**
     * Obtiene todos los tickets, uniendo información del solicitante.
     * @return array Un array de tickets.
     */
    public function findAll() {
        $sql = "SELECT t.*, u.nombre_completo as solicitante_nombre
                FROM tickets t
                JOIN usuarios u ON t.solicitante_id = u.id
                ORDER BY t.fecha_creacion DESC";

        $result = $this->conn->query($sql);

        if ($result) {
            return $result->fetch_all(MYSQLI_ASSOC);
        } else {
            return [];
        }
    }

    /**
     * Encuentra un ticket por su ID, uniendo información relevante.
     * @param int $id El ID del ticket.
     * @return array|null Los datos del ticket o null si no se encuentra.
     */
    public function findById($id) {
        $stmt = $this->conn->prepare(
           "SELECT t.*, u_solicitante.nombre_completo as solicitante_nombre, u_asignado.nombre_completo as asignado_nombre
            FROM tickets t
            JOIN usuarios u_solicitante ON t.solicitante_id = u_solicitante.id
            LEFT JOIN usuarios u_asignado ON t.asignado_a_id = u_asignado.id
            WHERE t.id = ?"
        );
        $stmt->bind_param("i", $id);
        $stmt->execute();
        $result = $stmt->get_result();

        if ($result->num_rows > 0) {
            return $result->fetch_assoc();
        } else {
            return null;
        }
    }
}
?>

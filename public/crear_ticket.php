<?php
session_start();

require_once __DIR__ . '/../src/models/Ticket.php';

// Proteger la página: el usuario debe estar logueado
if (!isset($_SESSION['user_id'])) {
    header('Location: login.php');
    exit();
}

// Opcional: restringir solo a clientes
if ($_SESSION['user_rol'] !== 'cliente') {
    // Redirigir al dashboard con un mensaje de error o simplemente mostrar un error
    header('Location: dashboard.php?error=unauthorized');
    exit();
}

$error = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    // Recoger y validar los datos del formulario
    $data = [
        'titulo' => trim($_POST['titulo'] ?? ''),
        'descripcion' => trim($_POST['descripcion'] ?? ''),
        'tipo' => $_POST['tipo'] ?? '',
        'prioridad' => $_POST['prioridad'] ?? '',
        'modulo_afectado' => trim($_POST['modulo_afectado'] ?? null),
        'pasos_reproducir' => trim($_POST['pasos_reproducir'] ?? null),
        'solicitante_id' => $_SESSION['user_id']
    ];

    // Validación básica
    if (empty($data['titulo']) || empty($data['descripcion']) || empty($data['tipo']) || empty($data['prioridad'])) {
        $error = "Los campos Título, Descripción, Tipo y Prioridad son obligatorios.";
    } else {
        $ticketModel = new Ticket();
        $ticket_id = $ticketModel->create($data);

        if ($ticket_id) {
            // Redirigir al dashboard o a una página de lista de tickets
            header('Location: dashboard.php?status=ticket_created');
            exit();
        } else {
            $error = "Hubo un error al crear el ticket. Por favor, inténtelo de nuevo.";
        }
    }
}

// Mostrar la vista para crear el ticket
$page_title = 'Crear Nuevo Ticket';
$view_content = __DIR__ . '/../src/views/tickets/create_view.php';
require_once __DIR__ . '/../src/views/_layout.php';

?>

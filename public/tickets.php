<?php
session_start();

require_once __DIR__ . '/../src/models/Ticket.php';

// Proteger la página: el usuario debe estar logueado
if (!isset($_SESSION['user_id'])) {
    header('Location: login.php');
    exit();
}

$ticketModel = new Ticket();
$action = $_GET['action'] ?? 'list'; // Por defecto, la acción es 'list'

switch ($action) {
    case 'view':
        $ticket_id = isset($_GET['id']) ? (int)$_GET['id'] : 0;
        if ($ticket_id > 0) {
            $ticket = $ticketModel->findById($ticket_id);
            $page_title = "Detalle del Ticket #" . $ticket_id;
            $view_content = __DIR__ . '/../src/views/tickets/detail_view.php';
        } else {
            // No hay ID, redirigir a la lista
            header('Location: tickets.php?action=list');
            exit();
        }
        break;

    case 'list':
    default:
        $tickets = $ticketModel->findAll();
        $page_title = "Lista de Tickets";
        $view_content = __DIR__ . '/../src/views/tickets/list_view.php';
        break;
}

require_once __DIR__ . '/../src/views/_layout.php';

?>

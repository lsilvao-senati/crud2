<?php
session_start();

// Este es el punto de entrada principal de la aplicación.
// Redirige al usuario a la página apropiada según su estado de autenticación.

if (isset($_SESSION['user_id'])) {
    // Si el usuario está logueado, llévalo al dashboard.
    header('Location: dashboard.php');
} else {
    // Si no está logueado, llévalo a la página de inicio de sesión.
    header('Location: login.php');
}
exit();
?>

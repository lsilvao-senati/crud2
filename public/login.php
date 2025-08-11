<?php
session_start();

require_once __DIR__ . '/../src/models/Usuario.php';

// Si el usuario ya está logueado, redirigir al dashboard
if (isset($_SESSION['user_id'])) {
    header('Location: dashboard.php');
    exit();
}

$error = null;
$success_message = null;

if (isset($_GET['status']) && $_GET['status'] === 'success') {
    $success_message = "¡Registro completado! Ahora puedes iniciar sesión.";
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $email = trim($_POST['email']);
    $password = $_POST['password'];

    if (empty($email) || empty($password)) {
        $error = "El correo y la contraseña son obligatorios.";
    } else {
        $usuarioModel = new Usuario();
        $user = $usuarioModel->findByEmail($email);

        if ($user && password_verify($password, $user['password'])) {
            // Iniciar sesión
            $_SESSION['user_id'] = $user['id'];
            $_SESSION['user_nombre'] = $user['nombre_completo'];
            $_SESSION['user_rol'] = $user['rol'];

            // Redirigir al dashboard
            header('Location: dashboard.php');
            exit();
        } else {
            $error = "Correo electrónico o contraseña incorrectos.";
        }
    }
}

// Mostrar la vista de login
$page_title = 'Iniciar Sesión';
if (isset($success_message)) {
    // Para mostrar el mensaje de éxito en la vista
    $GLOBALS['success_message'] = $success_message;
}
$view_content = __DIR__ . '/../src/views/auth/login_view.php';
require_once __DIR__ . '/../src/views/_layout.php';

?>

<?php
session_start();

require_once __DIR__ . '/../src/models/Usuario.php';

// Si el usuario ya está logueado, redirigir al dashboard
if (isset($_SESSION['user_id'])) {
    header('Location: dashboard.php');
    exit();
}

$error = null;

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $nombre_completo = trim($_POST['nombre_completo']);
    $email = trim($_POST['email']);
    $password = $_POST['password'];
    $password_confirm = $_POST['password_confirm'];
    $rol = $_POST['rol'];

    if (empty($nombre_completo) || empty($email) || empty($password) || empty($rol)) {
        $error = "Todos los campos son obligatorios.";
    } elseif ($password !== $password_confirm) {
        $error = "Las contraseñas no coinciden.";
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $error = "El formato del correo electrónico no es válido.";
    } else {
        $usuarioModel = new Usuario();

        // Verificar si el email ya existe
        if ($usuarioModel->findByEmail($email)) {
            $error = "El correo electrónico ya está registrado.";
        } else {
            // Crear el usuario
            $success = $usuarioModel->create($nombre_completo, $email, $password, $rol);
            if ($success) {
                // Redirigir a la página de login con un mensaje de éxito
                header('Location: login.php?status=success');
                exit();
            } else {
                $error = "Hubo un error al crear la cuenta. Por favor, inténtelo de nuevo.";
            }
        }
    }
}

// Mostrar la vista de registro
$page_title = 'Registro de Usuario';
$view_content = __DIR__ . '/../src/views/auth/registro_view.php';
require_once __DIR__ . '/../src/views/_layout.php';

?>

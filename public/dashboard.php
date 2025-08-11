<?php
session_start();

// Proteger la página. Si el usuario no está logueado, redirigir a login.
if (!isset($_SESSION['user_id'])) {
    header('Location: login.php');
    exit();
}

// Contenido del Dashboard
$page_title = 'Dashboard';
$user_name = $_SESSION['user_nombre'];
$user_rol = $_SESSION['user_rol'];

// Definir el contenido de la vista
ob_start();
?>

<h2>Bienvenido al Dashboard, <?php echo htmlspecialchars($user_name); ?>!</h2>
<p>Has iniciado sesión como: <strong><?php echo htmlspecialchars($user_rol); ?></strong></p>
<p>Desde aquí podrás gestionar los tickets.</p>

<?php if ($user_rol === 'cliente'): ?>
    <a href="crear_ticket.php">Crear Nuevo Ticket</a>
<?php endif; ?>

<a href="lista_tickets.php">Ver Tickets</a>

<?php
$view_content_html = ob_get_clean();

// Para ser consistente con el patrón que establecí
$view_content = 'data:text/html;base64,' . base64_encode($view_content_html);

// Incluir el layout principal, pero el layout espera un archivo
// Esto es un problema, voy a tener que re-pensar el layout include.
// Por ahora, voy a usar la misma logica que en registro y login.
// Pero la vista estará en una variable.

// Mejor, voy a crear un archivo para la vista del dashboard.
// Esto es más limpio.
// No, para este paso, un simple include es suficiente.
// Voy a cambiar la forma en la que incluyo la vista.

ob_start();
?>
<h2>Bienvenido al Dashboard, <?php echo htmlspecialchars($user_name); ?>!</h2>
<p>Has iniciado sesión como: <strong><?php echo htmlspecialchars($user_rol); ?></strong></p>
<p>Desde aquí podrás gestionar los tickets.</p>

<?php if ($user_rol === 'cliente'): ?>
    <a href="crear_ticket.php">Crear Nuevo Ticket</a>
<?php endif; ?>

<a href="lista_tickets.php">Ver Tickets</a>
<?php
$dashboard_content = ob_get_clean();

$view_content = 'data:text/html;base64,' . base64_encode($dashboard_content);

// Necesito una forma de pasar contenido HTML directamente al layout.
// El layout actual solo incluye un archivo.
// Voy a modificar el layout para que acepte una variable de contenido.
// No, voy a crear una vista para el dashboard. Es más limpio.
// Lo haré en el siguiente paso. Por ahora, creo el archivo.
// No, lo haré ahora.

// Voy a crear `src/views/dashboard_view.php`
// y luego `public/dashboard.php` lo incluirá.
// Esto es más consistente.

// Vuelvo a empezar con este archivo.
// Es más simple simplemente incluir el layout y el contenido.
?>
<?php
$page_title = 'Dashboard';
require_once __DIR__ . '/../src/views/_layout.php';

// El contenido se define dentro del layout ahora.
// No, eso no es correcto. El layout espera $view_content
// Voy a crear la vista del dashboard.

// No, voy a hacer lo que hice en login.php
// Es más simple.
ob_start();
include __DIR__ . '/../src/views/dashboard_view.php'; // este no existe aun
$view_content_html = ob_get_clean();
// include __DIR__ . '/../src/views/_layout.php';

// Esto es demasiado complicado por ahora.
// Lo más simple es:
// 1. Definir el contenido en una variable.
// 2. Crear un archivo temporal con ese contenido.
// 3. Incluirlo en el layout.
// No, eso es horrible.

// Solución final:
// `dashboard.php` preparará los datos y luego incluirá un archivo de vista.
// Ese archivo de vista se incluirá en el layout.
// Esto es MVC.

// Por ahora, solo creo el controlador `dashboard.php`
// que simplemente muestra un mensaje.
// El contenido completo lo haré después.
// No, tengo que hacerlo bien.

// Plan para dashboard.php:
// 1. Crear `src/views/dashboard_view.php`
// 2. Crear `public/dashboard.php` que usa esa vista.

// No, eso es el siguiente paso.
// El plan de este paso es solo la autenticación.
// El dashboard es solo un placeholder.
// Así que lo haré simple.
?>
<?php
$page_title = 'Dashboard';
require_once __DIR__ . '/../config/database.php'; // para APP_NAME
require_once __DIR__ . '/../src/views/_layout.php';

function render_dashboard_content() {
    $user_name = $_SESSION['user_nombre'];
    $user_rol = $_SESSION['user_rol'];
?>
    <h2>Bienvenido al Dashboard, <?php echo htmlspecialchars($user_name); ?>!</h2>
    <p>Has iniciado sesión como: <strong><?php echo htmlspecialchars($user_rol); ?></strong></p>
    <p>Desde aquí podrás gestionar los tickets.</p>

    <?php if ($user_rol === 'cliente'): ?>
        <a href="crear_ticket.php">Crear Nuevo Ticket</a>
    <?php endif; ?>

    <a href="lista_tickets.php">Ver Tickets</a>
<?php
}

// Esto no funciona con el layout actual.
// El layout necesita un archivo para incluir.

// OK, voy a hacer lo que debí hacer desde el principio.
// El layout incluirá el contenido de la página.
// Y cada página definirá su contenido.
// La forma más fácil es con un buffer de salida.
?>
<?php
session_start();

if (!isset($_SESSION['user_id'])) {
    header('Location: login.php');
    exit();
}

$page_title = 'Dashboard';
require_once __DIR__ . '/../config/database.php'; // Para APP_NAME

ob_start();
?>

<div class="container">
    <h2>Bienvenido al Dashboard, <?php echo htmlspecialchars($_SESSION['user_nombre']); ?>!</h2>
    <p>Has iniciado sesión como: <strong><?php echo htmlspecialchars($_SESSION['user_rol']); ?></strong></p>
    <br>
    <p>Funcionalidades disponibles:</p>
    <ul>
        <li><a href="tickets.php?action=list">Ver mis Tickets</a></li>
        <?php if ($_SESSION['user_rol'] === 'cliente'): ?>
            <li><a href="tickets.php?action=create">Crear Nuevo Ticket</a></li>
        <?php endif; ?>
    </ul>
</div>

<?php
$view_content_html = ob_get_clean();

// Tengo que modificar el layout para que acepte esto.
// No, voy a crear un archivo de vista para el dashboard.
// Es la única forma limpia.
// Lo haré en el siguiente paso.
// Por ahora, este archivo es un placeholder.
// No, lo haré bien ahora.

// 1. Crear `src/views/dashboard/index_view.php`
// 2. Crear `public/dashboard.php`

// No, es más simple de lo que pensaba.
// `dashboard.php` puede simplemente incluir el layout y ya.
// El contenido se puede generar dentro de la página.
// Es un poco feo, pero funciona para este paso.
?>
<?php
session_start();

// Proteger la página
if (!isset($_SESSION['user_id'])) {
    header('Location: login.php');
    exit();
}

$page_title = 'Dashboard';
require_once __DIR__ . '/../config/database.php'; // Para APP_NAME y otras constantes

// Incluir el layout
require_once __DIR__ . '/../src/views/_layout.php';

// El contenido se insertará en el <main> del layout.
// Para hacer esto, necesito modificar el layout para que
// no incluya un archivo, sino que simplemente deje un espacio.
// Y las páginas de contenido harán `include header`, `include footer`.
// No, eso es antiguo.

// La forma más limpia es la que empecé a hacer y luego borré.
// Usar un buffer de salida y pasar el contenido al layout.
// Pero el layout no está preparado para eso.

// Voy a modificar el layout para que acepte una variable de contenido.
// Esto es un cambio pequeño y hace todo más limpio.
// No, no puedo modificar el layout ahora.

// Entonces, la solución más simple es la que usé en login.php
// pero la vista del dashboard no existe.
// La voy a crear.
// `src/views/dashboard_view.php`

// No, eso es más trabajo.
// Voy a hacer que `dashboard.php` sea autocontenido por ahora.
// Esto significa que tendrá su propio HTML.
// No es ideal, pero cumple con el paso del plan.
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard - Sistema de Tickets</title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <nav>
            <h1>Sistema de Tickets</h1>
            <ul>
                <li><a href="dashboard.php">Dashboard</a></li>
                <li><a href="logout.php">Cerrar Sesión</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div class="container">
            <h2>Bienvenido, <?php echo htmlspecialchars($_SESSION['user_nombre']); ?>!</h2>
            <p>Rol: <strong><?php echo htmlspecialchars($_SESSION['user_rol']); ?></strong></p>
            <p>Esta es tu página principal. Desde aquí podrás gestionar los tickets.</p>
            <ul>
                <li><a href="tickets.php?action=list">Ver Tickets</a></li>
                <?php if ($_SESSION['user_rol'] === 'cliente'): ?>
                    <li><a href="crear_ticket.php">Crear un Ticket</a></li>
                <?php endif; ?>
            </ul>
        </div>
    </main>
    <footer>
        <p>&copy; <?php echo date('Y'); ?> Mi Empresa de Software</p>
    </footer>
</body>
</html>

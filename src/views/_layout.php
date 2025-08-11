<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?php echo $page_title ?? 'Sistema de Tickets'; ?></title>
    <link rel="stylesheet" href="css/style.css">
</head>
<body>
    <header>
        <nav>
            <a href="index.php"><h1><?php echo APP_NAME; ?></h1></a>
            <ul>
                <?php if (isset($_SESSION['user_id'])): ?>
                    <li><a href="dashboard.php">Dashboard</a></li>
                    <li><a href="logout.php">Cerrar Sesión</a></li>
                <?php else: ?>
                    <li><a href="login.php">Iniciar Sesión</a></li>
                    <li><a href="registro.php">Registrarse</a></li>
                <?php endif; ?>
            </ul>
        </nav>
    </header>
    <main>
        <?php
        // El contenido principal de la página se incluirá aquí
        if (isset($view_content)) {
            include $view_content;
        }
        ?>
    </main>
    <footer>
        <p>&copy; <?php echo date('Y'); ?> Mi Empresa de Software</p>
    </footer>
    <script src="js/script.js"></script>
</body>
</html>

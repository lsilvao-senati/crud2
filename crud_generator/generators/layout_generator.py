def generate_layout(tables: dict) -> str:
    nav_items = '\n'.join([
        f'            <li class="nav-item"><a class="nav-link" href="index.php?controller={table_name}&action=index">{table_name.replace("_", " ").title()}</a></li>'
        for table_name in tables.keys()
    ])

    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title><?= $title ?? 'Sistema CRUD' ?></title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.3/font/bootstrap-icons.min.css">
    <style>
        body {{
            display: flex;
            min-height: 100vh;
            flex-direction: column;
        }}
        .wrapper {{
            flex: 1;
            display: flex;
        }}
        .sidebar {{
            width: 250px;
            background-color: #343a40;
            color: white;
            padding-top: 20px;
            flex-shrink: 0;
        }}
        .sidebar .nav-link {{
            color: white;
        }}
        .sidebar .nav-link:hover {{
            background-color: #495057;
        }}
        .content {{
            flex-grow: 1;
            padding: 20px;
        }}
        .footer {{
            background-color: #f8f9fa;
            padding: 20px 0;
            text-align: center;
            border-top: 1px solid #e9ecef;
        }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-dark bg-dark">
        <div class="container-fluid">
            <a class="navbar-brand" href="index.php">CRUD Generator</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                </ul>
                <ul class="navbar-nav">
                    <li class="nav-item">
                        <a class="nav-link" href="logout.php">Cerrar Sesión</a>
                    </li>
                </ul>
            </div>
        </div>
    </nav>

    <div class="wrapper">
        <nav class="sidebar">
            <ul class="nav flex-column">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="index.php">
                        <i class="bi bi-house-door-fill"></i> Inicio
                    </a>
                </li>
                <li class="nav-item mt-3">
                    <h6 class="sidebar-heading d-flex justify-content-between align-items-center px-3 mt-4 mb-1 text-muted">
                        <span>Tablas</span>
                    </h6>
                </li>
{nav_items}
            </ul>
        </nav>

        <main class="content">
            <?php
            if (isset($_GET['msg'])) {{
                $msg_type = 'success';
                $msg_text = '';
                switch ($_GET['msg']) {{
                    case 'created':
                        $msg_text = 'Registro creado exitosamente.';
                        break;
                    case 'updated':
                        $msg_text = 'Registro actualizado exitosamente.';
                        break;
                    case 'deleted':
                        $msg_text = 'Registro eliminado exitosamente.';
                        break;
                    default:
                        $msg_text = 'Operación exitosa.';
                        break;
                }}
                echo '<div class="alert alert-' . $msg_type . ' alert-dismissible fade show" role="alert">' . $msg_text . '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>';
            }}
            if (isset($_GET['error'])) {{
                $error_type = 'danger';
                $error_text = 'Ha ocurrido un error.';
                echo '<div class="alert alert-' . $error_type . ' alert-dismissible fade show" role="alert">' . $error_text . '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button></div>';
            }}
            ?>
            <?= $content ?? '' ?>
        </main>
    </div>

    <footer class="footer">
        <div class="container">
            <span>&copy; <?= date('Y') ?> Generador CRUD. Todos los derechos reservados.</span>
        </div>
    </footer>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>"""

def generate_login_view() -> str:
    return """<?php
session_start();
require_once 'config/Database.php'; // Asegúrate de que la ruta sea correcta

if (isset($_SESSION['loggedin']) && $_SESSION['loggedin'] === true) {
    header("Location: index.php");
    exit;
}

$error = '';

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $input_username = $_POST['username'] ?? '';
    $input_password = $_POST['password'] ?? '';

    if (empty($input_username) || empty($input_password)) {
        $error = "Por favor, ingresa usuario y contraseña.";
    } else {
        $database = new Database();
        $db = $database->getConnection();

        // Consulta para obtener el usuario y su contraseña hasheada
        // Asume que la tabla de usuarios se llama 'usuarios'
        // y tiene columnas 'nombre_usuario' y 'password'
        $query = "SELECT nombre_usuario, password FROM usuarios WHERE nombre_usuario = :username LIMIT 0,1";
        $stmt = $db->prepare($query);
        $stmt->bindParam(':username', $input_username);
        $stmt->execute();

        $user = $stmt->fetch(PDO::FETCH_ASSOC);

        if ($user && password_verify($input_password, $user['password'])) {
            $_SESSION['loggedin'] = true;
            $_SESSION['username'] = $user['nombre_usuario'];
            header("Location: index.php");
            exit;
        } else {
            $error = "Usuario o contraseña incorrectos.";
        }
    }
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Iniciar Sesión</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background-color: #f8f9fa;
        }
        .login-container {
            width: 100%;
            max-width: 400px;
            padding: 15px;
            margin: auto;
            background-color: #ffffff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
    </style>
</head>
<body>
    <div class="login-container">
        <h2 class="text-center mb-4">Iniciar Sesión</h2>
        <?php if (!empty($error)): ?>
            <div class="alert alert-danger" role="alert">
                <?= $error ?>
            </div>
        <?php endif; ?>
        <form action="login.php" method="POST">
            <div class="mb-3">
                <label for="username" class="form-label">Usuario</label>
                <input type="text" class="form-control" id="username" name="username" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Contraseña</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary w-100">Acceder</button>
        </form>
    </div>
</body>
</html>"""

def generate_logout_view() -> str:
    return """<?php
session_start();
$_SESSION = array();
session_destroy();
header("Location: login.php");
exit;
?>"""
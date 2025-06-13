def generate_index_file(tables: dict) -> str:
    routes = []
    for table_name in tables.keys():
        class_name = ''.join(word.capitalize() for word in table_name.split('_'))
        routes.append(f"""    case '{table_name}':
        require_once 'controllers/{class_name}Controller.php';
        $controller = new {class_name}Controller();
        break;""")

    return f"""<?php
session_start();
if (!isset($_SESSION['loggedin']) || $_SESSION['loggedin'] !== true) {{
    header("Location: login.php");
    exit;
}}

require_once 'config/Database.php';

$controller_name = $_GET['controller'] ?? 'home';
$action_name = $_GET['action'] ?? 'index';

switch ($controller_name) {{
{chr(10).join(routes)}
    case 'home':
    default:
        $title = "Bienvenido";
        ob_start();
        echo '<div class="p-5 mb-4 bg-light rounded-3">';
        echo '<div class="container-fluid py-5">';
        echo '<h1 class="display-5 fw-bold">Bienvenido al Generador CRUD</h1>';
        echo '<p class="col-md-8 fs-4">Selecciona una tabla del menú lateral para gestionar sus registros.</p>';
        echo '</div>';
        echo '</div>';
        $content = ob_get_clean();
        // CAMBIO AQUÍ: La ruta a layout.php debe ser relativa a 'views/'
        include(__DIR__ . '/views/layout.php');
        break;
}}

if (isset($controller) && method_exists($controller, $action_name)) {{
    $controller->$action_name();
}} elseif (isset($controller)) {{
    // Fallback if action does not exist for a given controller
    header("Location: index.php?controller=$controller_name&action=index");
    exit;
}}
?>"""